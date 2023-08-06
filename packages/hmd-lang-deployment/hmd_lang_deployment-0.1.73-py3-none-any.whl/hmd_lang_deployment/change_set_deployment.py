

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class ChangeSetDeployment(Noun):

    _entity_def = \
        {'name': 'change_set_deployment', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'deployment_set_name': {'type': 'string', 'required': False, 'description': 'The name of the DeploymentSet to which the deployment was done.'}, 'deployment_set_definition': {'type': 'collection', 'description': 'The contents of the DeploymentSet when the deployment occurred.', 'required': True, 'schema': {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'http://hmd_lang_deployment/change_set', 'title': 'definition', 'type': 'array', 'items': {'type': 'object', 'properties': {'environment': {'type': 'string'}, 'deployment_gate': {'type': 'object', 'properties': {'transforms': {'type': 'array', 'items': {'type': 'object', 'properties': {'apply_to': {'type': 'string'}, 'transform': {'type': 'object', 'properties': {'image_name': {'type': 'string'}, 'tag': {'type': 'string'}}, 'required': ['image_name', 'tag'], 'additionalProperties': False}, 'artifact_ref': {'type': 'string', 'required': ['artifact_ref'], 'additionalProperties': False}}, 'required': ['apply_to', 'transform'], 'additionalProperties': False}}, 'approval': {'type': 'boolean'}}, 'required': ['transforms', 'approval']}}, 'required': ['environment', 'deployment_gate'], 'additionalProperties': False}}}, 'csd_status': {'type': 'enum', 'enum_def': ['CREATED', 'STARTED', 'COMPLETED', 'FAILED', 'DESTROYED']}, 'deploy_time': {'type': 'timestamp', 'description': 'The time that the ChangeSet was deployed.', 'required': True}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ChangeSetDeployment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ChangeSetDeployment._entity_def)


    

    
        
    @property
    def deployment_set_name(self) -> str:
        return self._getter("deployment_set_name")

    @deployment_set_name.setter
    def deployment_set_name(self, value: str) -> None:
        self._setter("deployment_set_name", value)
    
        
    @property
    def deployment_set_definition(self) -> List:
        return self._getter("deployment_set_definition")

    @deployment_set_definition.setter
    def deployment_set_definition(self, value: List) -> None:
        self._setter("deployment_set_definition", value)
    
        
    @property
    def csd_status(self) -> str:
        return self._getter("csd_status")

    @csd_status.setter
    def csd_status(self, value: str) -> None:
        self._setter("csd_status", value)
    
        
    @property
    def deploy_time(self) -> datetime:
        return self._getter("deploy_time")

    @deploy_time.setter
    def deploy_time(self, value: datetime) -> None:
        self._setter("deploy_time", value)
    

    
    
        
    def get_from_change_set_deployment_has_change_set_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.change_set_deployment_has_change_set"]
    
        
    def get_from_change_set_deployment_has_change_set_env_deployment_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.change_set_deployment_has_change_set_env_deployment"]
    
        
    def get_from_change_set_deployment_has_deployment_set_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.change_set_deployment_has_deployment_set"]
    