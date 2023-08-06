

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class EnvironmentActionVersion(Noun):

    _entity_def = \
        {'name': 'environment_action_version', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'version': {'type': 'string', 'description': 'The version number of the associated EnvironmentAction', 'required': True}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return EnvironmentActionVersion._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(EnvironmentActionVersion._entity_def)


    

    
        
    @property
    def version(self) -> str:
        return self._getter("version")

    @version.setter
    def version(self, value: str) -> None:
        self._setter("version", value)
    

    
        
    def get_to_environment_action_execution_has_environment_action_version_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.environment_action_execution_has_environment_action_version"]
    
        
    def get_to_environment_action_has_environment_action_version_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.environment_action_has_environment_action_version"]
    
    