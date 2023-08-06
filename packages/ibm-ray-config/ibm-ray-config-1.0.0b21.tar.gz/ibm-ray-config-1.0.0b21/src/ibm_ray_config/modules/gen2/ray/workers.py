import re
import copy
from typing import Any, Dict
from uuid import uuid4
from ibm_ray_config.modules.config_builder import ConfigBuilder, spinner
from ibm_ray_config.modules.utils import (find_default, free_dialog, get_confirmation, get_option_from_list,
                                           validate_name, get_profile_resources)

class WorkersConfig(ConfigBuilder):
    def __init__(self, base_config: Dict[str, Any]) -> None:
        super().__init__(base_config)
        self.cluster_name_scheme = f'cluster-{uuid4().hex[:5]}'
        self.instance_profile_objects = self.get_instance_profile_objects()
        # stores the sum of max_workers requested in all node types
        self.global_max_workers = 0
    
    @spinner
    def get_instance_profile_objects(self):
        return self.ibm_vpc_client.list_instance_profiles().get_result()['profiles']

    def run(self) -> Dict[str, Any]:

        def get_workers_span():
            """prompt user for min, max worker values 

            Returns:
                Tuple: (min_workers, max_workers)
            """
            default_min_workers = self.base_config.get('min_workers', '0')
            min_workers = int(free_dialog(msg="Minimum number of worker nodes",
                                      default=default_min_workers,
                                      validate=lambda _, min_val: re.match('^[+]?[0-9]+$', min_val))['answer'])
            max_workers = int(free_dialog(msg="Maximum number of worker nodes",
                                      default=str(min_workers),
                                      validate=lambda _, max_val: re.match('^[+]?[0-9]+$', max_val) and int(max_val) >= int(min_workers))['answer'])
            # update the sum of workers requested in the config file
            self.global_max_workers += max_workers 
            return min_workers, max_workers

        def store_node_config(node_type, instance_profile, min_workers, max_workers, create_new_config=True):
            """stores the node config data in the cluster's config file 

            Args:
                node_type (str): short name for type of node to be configured, e.g. GPU_worker
                instance_profile (str): hardware specs for the vm, for this node type
                min_workers (int): the lower bound to scale in to, for this node type
                max_workers (int): the upper bound to scale out to, for this node type
                create_new_config (bool, optional): when set to false updates the DEFAULT_NODE_TYPE data. Defaults to True.
            """
            
            # add new node_type entry to configuration dict if create_new_config=True
            if create_new_config:
               self.base_config['available_node_types'][node_type] = copy.deepcopy(self.base_config['available_node_types'][self.DEFAULT_NODE_TYPE])
            node_data = self.base_config['available_node_types'][node_type]
            
            cpu_num, memory, gpu_num = get_profile_resources(instance_profile)
            node_data['node_config']['instance_profile_name'] = head_instance_profile
            node_data['resources']['CPU'] = cpu_num
            node_data['resources']['memory'] = memory
            if gpu_num:
                node_data['resources']['GPU'] = gpu_num

            node_data['min_workers'] = min_workers 
            node_data['max_workers'] = max_workers

        # get cluster name
        default_cluster_prefix = self.base_config.get('cluster_name')
        if not default_cluster_prefix:
            default_cluster_prefix = self.cluster_name_scheme.rsplit('-',1)[0]
        print(f"\ncluster name is: '{self.cluster_name_scheme}'")
        cluster_prefix = free_dialog(msg= f"Pick a custom name to replace: '{default_cluster_prefix}'(or Enter for default)",
                                default=default_cluster_prefix,
                                validate=validate_name)['answer']
        cluster_name = self.cluster_name_scheme.replace(default_cluster_prefix, cluster_prefix)
        self.base_config['cluster_name'] = cluster_name

        # create profile configs
        default = find_default(
            self.base_config, self.instance_profile_objects, name='instance_profile_name')
        head_instance_profile = get_option_from_list(
            'Choose instance profile for the Head node, please refer to https://cloud.ibm.com/docs/vpc?topic=vpc-profiles',
            self.instance_profile_objects,
            default=default)['name']
        
        multipurpose = get_confirmation("Use head profile for workers as well?", default=True)
        default_type_min_workers, default_type_max_workers = get_workers_span() if multipurpose else (0, 0)
        store_node_config(self.DEFAULT_NODE_TYPE, head_instance_profile, default_type_min_workers,
                           default_type_max_workers, create_new_config=False)
        
        worker_types_counter = 0
        while get_confirmation("Add a worker profile?", default=False):
            worker_types_counter += 1
            worker_instance_profile = get_option_from_list(
                'Choose instance profile for the worker node, please refer to https://cloud.ibm.com/docs/vpc?topic=vpc-profiles',
                self.instance_profile_objects,
                default=default)['name']
            worker_type_min_workers, worker_type_max_workers = get_workers_span()
            store_node_config(self.DEFAULT_NODE_TYPE+str(worker_types_counter), worker_instance_profile,
                               worker_type_min_workers, worker_type_max_workers)
            
        print(f"Global max workers is set to the sum of all max_workers: '{self.global_max_workers}'")
        if self.global_max_workers: # redundant question if only head node can be created  
            self.global_max_workers = int(free_dialog(msg= f"Edit to adjust value (or Enter for default)",
                                    default=self.global_max_workers,
                                    validate=lambda _, val: re.match('^[+]?[0-9]+$', val))['answer'])
        self.base_config['max_workers'] = self.global_max_workers

        return self.base_config

    
    def verify(self, base_config):
        min_workers = base_config['available_node_types'][self.DEFAULT_NODE_TYPE]['min_workers']
        max_workers = base_config['available_node_types'][self.DEFAULT_NODE_TYPE]['max_workers']
        
        if max_workers < min_workers:
            raise Exception(f'specified min workers {min_workers} larger than max workers {max_workers}')

        return base_config
