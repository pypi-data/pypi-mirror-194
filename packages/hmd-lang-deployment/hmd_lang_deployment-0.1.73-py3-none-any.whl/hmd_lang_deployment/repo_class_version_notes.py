

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class RepoClassVersionNotes(Noun):

    _entity_def = \
        {'name': 'repo_class_version_notes', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'version_notes': {'type': 'string', 'description': 'release notes for the version', 'required': True}, 'requirement_identifiers': {'type': 'collection', 'description': 'a list of identifiers for related requirements records', 'required': False}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoClassVersionNotes._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoClassVersionNotes._entity_def)


    

    
        
    @property
    def version_notes(self) -> str:
        return self._getter("version_notes")

    @version_notes.setter
    def version_notes(self, value: str) -> None:
        self._setter("version_notes", value)
    
        
    @property
    def requirement_identifiers(self) -> List:
        return self._getter("requirement_identifiers")

    @requirement_identifiers.setter
    def requirement_identifiers(self, value: List) -> None:
        self._setter("requirement_identifiers", value)
    

    
        
    def get_to_repo_class_version_has_repo_class_version_notes_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.repo_class_version_has_repo_class_version_notes"]
    
    