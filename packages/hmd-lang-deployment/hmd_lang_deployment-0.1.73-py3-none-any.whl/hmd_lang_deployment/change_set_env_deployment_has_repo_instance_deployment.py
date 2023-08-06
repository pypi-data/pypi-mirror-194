

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.change_set_env_deployment import ChangeSetEnvDeployment
from hmd_lang_deployment.repo_instance_deployment import RepoInstanceDeployment
from datetime import datetime
from typing import List, Dict, Any

class ChangeSetEnvDeploymentHasRepoInstanceDeployment(Relationship):

    _entity_def = \
        {'name': 'change_set_env_deployment_has_repo_instance_deployment', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.change_set_env_deployment', 'ref_to': 'hmd_lang_deployment.repo_instance_deployment', 'attributes': {}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '1'}, 'ref_to': {'arrow': True, 'cardinality': '*'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ChangeSetEnvDeploymentHasRepoInstanceDeployment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ChangeSetEnvDeploymentHasRepoInstanceDeployment._entity_def)


    @staticmethod
    def ref_from_type():
        return ChangeSetEnvDeployment

    @staticmethod
    def ref_to_type():
        return RepoInstanceDeployment

    

    