

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.repo_class import RepoClass
from hmd_lang_deployment.repo_class_version import RepoClassVersion
from datetime import datetime
from typing import List, Dict, Any

class RepoClassHasRepoClassVersion(Relationship):

    _entity_def = \
        {'name': 'repo_class_has_repo_class_version', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.repo_class', 'ref_to': 'hmd_lang_deployment.repo_class_version', 'attributes': {}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '1'}, 'ref_to': {'arrow': True, 'cardinality': '*'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoClassHasRepoClassVersion._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoClassHasRepoClassVersion._entity_def)


    @staticmethod
    def ref_from_type():
        return RepoClass

    @staticmethod
    def ref_to_type():
        return RepoClassVersion

    

    