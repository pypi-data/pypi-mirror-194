

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class EnvironmentActionExecution(Noun):

    _entity_def = \
        {'name': 'environment_action_execution', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'execute_time': {'type': 'timestamp', 'description': 'The time that the EnvironmentAction was executed.', 'required': True}, 'ea_status': {'type': 'enum', 'enum_def': ['FAILED', 'SUCCEEDED'], 'description': 'The status of the action execution.', 'required': True}, 'message': {'type': 'string', 'description': 'A result message of the action, if available.'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return EnvironmentActionExecution._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(EnvironmentActionExecution._entity_def)


    

    
        
    @property
    def execute_time(self) -> datetime:
        return self._getter("execute_time")

    @execute_time.setter
    def execute_time(self, value: datetime) -> None:
        self._setter("execute_time", value)
    
        
    @property
    def ea_status(self) -> str:
        return self._getter("ea_status")

    @ea_status.setter
    def ea_status(self, value: str) -> None:
        self._setter("ea_status", value)
    
        
    @property
    def message(self) -> str:
        return self._getter("message")

    @message.setter
    def message(self, value: str) -> None:
        self._setter("message", value)
    

    
        
    def get_to_change_set_env_deployment_has_environment_action_execution_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.change_set_env_deployment_has_environment_action_execution"]
    
    
        
    def get_from_environment_action_execution_has_environment_action_version_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.environment_action_execution_has_environment_action_version"]
    