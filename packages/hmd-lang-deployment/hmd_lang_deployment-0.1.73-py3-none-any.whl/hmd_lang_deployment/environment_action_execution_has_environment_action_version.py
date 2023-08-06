

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.environment_action_execution import EnvironmentActionExecution
from hmd_lang_deployment.environment_action_version import EnvironmentActionVersion
from datetime import datetime
from typing import List, Dict, Any

class EnvironmentActionExecutionHasEnvironmentActionVersion(Relationship):

    _entity_def = \
        {'name': 'environment_action_execution_has_environment_action_version', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.environment_action_execution', 'ref_to': 'hmd_lang_deployment.environment_action_version', 'attributes': {}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '*'}, 'ref_to': {'arrow': True, 'cardinality': '1'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return EnvironmentActionExecutionHasEnvironmentActionVersion._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(EnvironmentActionExecutionHasEnvironmentActionVersion._entity_def)


    @staticmethod
    def ref_from_type():
        return EnvironmentActionExecution

    @staticmethod
    def ref_to_type():
        return EnvironmentActionVersion

    

    