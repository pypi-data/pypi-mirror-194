

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class ChangeSet(Noun):

    _entity_def = \
        {'name': 'change_set', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'name': {'type': 'string', 'description': 'The name of the test set.', 'required': True, 'business_id': True}, 'definition': {'type': 'collection', 'description': 'The contents of the change set.', 'required': True, 'schema': {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'http://hmd_lang_deployment/change_set', 'title': 'definition', 'type': 'array', 'items': {'type': 'object', 'oneOf': [{'properties': {'deployment_id': {'type': 'string'}, 'hmd_region': {'type': 'string'}, 'repo_instance_name': {'type': 'string'}, 'repo_class_name': {'type': 'string'}, 'repo_class_version': {'type': 'string'}, 'auto_deploy': {'type': 'string'}, 'image_only': {'const': True}}, 'required': ['deployment_id', 'repo_instance_name', 'repo_class_name', 'repo_class_version', 'image_only'], 'additionalProperties': False}, {'properties': {'deployment_id': {'type': 'string'}, 'hmd_region': {'type': 'string'}, 'repo_instance_name': {'type': 'string'}, 'repo_class_name': {'type': 'string'}, 'repo_class_version': {'type': 'string'}, 'auto_deploy': {'type': 'string'}, 'config_spec': {'type': 'string'}}, 'required': ['deployment_id', 'repo_instance_name', 'repo_class_name', 'repo_class_version', 'config_spec'], 'additionalProperties': False}, {'properties': {'deployment_id': {'type': 'string'}, 'hmd_region': {'type': 'string'}, 'repo_instance_name': {'type': 'string'}, 'repo_class_name': {'type': 'string'}, 'repo_class_version': {'type': 'string'}, 'auto_deploy': {'type': 'string'}, 'instance_configuration': {'type': 'object'}, 'dependencies': {'type': 'object', 'patternProperties': {'.*': {'anyOf': [{'type': 'string'}, {'type': 'array', 'items': {'type': 'string'}}]}}}}, 'required': ['deployment_id', 'repo_instance_name', 'repo_class_name', 'repo_class_version', 'instance_configuration', 'dependencies'], 'additionalProperties': False}]}}}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ChangeSet._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ChangeSet._entity_def)


    

    
        
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
    

    
        
    def get_to_change_set_deployment_has_change_set_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.change_set_deployment_has_change_set"]
    
    