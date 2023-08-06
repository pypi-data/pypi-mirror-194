

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class EnvironmentAction(Noun):

    _entity_def = \
        {'name': 'environment_action', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'action_name': {'type': 'string', 'description': 'The common name of the repository.', 'business_id': True, 'required': True}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return EnvironmentAction._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(EnvironmentAction._entity_def)


    

    
        
    @property
    def action_name(self) -> str:
        return self._getter("action_name")

    @action_name.setter
    def action_name(self, value: str) -> None:
        self._setter("action_name", value)
    

    
    
        
    def get_from_environment_action_has_environment_action_version_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.environment_action_has_environment_action_version"]
    