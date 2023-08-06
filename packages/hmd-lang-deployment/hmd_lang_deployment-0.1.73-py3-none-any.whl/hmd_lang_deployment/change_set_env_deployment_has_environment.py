

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.change_set_env_deployment import ChangeSetEnvDeployment
from hmd_lang_deployment.environment import Environment
from datetime import datetime
from typing import List, Dict, Any

class ChangeSetEnvDeploymentHasEnvironment(Relationship):

    _entity_def = \
        {'name': 'change_set_env_deployment_has_environment', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.change_set_env_deployment', 'ref_to': 'hmd_lang_deployment.environment', 'attributes': {}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '*'}, 'ref_to': {'arrow': True, 'cardinality': '1'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ChangeSetEnvDeploymentHasEnvironment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ChangeSetEnvDeploymentHasEnvironment._entity_def)


    @staticmethod
    def ref_from_type():
        return ChangeSetEnvDeployment

    @staticmethod
    def ref_to_type():
        return Environment

    

    