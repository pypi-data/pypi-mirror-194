

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class ChangeSetEnvDeployment(Noun):

    _entity_def = \
        {'name': 'change_set_env_deployment', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'deploy_time': {'type': 'timestamp', 'description': 'The time that the ChangeSet was deployed.', 'required': True}, 'csed_status': {'type': 'enum', 'enum_def': ['CREATED', 'STARTED', 'COMPLETED', 'FAILED', 'SKIPPED', 'DESTROYED']}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ChangeSetEnvDeployment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ChangeSetEnvDeployment._entity_def)


    

    
        
    @property
    def deploy_time(self) -> datetime:
        return self._getter("deploy_time")

    @deploy_time.setter
    def deploy_time(self, value: datetime) -> None:
        self._setter("deploy_time", value)
    
        
    @property
    def csed_status(self) -> str:
        return self._getter("csed_status")

    @csed_status.setter
    def csed_status(self, value: str) -> None:
        self._setter("csed_status", value)
    

    
        
    def get_to_change_set_deployment_has_change_set_env_deployment_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.change_set_deployment_has_change_set_env_deployment"]
    
    
        
    def get_from_change_set_env_deployment_has_environment_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.change_set_env_deployment_has_environment"]
    
        
    def get_from_change_set_env_deployment_has_environment_action_execution_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.change_set_env_deployment_has_environment_action_execution"]
    
        
    def get_from_change_set_env_deployment_has_repo_instance_deployment_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.change_set_env_deployment_has_repo_instance_deployment"]
    