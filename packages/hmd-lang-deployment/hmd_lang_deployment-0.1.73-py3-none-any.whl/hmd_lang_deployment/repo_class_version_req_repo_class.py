

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.repo_class_version import RepoClassVersion
from hmd_lang_deployment.repo_class import RepoClass
from datetime import datetime
from typing import List, Dict, Any

class RepoClassVersionReqRepoClass(Relationship):

    _entity_def = \
        {'name': 'repo_class_version_req_repo_class', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.repo_class_version', 'ref_to': 'hmd_lang_deployment.repo_class', 'attributes': {'required': {'description': 'flag indicating that the repo class dependency is required', 'type': 'string', 'required': False}, 'version_spec': {'description': 'A specification of the acceptable version of the repo class to which the relationship points.', 'type': 'string', 'required': False}, 'role': {'description': 'The role the target repo class plays relative to the origin repo class.', 'type': 'string', 'required': False}}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '*'}, 'ref_to': {'arrow': True, 'cardinality': '0..*'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoClassVersionReqRepoClass._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoClassVersionReqRepoClass._entity_def)


    @staticmethod
    def ref_from_type():
        return RepoClassVersion

    @staticmethod
    def ref_to_type():
        return RepoClass

    
        
    @property
    def required(self) -> str:
        return self._getter("required")

    @required.setter
    def required(self, value: str) -> None:
        self._setter("required", value)
    
        
    @property
    def version_spec(self) -> str:
        return self._getter("version_spec")

    @version_spec.setter
    def version_spec(self, value: str) -> None:
        self._setter("version_spec", value)
    
        
    @property
    def role(self) -> str:
        return self._getter("role")

    @role.setter
    def role(self, value: str) -> None:
        self._setter("role", value)
    

    