

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class RepoClass(Noun):

    _entity_def = \
        {'name': 'repo_class', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'repo_class_name': {'type': 'string', 'description': 'The common name of the repository.', 'business_id': True, 'required': True}, 'deploy_commands': {'type': 'collection', 'description': 'a list of commands that are required to deploy', 'required': False}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoClass._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoClass._entity_def)


    

    
        
    @property
    def repo_class_name(self) -> str:
        return self._getter("repo_class_name")

    @repo_class_name.setter
    def repo_class_name(self, value: str) -> None:
        self._setter("repo_class_name", value)
    
        
    @property
    def deploy_commands(self) -> List:
        return self._getter("deploy_commands")

    @deploy_commands.setter
    def deploy_commands(self, value: List) -> None:
        self._setter("deploy_commands", value)
    

    
        
    def get_to_repo_class_version_req_repo_class_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.repo_class_version_req_repo_class"]
    
        
    def get_to_repo_instance_isa_repo_class_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.repo_instance_isa_repo_class"]
    
    
        
    def get_from_repo_class_has_repo_class_version_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.repo_class_has_repo_class_version"]
    