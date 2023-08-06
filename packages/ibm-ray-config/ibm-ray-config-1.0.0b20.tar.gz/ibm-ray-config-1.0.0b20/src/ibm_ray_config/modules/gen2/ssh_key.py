import os
import subprocess
from typing import Any, Dict
from pathlib import Path
from uuid import uuid4
import inquirer
from inquirer import errors
from ibm_ray_config.modules.config_builder import ConfigBuilder, update_decorator, spinner
from ibm_ray_config.modules.utils import (Color, color_msg, find_default, find_name_id,
                                        validate_exists, validate_not_empty, free_dialog)

from ibm_cloud_sdk_core import ApiException
DEFAULT_KEY_NAME = f'ray-{os.environ.get("USERNAME")}-{str(uuid4())[:5]}'
        
def generate_keypair():
    """Returns newly generated public ssh-key's contents and private key's path"""
    filename = f"{os.sep}tmp{os.sep}{DEFAULT_KEY_NAME}"

    os.system(f'ssh-keygen -b 2048 -t rsa -f {filename} -q -N ""')
    print(f"\n\n\033[92mSSH key pair been generated\n")
    print(f"private key intermediate location: {os.path.abspath(filename)}")
    print(f"public key intermediate location: {os.path.abspath(filename)}.pub\033[0m")
    with open(f"{filename}.pub", 'r') as file:
        ssh_key_data = file.read()
    ssh_key_path = os.path.abspath(filename)
    return ssh_key_data, ssh_key_path

def get_ssh_key(ibm_vpc_client, name):
    """Returns ssh key matching specified name, stored in the VPC associated with the vpc_client"""
    for key in ibm_vpc_client.list_keys().result['keys']:
        if key['name'] == name:
            return key
                    
