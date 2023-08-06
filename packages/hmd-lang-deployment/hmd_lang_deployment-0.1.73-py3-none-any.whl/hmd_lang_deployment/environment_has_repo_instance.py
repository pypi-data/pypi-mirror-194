

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.environment import Environment
from hmd_lang_deployment.repo_instance import RepoInstance
from datetime import datetime
from typing import List, Dict, Any

class EnvironmentHasRepoInstance(Relationship):

    _entity_def = \
        {'name': 'environment_has_repo_instance', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.environment', 'ref_to': 'hmd_lang_deployment.repo_instance', 'attributes': {}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '1'}, 'ref_to': {'arrow': True, 'cardinality': '*'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return EnvironmentHasRepoInstance._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(EnvironmentHasRepoInstance._entity_def)


    @staticmethod
    def ref_from_type():
        return Environment

    @staticmethod
    def ref_to_type():
        return RepoInstance

    

    