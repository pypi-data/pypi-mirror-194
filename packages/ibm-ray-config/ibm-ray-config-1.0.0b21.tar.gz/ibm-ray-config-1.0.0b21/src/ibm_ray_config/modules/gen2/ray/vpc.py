from typing import Any, Dict
from uuid import uuid4
import inquirer
from ibm_ray_config.modules.config_builder import ConfigBuilder, update_decorator, spinner
from ibm_ray_config.modules.utils import (Color, color_msg, get_confirmation,find_default, find_name_id,
                                        get_option_from_list, free_dialog, validate_name, CACHE)


REQUIRED_RULES = {'outbound_tcp_all': 'selected security group is missing rule permitting outbound TCP access\n', 'outbound_udp_all': 'selected security group is missing rule permitting outbound UDP access\n', 'inbound_tcp_sg': 'selected security group is missing rule permitting inbound tcp traffic inside selected security group\n',
                  'inbound_tcp_22': 'selected security group is missing rule permitting inbound traffic to tcp port 22 required for ssh\n'}
INSECURE_RULES = {'inbound_tcp_6379': 'selected security group is missing rule permitting inbound traffic to tcp port 6379 required for Redis\n', 'inbound_tcp_8265': 'selected security group is missing rule permitting inbound traffic to tcp port 8265 required to access Ray Dashboard\n'}

def validate_security_group(ibm_vpc_client, sec_group_id):
    errors = validate_security_group_rules(ibm_vpc_client, sec_group_id)

    if errors:
        for val in errors.values():
            print(f"\033[91m{val}\033[0m")

        questions = [
            inquirer.List('answer',
                          message='Selected security group is missing required rules, see error above, update with required rules?',
                          choices=['yes', 'no'], default='yes'
                          ), ]

        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)

        if answers['answer'] == 'yes':
            add_rules_to_security_group(ibm_vpc_client, sec_group_id, errors)
        else:
            exit(1)

        # just in case, validate again the updated/created security group
        errors = validate_security_group_rules(ibm_vpc_client, sec_group_id)
        if not errors:
            return
        else:
            print(f'Something failed during security group rules update/create, please update the required rules manually using ibmcli or web ui and try again')
            exit(1)
    else:
        return


def validate_security_group_rules(ibm_vpc_client, sg_id):
    """
    returns unsatisfied security group rules.
    """

    required_rules = REQUIRED_RULES.copy()

    sg = ibm_vpc_client.get_security_group(sg_id).get_result()

    for rule in sg['rules']:

        # check outbound rules that are not associated with a specific IP address range
        if rule['direction'] == 'outbound' and rule['remote'] == {'cidr_block': '0.0.0.0/0'}:
            if rule['protocol'] == 'all':
                # outbound is fine!
                required_rules.pop('outbound_tcp_all', None)
                required_rules.pop('outbound_udp_all', None)
            elif rule['protocol'] == 'tcp':
                required_rules.pop('outbound_tcp_all', None)
            elif rule['protocol'] == 'udp':
                required_rules.pop('outbound_udp_all', None)

        # Check inbound rules
        elif rule['direction'] == 'inbound':
            # check rules that are not associated with a specific IP address range
            if rule['remote'] == {'cidr_block': '0.0.0.0/0'}:
                # we interested only in all or tcp protocols
                if rule['protocol'] == 'all':
                    # there a rule permitting all traffic
                    required_rules.pop('inbound_tcp_sg', None)
                    required_rules.pop('inbound_tcp_22', None)
                    required_rules.pop('inbound_tcp_6379', None)
                    required_rules.pop('inbound_tcp_8265', None)

                elif rule['protocol'] == 'tcp':
                    if rule['port_min'] == 1 and rule['port_max'] == 65535:
                        # all ports are open
                        required_rules.pop('inbound_tcp_sg', None)
                        required_rules.pop('inbound_tcp_22', None)
                        required_rules.pop('inbound_tcp_6379', None)
                        required_rules.pop('inbound_tcp_8265', None)
                    else:
                        port_min = rule['port_min']
                        port_max = rule['port_max']
                        if port_min <= 22 and port_max >= 22:
                            required_rules.pop('inbound_tcp_22', None)
                        elif port_min <= 6379 and port_max >= 6379:
                            required_rules.pop('inbound_tcp_6379', None)
                        elif port_min <= 8265 and port_max >= 8265:
                            required_rules.pop('inbound_tcp_8265', None)

            # rule regards private traffic within the VSIs associated with the security group
            elif rule['remote'].get('id') == sg['id']:
                # validate that inbound traffic inside group available
                if rule['protocol'] == 'all' or rule['protocol'] == 'tcp':
                    required_rules.pop('inbound_tcp_sg', None)

    return required_rules


