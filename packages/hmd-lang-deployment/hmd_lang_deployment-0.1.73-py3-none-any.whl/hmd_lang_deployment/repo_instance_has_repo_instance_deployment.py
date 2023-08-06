

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.repo_instance import RepoInstance
from hmd_lang_deployment.repo_instance_deployment import RepoInstanceDeployment
from datetime import datetime
from typing import List, Dict, Any

class RepoInstanceHasRepoInstanceDeployment(Relationship):

    _entity_def = \
        {'name': 'repo_instance_has_repo_instance_deployment', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.repo_instance', 'ref_to': 'hmd_lang_deployment.repo_instance_deployment', 'attributes': {'current': {'type': 'string', 'description': 'Contains a value of "true" if this is the current deployment', 'required': True}}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '1'}, 'ref_to': {'arrow': True, 'cardinality': '*'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoInstanceHasRepoInstanceDeployment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoInstanceHasRepoInstanceDeployment._entity_def)


    @staticmethod
    def ref_from_type():
        return RepoInstance

    @staticmethod
    def ref_to_type():
        return RepoInstanceDeployment

    
        
    @property
    def current(self) -> str:
        return self._getter("current")

    @current.setter
    def current(self, value: str) -> None:
        self._setter("current", value)
    

    