

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class ExternalArtifact(Noun):

    _entity_def = \
        {'name': 'external_artifact', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'name': {'type': 'string', 'description': 'the name of the artifact', 'required': True}, 'tool': {'type': 'string', 'description': 'the CLI tool used to create the artifact', 'required': True}, 'external_location': {'type': 'string', 'description': 'location of external registry', 'required': True}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ExternalArtifact._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ExternalArtifact._entity_def)


    

    
        
    @property
    def name(self) -> str:
        return self._getter("name")

    @name.setter
    def name(self, value: str) -> None:
        self._setter("name", value)
    
        
    @property
    def tool(self) -> str:
        return self._getter("tool")

    @tool.setter
    def tool(self, value: str) -> None:
        self._setter("tool", value)
    
        
    @property
    def external_location(self) -> str:
        return self._getter("external_location")

    @external_location.setter
    def external_location(self, value: str) -> None:
        self._setter("external_location", value)
    

    
        
    def get_to_repo_class_version_has_external_artifact_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.repo_class_version_has_external_artifact"]
    
    