def register_ssh_key(ibm_vpc_client, config, auto=False):
    """Returns:
        1. key's name on the VPC platform.
        2. it's public key's contents. 
        3. local path to private key ONLY if user generated a key, ELSE None.
        Registers an either existing or newly generated ssh-key to a specific VPC. """
    
    if config.get('ibm_vpc'):
        resource_group_id = config['ibm_vpc']['resource_group_id']
    else:
        for available_node_type in config['available_node_types']:
            resource_group_id = config['available_node_types'][available_node_type]['node_config']['resource_group_id']
            break

    keyname = DEFAULT_KEY_NAME

    EXISTING_CONTENTS = 'Paste existing public key contents'
    EXISTING_PATH = 'Provide path to existing public key'
    GENERATE_NEW = f'Generate new public key {color_msg("[Best Practice]",Color.LIGHTGREEN)}'

    questions = [
        inquirer.List('answer',
                      message="Please choose",
                      choices=[GENERATE_NEW, EXISTING_PATH, EXISTING_CONTENTS],
                      default=GENERATE_NEW
                      )]

    if not auto:
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    else:
        answers["answer"] = GENERATE_NEW

    public_ssh_key_data = ""
    private_ssh_key_path = None
    if answers["answer"] == EXISTING_CONTENTS:
        print("Registering from file contents")
        public_ssh_key_data = input(
            "[\033[33m?\033[0m] Please paste the contents of your public ssh key. It should start with ssh-rsa: ")
    elif answers["answer"] == EXISTING_PATH:
        print("Register in vpc existing key from path")
        questions = [
            inquirer.Text(
                "public_key_path", message='Please paste path to your \033[92mpublic\033[0m ssh key', validate=validate_exists)
        ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        with open(os.path.abspath(os.path.expanduser(answers["public_key_path"])), 'r') as file:
            public_ssh_key_data = file.read()
    else: # choice GENERATE_NEW
        public_ssh_key_data, private_ssh_key_path = generate_keypair()

    try:    # regardless of the above choices, try registering an ssh-key 
        response = ibm_vpc_client.create_key(public_key=public_ssh_key_data, name=keyname, resource_group={
                                        "id": resource_group_id}, type='rsa')
    except ApiException as e:
        if "Key with name already exists" in e.message:
            print(color_msg(f"Key by the name '{keyname}' already exists",Color.RED))
            keyname = free_dialog("Please specify a *unique* name for the new key")["answer"]
        else: 
            if "Key with fingerprint already exists" in e.message:
                print(color_msg("Can't register an SSH key with the same fingerprint",Color.RED))
            exit(1) # can't continue the configuration process without a valid ssh key   
            
    print(f"\033[92mnew SSH key: '{keyname}' been registered in vpc\033[0m")

    result = response.get_result()
    return result['name'], result['id'], private_ssh_key_path


DEPENDENCIES = {'ibm_vpc': {'resource_group_id': None}}


class SshKeyConfig(ConfigBuilder):

    def __init__(self, base_config: Dict[str, Any]) -> None:
        super().__init__(base_config)
        self.base_config = base_config

    def _validate_keypair(self, answers, current):
        if not current or not os.path.exists(os.path.abspath(os.path.expanduser(current))):
            raise errors.ValidationError(
            '', reason=f"File {current} doesn't exist")

        public_res = self.ibm_vpc_client.get_key(self.ssh_key_id).get_result()['public_key'].split(' ')[1]
        private_res = subprocess.getoutput([f"ssh-keygen -y -f {current} | cut -d' ' -f 2"])

        if not public_res == private_res:
            raise errors.ValidationError(
            '', reason=f"Private ssh key {current} and public key {self.ssh_key_name} are not a pair")

        return public_res == private_res

    @update_decorator
    def run(self) -> Dict[str, Any]:
        @spinner
        def get_ssh_key_objects():
            return self.ibm_vpc_client.list_keys().get_result()['keys']

        ssh_key_objects = get_ssh_key_objects()

        CREATE_NEW_SSH_KEY = f"""Register new SSH key in IBM VPC {color_msg("[Best Practice]",Color.LIGHTGREEN)}"""

        default = find_default(self.defaults, ssh_key_objects, id='key_id')
        default = default if default else CREATE_NEW_SSH_KEY
        ssh_key_name, ssh_key_id = find_name_id(
            ssh_key_objects, 'Choose ssh key', do_nothing=CREATE_NEW_SSH_KEY, default=default)
        
        private_ssh_key_path = None
        if not ssh_key_name: # user chose to create a new key / no keys registered
            ssh_key_name, ssh_key_id, private_ssh_key_path = register_ssh_key(
                self.ibm_vpc_client, self.base_config)

        self.ssh_key_id = ssh_key_id
        self.ssh_key_name = ssh_key_name

        # private_ssh_key_path is known only if user generated a key.  
        if not private_ssh_key_path:
            questions = [
                inquirer.Text(
                    "private_key_path", message=f'Please paste path to \033[92mprivate\033[0m ssh key associated with selected public key {ssh_key_name}',
                      validate=self._validate_keypair,
                      default=self.defaults.get('ssh_key_filename') or "~/.ssh/id_rsa")
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            private_ssh_key_path = os.path.abspath(
                os.path.expanduser(answers["private_key_path"]))

        # currently the user is hardcoded to root
        return ssh_key_id, private_ssh_key_path, 'root'

    @update_decorator
    def verify(self, base_config):
        default_keyname = DEFAULT_KEY_NAME
        
        if base_config.get('ibm_vpc'):
            resource_group_id = base_config['ibm_vpc']['resource_group_id']
        else:
            for available_node_type in base_config['available_node_types']:
                resource_group_id = base_config['available_node_types'][available_node_type]['node_config']['resource_group_id']
                break
        
        def is_pair(id, ssh_key_filename):
            public_res = self.ibm_vpc_client.get_key(id).get_result()['public_key'].split(' ')[1]
            private_res = subprocess.getoutput([f"ssh-keygen -y -f {ssh_key_filename} | cut -d' ' -f 2"])
            return public_res == private_res

        # user specified both vpc key id and private key, just validate they are a pair
        if self.defaults['key_id'] and self.defaults['ssh_key_filename']:
            if not is_pair(self.defaults['key_id'], self.defaults['ssh_key_filename']):
                raise errors.ValidationError(
                '', reason=f"Private ssh key {self.defaults['ssh_key_filename']} and public key {self.defaults['key_id']} are not a pair")
            
            return self.defaults['key_id'], self.defaults['ssh_key_filename'], 'root'
        elif self.defaults['ssh_key_filename']:
            # user provided private key only, check if there default ssh key already in vpc
            default_key = get_ssh_key(self.ibm_vpc_client, default_keyname)
            # and it match the specified private key
            if default_key and is_pair(default_key['id'], self.defaults['ssh_key_filename']):
                return default_key['id'], self.defaults['ssh_key_filename'], 'root'
            
            # not a pair. delete not matching default key from vpc if exists
            if default_key:
                self.ibm_vpc_client.delete_key(id=default_key['id'])
            # generate public key from private key
            ssh_key_data = subprocess.getoutput([f"ssh-keygen -y -f {self.defaults['ssh_key_filename']} | cut -d' ' -f 2"])
            response = self.ibm_vpc_client.create_key(public_key=ssh_key_data, name=default_keyname, resource_group={
                                        "id": resource_group_id}, type='rsa')
            print(f"\033[92mnew SSH key {default_keyname} been registered in vpc\033[0m")
            result = response.get_result()
            return result['id'], self.defaults['ssh_key_filename'], 'root'
        else:
            # check if there default ssh key already in vpc
            default_key = get_ssh_key(self.ibm_vpc_client, default_keyname)
            if default_key:
                self.ibm_vpc_client.delete_key(id=default_key['id'])

            # no ssh key information been provided by user, generate new keypair
            ssh_key_data, ssh_key_path = generate_keypair(default_keyname)    

            response = self.ibm_vpc_client.create_key(public_key=ssh_key_data, name=default_keyname, resource_group={
                                        "id": resource_group_id}, type='rsa')
            print(f"\033[92mnew SSH key {default_keyname} been registered in vpc\033[0m")
            result = response.get_result()
            return result['id'], ssh_key_path, 'root'

    @update_decorator
    def create_default(self):
        
        # if exist with same name - override
        _, key_id, ssh_key_path = register_ssh_key(self.ibm_vpc_client, self.base_config, auto=True)
        
        return key_id, ssh_key_path, 'root'