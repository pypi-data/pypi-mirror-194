

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.repo_class_version import RepoClassVersion
from hmd_lang_deployment.external_artifact import ExternalArtifact
from datetime import datetime
from typing import List, Dict, Any

class RepoClassVersionHasExternalArtifact(Relationship):

    _entity_def = \
        {'name': 'repo_class_version_has_external_artifact', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.repo_class_version', 'ref_to': 'hmd_lang_deployment.external_artifact', 'attributes': {}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoClassVersionHasExternalArtifact._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoClassVersionHasExternalArtifact._entity_def)


    @staticmethod
    def ref_from_type():
        return RepoClassVersion

    @staticmethod
    def ref_to_type():
        return ExternalArtifact

    

    