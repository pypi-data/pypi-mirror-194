

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class Environment(Noun):

    _entity_def = \
        {'name': 'environment', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'type': {'type': 'string', 'description': 'The environment type, e.g., dev, prod, etc.', 'required': True, 'business_id': True}, 'account_number': {'type': 'string', 'description': 'the account number', 'required': True}, 'hmd_region': {'type': 'string', 'required': True}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return Environment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(Environment._entity_def)


    

    
        
    @property
    def type(self) -> str:
        return self._getter("type")

    @type.setter
    def type(self, value: str) -> None:
        self._setter("type", value)
    
        
    @property
    def account_number(self) -> str:
        return self._getter("account_number")

    @account_number.setter
    def account_number(self, value: str) -> None:
        self._setter("account_number", value)
    
        
    @property
    def hmd_region(self) -> str:
        return self._getter("hmd_region")

    @hmd_region.setter
    def hmd_region(self, value: str) -> None:
        self._setter("hmd_region", value)
    

    
        
    def get_to_change_set_env_deployment_has_environment_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.change_set_env_deployment_has_environment"]
    
    
        
    def get_from_environment_has_repo_instance_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.environment_has_repo_instance"]
    