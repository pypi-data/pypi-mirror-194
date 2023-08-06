

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class RepoInstance(Noun):

    _entity_def = \
        {'name': 'repo_instance', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'name': {'type': 'string', 'description': 'The instance name.', 'required': True, 'business_id': True}, 'auto_deploy': {'type': 'string', 'description': 'A flag indicating whether auto-deploy is supported by the deployment set. Expects ["true","false"]'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoInstance._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoInstance._entity_def)


    

    
        
    @property
    def name(self) -> str:
        return self._getter("name")

    @name.setter
    def name(self, value: str) -> None:
        self._setter("name", value)
    
        
    @property
    def auto_deploy(self) -> str:
        return self._getter("auto_deploy")

    @auto_deploy.setter
    def auto_deploy(self, value: str) -> None:
        self._setter("auto_deploy", value)
    

    
        
    def get_to_environment_has_repo_instance_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.environment_has_repo_instance"]
    
        
    def get_to_repo_instance_req_repo_instance_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.repo_instance_req_repo_instance"]
    
    
        
    def get_from_repo_instance_has_repo_instance_deployment_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.repo_instance_has_repo_instance_deployment"]
    
        
    def get_from_repo_instance_isa_repo_class_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.repo_instance_isa_repo_class"]
    
        
    def get_from_repo_instance_req_repo_instance_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.repo_instance_req_repo_instance"]
    