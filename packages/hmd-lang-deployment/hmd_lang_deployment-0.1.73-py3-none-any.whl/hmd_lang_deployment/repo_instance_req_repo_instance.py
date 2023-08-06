

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.repo_instance import RepoInstance
from hmd_lang_deployment.repo_instance import RepoInstance
from datetime import datetime
from typing import List, Dict, Any

class RepoInstanceReqRepoInstance(Relationship):

    _entity_def = \
        {'name': 'repo_instance_req_repo_instance', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.repo_instance', 'ref_to': 'hmd_lang_deployment.repo_instance', 'attributes': {'role': {'description': 'The role the referenced repo_class assumes relative to the referring repo_class.', 'type': 'string', 'required': True}}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '1'}, 'ref_to': {'arrow': True, 'cardinality': '0..*'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoInstanceReqRepoInstance._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoInstanceReqRepoInstance._entity_def)


    @staticmethod
    def ref_from_type():
        return RepoInstance

    @staticmethod
    def ref_to_type():
        return RepoInstance

    
        
    @property
    def role(self) -> str:
        return self._getter("role")

    @role.setter
    def role(self, value: str) -> None:
        self._setter("role", value)
    

    