def add_rules_to_security_group(ibm_vpc_client, sg_id, missing_rules):
    add_rule_msgs = {
        'outbound_tcp_all': f'Add rule to open all outbound TCP ports in selected security group {sg_id}',
        'outbound_udp_all': f'Add rule to open all outbound UDP ports in selected security group {sg_id}',
        'inbound_tcp_sg': f'Add rule to open inbound tcp traffic inside selected security group {sg_id}',
        'inbound_tcp_22': f'Add rule to open inbound tcp port 22 required for SSH in selected security group {sg_id}',
        'inbound_tcp_6379': f'Add rule to open inbound tcp port 6379 required for Redis in selected security group {sg_id}',
        'inbound_tcp_8265': f'Add rule to open inbound tcp port 8265 required to access Ray Dashboard in selected security group {sg_id}'}

    for missing_rule in missing_rules.keys():
        q = [
            inquirer.List('answer',
                          message=add_rule_msgs[missing_rule],
                          choices=['yes', 'no'],
                          default='yes')
        ]

        answers = inquirer.prompt(q, raise_keyboard_interrupt=True)
        if answers['answer'] == 'yes':
            security_group_rule_prototype_model = build_security_group_rule_prototype_model(
                missing_rule, sg_id=sg_id)
            ibm_vpc_client.create_security_group_rule(
                sg_id, security_group_rule_prototype_model).get_result()
        else:
            return False
    return True


def build_security_group_rule_prototype_model(missing_rule, sg_id=None):
    direction, protocol, port = missing_rule.split('_')
    remote = {"cidr_block": "0.0.0.0/0"}

    try:
        port = int(port)
        port_min = port
        port_max = port
    except:
        port_min = 1
        port_max = 65535

        # only valid if security group already exists
        if port == 'sg':
            if not sg_id:
                return None
            remote = {'id': sg_id}

    return {
        'direction': direction,
        'ip_version': 'ipv4',
        'protocol': protocol,
        'remote': remote,
        'port_min': port_min,
        'port_max': port_max
    }


