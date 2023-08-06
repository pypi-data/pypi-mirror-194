

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.repo_instance import RepoInstance
from hmd_lang_deployment.repo_class import RepoClass
from datetime import datetime
from typing import List, Dict, Any

class RepoInstanceIsaRepoClass(Relationship):

    _entity_def = \
        {'name': 'repo_instance_isa_repo_class', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.repo_instance', 'ref_to': 'hmd_lang_deployment.repo_class', 'attributes': {'version': {'type': 'string', 'required': False, 'description': 'The version of the repo class the repo instance refers to.'}}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '*'}, 'ref_to': {'arrow': True, 'cardinality': '1'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoInstanceIsaRepoClass._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoInstanceIsaRepoClass._entity_def)


    @staticmethod
    def ref_from_type():
        return RepoInstance

    @staticmethod
    def ref_to_type():
        return RepoClass

    
        
    @property
    def version(self) -> str:
        return self._getter("version")

    @version.setter
    def version(self, value: str) -> None:
        self._setter("version", value)
    

    