

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class DeploymentSet(Noun):

    _entity_def = \
        {'name': 'deployment_set', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'name': {'type': 'string', 'description': 'The name of the DeploymentSet', 'required': True}, 'definition': {'type': 'collection', 'description': 'The contents of the DeploymentSet when the deployment occurred.', 'required': True, 'schema': {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'http://hmd_lang_deployment/change_set', 'title': 'definition', 'type': 'array', 'items': {'type': 'object', 'properties': {'environment': {'type': 'string'}, 'deployment_gate': {'type': 'object', 'properties': {'transforms': {'type': 'array', 'items': {'type': 'object', 'properties': {'apply_to': {'type': 'string'}, 'transform': {'type': 'object', 'properties': {'image_name': {'type': 'string'}, 'tag': {'type': 'string'}}, 'required': ['image_name', 'tag'], 'additionalProperties': False}, 'artifact_ref': {'type': 'string', 'required': ['artifact_ref'], 'additionalProperties': False}}, 'required': ['apply_to', 'transform'], 'additionalProperties': False}}, 'approval': {'type': 'boolean'}}, 'required': ['transforms', 'approval']}}, 'required': ['environment', 'deployment_gate'], 'additionalProperties': False}}}, 'auto_deploy': {'type': 'string', 'description': 'A flag indicating whether auto-deploy is supported by the deployment set. Expects ["true","false"]'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return DeploymentSet._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(DeploymentSet._entity_def)


    

    
        
    @property
    def name(self) -> str:
        return self._getter("name")

    @name.setter
    def name(self, value: str) -> None:
        self._setter("name", value)
    
        
    @property
    def definition(self) -> List:
        return self._getter("definition")

    @definition.setter
    def definition(self, value: List) -> None:
        self._setter("definition", value)
    
        
    @property
    def auto_deploy(self) -> str:
        return self._getter("auto_deploy")

    @auto_deploy.setter
    def auto_deploy(self, value: str) -> None:
        self._setter("auto_deploy", value)
    

    
        
    def get_to_change_set_deployment_has_deployment_set_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.change_set_deployment_has_deployment_set"]
    
    