class RayVPCConfig(ConfigBuilder):

    def __init__(self, base_config: Dict[str, Any]) -> None:
        super().__init__(base_config)
        self.region = self.get_region()
        self.default_vpc_name_scheme = f'vpc-{uuid4().hex[:5]}'

        if base_config.get('available_node_types'):
            for available_node_type in self.base_config['available_node_types']:
                self.defaults['vpc_id'] = base_config['available_node_types'][available_node_type]['node_config'].get('vpc_id')
                break

    def update_config(self, vpc_obj, zone_obj, subnet_id):
        sec_group_id = vpc_obj['default_security_group']['id']

        validate_security_group(self.ibm_vpc_client, sec_group_id)

        self.base_config['provider']['zone_name'] = zone_obj['name']

        node_config = {
            'vpc_id': vpc_obj['id'],
            'resource_group_id': vpc_obj['resource_group']['id'],
            'security_group_id': sec_group_id,
            'subnet_id': subnet_id
        }

        if self.base_config.get('available_node_types'):
            for available_node_type in self.base_config['available_node_types']:
                self.base_config['available_node_types'][available_node_type]['node_config'].update(
                    node_config)
        else:
            self.base_config['available_node_types'] = {
                self.DEFAULT_NODE_TYPE: {'node_config': node_config}}


    @update_decorator
    def run(self) -> Dict[str, Any]:
        vpc_obj, zone_obj = self._select_vpc(self.base_config, self.region)

        if not vpc_obj:
            raise Exception(f'Failed to select VPC')

        all_subnet_objects = self.ibm_vpc_client.list_subnets().get_result()[
            'subnets']

        # filter only subnets from selected availability zone
        subnet_objects = [s_obj for s_obj in all_subnet_objects if s_obj['zone']
                          ['name'] == zone_obj['name'] and s_obj['vpc']['id'] == vpc_obj['id']]

        if not subnet_objects:
            raise f'Failed to find subnet for vpc {vpc_obj["name"]} in zone {zone_obj["name"]}'

        return vpc_obj, zone_obj, subnet_objects[0]['id']

    def _build_security_group_rule_prototype_model(self, missing_rule, sg_id=None):
        direction, protocol, port = missing_rule.split('_')
        remote = {"cidr_block": "0.0.0.0/0"}

        try: # port number was specified
            port = int(port)
            port_min = port
            port_max = port
        except:
            port_min = 1
            port_max = 65535

            # only valid if security group already exists
            if port == 'sg':
                if not sg_id:
                    return None
                remote = {'id': sg_id}

        return {
            'direction': direction,
            'ip_version': 'ipv4',
            'protocol': protocol,
            'remote': remote,
            'port_min': port_min,
            'port_max': port_max
        }

    def _create_vpc(self, ibm_vpc_client, resource_group, auto=False):
        @spinner
        def _create():
            return ibm_vpc_client.create_vpc(address_prefix_management='auto', classic_access=False,
                                            name=vpc_name, resource_group=resource_group).get_result()
        default_vpc_prefix = self.default_vpc_name_scheme.rsplit('-',1)[0]
        if auto:
            vpc_prefix = default_vpc_prefix
        else:
            print(f"VPC name is: '{self.default_vpc_name_scheme}'")
            vpc_prefix = free_dialog(msg= f"Pick a custom name to replace: '{default_vpc_prefix}'(or Enter for default)",
                                    default=default_vpc_prefix,
                                    validate=validate_name)['answer']
        vpc_name = self.default_vpc_name_scheme.replace(default_vpc_prefix, vpc_prefix)

        return _create()


    def _create_vpc_peripherals(self, ibm_vpc_client, vpc_obj, zone_obj, resource_group):
        vpc_name = vpc_obj['name']
        vpc_id = vpc_obj['id']
        # create subnet
        subnet_name = '{}-subnet'.format(vpc_name)
        subnet_data = None

        # find cidr
        ipv4_cidr_block = None
        res = ibm_vpc_client.list_vpc_address_prefixes(
            vpc_id).result
        address_prefixes = res['address_prefixes']

        # searching for the CIDR block (internal ip range) matching the specified zone of a VPC (whose region has already been set)
        for address_prefix in address_prefixes:
            if address_prefix['zone']['name'] == zone_obj['name']:
                ipv4_cidr_block = address_prefix['cidr']
                break

        subnet_prototype = {}
        subnet_prototype['zone'] = {'name': zone_obj['name']}
        subnet_prototype['ip_version'] = 'ipv4'
        subnet_prototype['name'] = subnet_name
        subnet_prototype['resource_group'] = resource_group
        subnet_prototype['vpc'] = {'id': vpc_id}
        subnet_prototype['ipv4_cidr_block'] = ipv4_cidr_block

        subnet_data = ibm_vpc_client.create_subnet(
            subnet_prototype).result
        subnet_id = subnet_data['id']

        # create public gateway
        gateway_id = self.create_public_gateway(vpc_obj, zone_obj, resource_group, subnet_name)

        # Attach public gateway to the subnet
        ibm_vpc_client.set_subnet_public_gateway(
            subnet_id, {'id': gateway_id})

        print(color_msg(f"VPC subnet {subnet_prototype['name']} been created and attached to gateway", color=Color.LIGHTGREEN))
        
        # Update security group to have all required rules
        sg_id = vpc_obj['default_security_group']['id']

        # update sg name
        sg_name = '{}-sg'.format(vpc_name)
        ibm_vpc_client.update_security_group(
            sg_id, security_group_patch={'name': sg_name})

        # add rule to open private tcp traffic between VSIs within the security group
        sg_rule_prototype = self._build_security_group_rule_prototype_model(
            'inbound_tcp_sg', sg_id=sg_id)
        res = ibm_vpc_client.create_security_group_rule(
            sg_id, sg_rule_prototype).get_result()

        # add all other required rules configured by the specific backend
        is_insecure = get_confirmation("Would you like to open insecure ports: 6379 and 8265?", default=False)
        if is_insecure:
            REQUIRED_RULES.update(INSECURE_RULES)
        for rule in REQUIRED_RULES.keys():
            sg_rule_prototype = self._build_security_group_rule_prototype_model(
                rule)
            if sg_rule_prototype:
                res = ibm_vpc_client.create_security_group_rule(
                    sg_id, sg_rule_prototype).get_result()

        print(color_msg(f"Security group {sg_name} been updated with required rules", color=Color.LIGHTGREEN))

    def create_public_gateway(self, vpc_obj, zone_obj, resource_group, subnet_name):
        vpc_id = vpc_obj['id']

        gateway_prototype = {}
        gateway_prototype['vpc'] = {'id': vpc_id}
        gateway_prototype['zone'] = {'name': zone_obj['name']}
        gateway_prototype['name'] = f"{subnet_name}-gw"
        gateway_prototype['resource_group'] = resource_group
        gateway_data = self.ibm_vpc_client.create_public_gateway(
            **gateway_prototype).get_result()
        gateway_id = gateway_data['id']

        print(
            f"\033[92mVPC public gateway {gateway_prototype['name']} been created\033[0m")

        return gateway_id

    def _select_resource_group(self, auto=False):
        # find resource group

        @spinner
        def get_res_group_objects():
            return self.resource_service_client.list_resource_groups().get_result()['resources']

        res_group_objects = get_res_group_objects()
        if auto:
            return res_group_objects[0]['id']

        default = find_default(
            self.defaults, res_group_objects, id='resource_group_id')
        res_group_obj = get_option_from_list(
            "Select resource group", res_group_objects, default=default)
        return res_group_obj['id']

    def _select_zone(self, vpc_id, region, auto=False):
        # find availability zone
        @spinner
        def get_zones_and_subnets():
            zones_objects = self.ibm_vpc_client.list_region_zones(region).get_result()['zones']
            all_subnet_objects = self.ibm_vpc_client.list_subnets().get_result()['subnets']
            return zones_objects, all_subnet_objects

        zones_objects, all_subnet_objects = get_zones_and_subnets()

        if auto:
            return zones_objects[0]

        if vpc_id:
            # filter out zones that given vpc has no subnets in
            zones = [s_obj['zone']['name']
                        for s_obj in all_subnet_objects if s_obj['vpc']['id'] == vpc_id]
            zones_objects = [
                z for z in zones_objects if z['name'] in zones]

        try:
            default = find_default(
                self.defaults, zones_objects, name='zone_name')
            zone_obj = get_option_from_list(
                "Choose availability zone", zones_objects, default=default)
        except:
            raise Exception(
                "Failed to list zones for selected vpc {vpc_id}, please check whether vpc missing subnet")

        return zone_obj

    def _select_vpc(self, node_config, region):

        vpc_id, vpc_name, zone_obj, sg_id, resource_group = None, None, None, None, None
        ibm_vpc_client = self.ibm_vpc_client

        while True:
            CREATE_NEW = 'Create new VPC'

            @spinner
            def list_vpcs():
                return ibm_vpc_client.list_vpcs().get_result()['vpcs']

            vpc_objects = list_vpcs()
            default = find_default(self.defaults, vpc_objects, id='vpc_id')

            vpc_name, vpc_id = find_name_id(
                vpc_objects, "Select VPC", obj_id=vpc_id, do_nothing=CREATE_NEW, default=default)
            zone_obj = self._select_zone(vpc_id, region)

            # Create a new VPC
            if not vpc_name:
                resource_group_id = self._select_resource_group()
                print(color_msg(f"Using resource group id: {resource_group_id}",color=Color.LIGHTGREEN))
                resource_group = {'id': resource_group_id}

                vpc_obj = self._create_vpc(ibm_vpc_client, resource_group)
                if not vpc_obj:     # User declined create a new VPC
                    continue        # the loop will restart
                else:   # User created a new VPC
                    vpc_name = vpc_obj['name']
                    vpc_id = vpc_obj['id']
                    print(color_msg(f"VPC: {vpc_name} with id: {vpc_id} been created", color=Color.LIGHTGREEN))

                    self._create_vpc_peripherals(ibm_vpc_client, vpc_obj, zone_obj, resource_group)
                    break           # VPC created, exit the VPC creation loop

            # User chose an existing VPC
            else:
                # validate chosen vpc has all requirements
                # starting from validating each of its subnets has public gateway

                @spinner
                def get_vpc_obj_and_subnets():
                    vpc_obj = ibm_vpc_client.get_vpc(id=vpc_id).result
                    all_subnet_objects = ibm_vpc_client.list_subnets().get_result()['subnets']
                    return vpc_obj, all_subnet_objects

                vpc_obj, all_subnet_objects = get_vpc_obj_and_subnets()
                resource_group = {'id': vpc_obj['resource_group']['id']}

                subnet_objects = [s_obj for s_obj in all_subnet_objects if s_obj['zone']
                          ['name'] == zone_obj['name'] and s_obj['vpc']['id'] == vpc_obj['id']]

                gw_id = None
                for subnet in subnet_objects:
                    gw = subnet.get('public_gateway')
                    if not gw:
                        if not gw_id:
                            questions = [
                                inquirer.List('answer',
                                    message=f'Selected vpcs {vpc_obj["name"]} subnet {subnet["name"]} is missing required public gateway, create a new one?',
                                    choices=['yes', 'no'], default='yes'
                                ), ]

                            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)

                            if answers['answer'] == 'yes':
                                gw_id = self.create_public_gateway(vpc_obj, zone_obj, resource_group, subnet['name'])
                            else:
                                exit(1)

                        # attach gateway to subnet
                        ibm_vpc_client.set_subnet_public_gateway(subnet['id'], {'id': gw_id})
                    else:
                        gw_id = gw['id']
                break

        CACHE['resource_group_id'] = resource_group['id']
        CACHE['vpc_name'] = vpc_obj['name']  # used to create the cluster's name at the workers module

        return vpc_obj, zone_obj

    @update_decorator
    def verify(self, base_config):
        # if vpc_id not specified will look for the first one

        if self.defaults['vpc_id']:
            vpc_obj = self.ibm_vpc_client.get_vpc(id=self.defaults['vpc_id']).result
        else:
            vpc_objects = self.ibm_vpc_client.list_vpcs().result
            if vpc_objects['total_count'] > 0:
                # return first vpc occurrence
                vpc_obj = vpc_objects['vpcs'][0]
            else:
                # create new vpc
                res_group_objects = self.resource_service_client.list_resource_groups().get_result()['resources']

                print(f"Selected first found resource group {res_group_objects[0]['name']}")
                resource_group = resource_group = {'id': res_group_objects[0]['id']}

                print(f"\n\n\033[92mRegion {self.region} been selected\033[0m")

                vpc_obj = self.ibm_vpc_client.create_vpc(address_prefix_management='auto', classic_access=False,
                                        name="ray-default-vpc", resource_group=resource_group).get_result()

                print(f"\n\n\033[92mVPC {vpc_obj['name']} been created\033[0m")

                zones_objects = self.ibm_vpc_client.list_region_zones(self.region).get_result()['zones']
                zone_obj = zones_objects[0]
                self._create_vpc_peripherals(self.ibm_vpc_client, vpc_obj, zone_obj, resource_group)

        subnet_objects = self.ibm_vpc_client.list_subnets().get_result()['subnets']
        return vpc_obj, subnet_objects[0]['zone'], subnet_objects[0]['id']

    @update_decorator
    def create_default(self):
        resource_group_id = self._select_resource_group(auto=True)
        print(color_msg(f"Using resource group id: {resource_group_id}",color=Color.LIGHTGREEN))
        resource_group = {'id': resource_group_id}

        vpc_objects = self.ibm_vpc_client.list_vpcs().get_result()['vpcs']
        vpc_obj = next((vpc_obj for vpc_obj in vpc_objects if self.default_vpc_name_scheme in vpc_obj['name']), None)

        if vpc_obj:
            # TODO: validate existing
            print(f"\n\n\033[92mUsing existing VPC with default name {vpc_obj['name']} \033[0m")
        else:
            vpc_name = f"{self.default_vpc_name_scheme}"
            vpc_obj = self._create_vpc(self.ibm_vpc_client,
                                    resource_group, vpc_name, auto=True)
            if not vpc_obj:
                raise Exception(f"Failed to create VPC {vpc_name}")
            else:
                print(f"\n\n\033[92mVPC {vpc_obj['name']} been created\033[0m")

            zone_obj = self._select_zone(vpc_obj['id'], self.region, auto=True)
            self._create_vpc_peripherals(self.ibm_vpc_client,
                                        vpc_obj,
                                        zone_obj,
                                        resource_group)

        zone_obj = self._select_zone(vpc_obj['id'], self.region, auto=True)
        CACHE['resource_group_id'] = resource_group['id']

        all_subnet_objects = self.ibm_vpc_client.list_subnets().get_result()[
            'subnets']

        # filter only subnets from selected availability zone
        subnet_objects = [s_obj for s_obj in all_subnet_objects if s_obj['zone']
                          ['name'] == zone_obj['name'] and s_obj['vpc']['id'] == vpc_obj['id']]

        if not subnet_objects:
            raise f'Failed to find subnet for vpc {vpc_obj["name"]} in zone {zone_obj["name"]}'

        return vpc_obj, zone_obj, subnet_objects[0]['id']