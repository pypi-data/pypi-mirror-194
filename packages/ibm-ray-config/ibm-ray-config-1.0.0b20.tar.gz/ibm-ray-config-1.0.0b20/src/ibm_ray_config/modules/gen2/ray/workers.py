import re
import copy
from typing import Any, Dict
from uuid import uuid4
import inquirer
from ibm_ray_config.modules.config_builder import ConfigBuilder
from ibm_ray_config.modules.utils import CACHE, free_dialog, validate_name, get_profile_resources

class WorkersConfig(ConfigBuilder):
    def __init__(self, base_config: Dict[str, Any]) -> None:
        super().__init__(base_config)
        self.cluster_name_scheme = f'cluster-{uuid4().hex[:5]}'
    

    def run(self) -> Dict[str, Any]:
        default_cluster_prefix = self.base_config.get('cluster_name')
        if not default_cluster_prefix:
            default_cluster_prefix = self.cluster_name_scheme.rsplit('-',1)[0]
        default_min_workers = self.base_config.get('min_workers', '0')
        default_max_workers = default_min_workers

        question = [
            inquirer.Text('min_workers', message="Minimum number of worker nodes",
                          default=default_min_workers, validate=lambda _, x: re.match('^[+]?[0-9]+$', x)),
            inquirer.Text('max_workers', message="Maximum number of worker nodes", default=default_max_workers,
                          validate=lambda answers, x: re.match('^[+]?[0-9]+$', x) and int(x) >= int(answers['min_workers']))
        ]

        print(f"\ncluster name is: '{self.cluster_name_scheme}'")
        cluster_prefix = free_dialog(msg= f"Pick a custom name to replace: '{default_cluster_prefix}'(or Enter for default)",
                                default=default_cluster_prefix,
                                validate=validate_name)['answer']
        answers = inquirer.prompt(question, raise_keyboard_interrupt=True)
        # replaces first word of self.cluster_name_scheme with user input.
        cluster_name = self.cluster_name_scheme.replace(default_cluster_prefix, cluster_prefix)
        self.base_config['cluster_name'] = cluster_name
        self.base_config['max_workers'] = int(answers['max_workers'])

        if self.base_config.get('worker_instance_profile', None):
            self.base_config['available_node_types']['ray_head_default']['min_workers'] = 0 
            self.base_config['available_node_types']['ray_head_default']['max_workers'] = 0

            worker_dict = copy.deepcopy(self.base_config['available_node_types']['ray_head_default'])
            worker_dict['node_config'].pop('head_ip',None)

            worker_dict['min_workers'] = int(answers['min_workers'])
            worker_dict['max_workers'] = int(answers['max_workers'])
            worker_dict['node_config']['instance_profile_name'] = self.base_config['worker_instance_profile']
            
            cpu, memory, gpu = get_profile_resources(self.base_config['worker_instance_profile'])
            if gpu:
                worker_dict['resources']['GPU'] = gpu
            worker_dict['resources']['CPU'] = cpu
            worker_dict['resources']['memory'] = memory

            self.base_config['available_node_types']['ray_worker_default'] = worker_dict
            del self.base_config['worker_instance_profile']
        else:
            self.base_config['available_node_types']['ray_head_default']['min_workers'] = int(answers['min_workers'])
            self.base_config['available_node_types']['ray_head_default']['max_workers'] = int(answers['max_workers'])

        return self.base_config
    
    def verify(self, base_config):
        min_workers = base_config['available_node_types']['ray_head_default']['min_workers']
        max_workers = base_config['available_node_types']['ray_head_default']['max_workers']
        
        if max_workers < min_workers:
            raise Exception(f'specified min workers {min_workers} larger than max workers {max_workers}')

        return base_config
