

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.repo_class_version import RepoClassVersion
from hmd_lang_deployment.repo_class_version_notes import RepoClassVersionNotes
from datetime import datetime
from typing import List, Dict, Any

class RepoClassVersionHasRepoClassVersionNotes(Relationship):

    _entity_def = \
        {'name': 'repo_class_version_has_repo_class_version_notes', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.repo_class_version', 'ref_to': 'hmd_lang_deployment.repo_class_version_notes', 'attributes': {}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '1'}, 'ref_to': {'arrow': True, 'cardinality': '0..1'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoClassVersionHasRepoClassVersionNotes._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoClassVersionHasRepoClassVersionNotes._entity_def)


    @staticmethod
    def ref_from_type():
        return RepoClassVersion

    @staticmethod
    def ref_to_type():
        return RepoClassVersionNotes

    

    