

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class RepoClassVersion(Noun):

    _entity_def = \
        {'name': 'repo_class_version', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'version': {'type': 'string', 'description': 'The version specifier.', 'required': True, 'business_id': True}, 'default_configuration': {'type': 'mapping', 'description': 'the default configuration for the repo class version', 'required': False}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoClassVersion._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoClassVersion._entity_def)


    

    
        
    @property
    def version(self) -> str:
        return self._getter("version")

    @version.setter
    def version(self, value: str) -> None:
        self._setter("version", value)
    
        
    @property
    def default_configuration(self) -> Dict:
        return self._getter("default_configuration")

    @default_configuration.setter
    def default_configuration(self, value: Dict) -> None:
        self._setter("default_configuration", value)
    

    
        
    def get_to_repo_class_has_repo_class_version_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.repo_class_has_repo_class_version"]
    
        
    def get_to_repo_instance_deployment_has_repo_class_version_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.repo_instance_deployment_has_repo_class_version"]
    
    
        
    def get_from_repo_class_version_has_external_artifact_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.repo_class_version_has_external_artifact"]
    
        
    def get_from_repo_class_version_has_repo_class_version_notes_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.repo_class_version_has_repo_class_version_notes"]
    
        
    def get_from_repo_class_version_req_repo_class_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.repo_class_version_req_repo_class"]
    