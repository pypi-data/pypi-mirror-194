

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.change_set_deployment import ChangeSetDeployment
from hmd_lang_deployment.change_set_env_deployment import ChangeSetEnvDeployment
from datetime import datetime
from typing import List, Dict, Any

class ChangeSetDeploymentHasChangeSetEnvDeployment(Relationship):

    _entity_def = \
        {'name': 'change_set_deployment_has_change_set_env_deployment', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.change_set_deployment', 'ref_to': 'hmd_lang_deployment.change_set_env_deployment', 'attributes': {'order': {'type': 'integer', 'description': 'The order of the env deployment relative to the deployment.', 'required': True}}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '1'}, 'ref_to': {'arrow': True, 'cardinality': 'ordered\\n*'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ChangeSetDeploymentHasChangeSetEnvDeployment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ChangeSetDeploymentHasChangeSetEnvDeployment._entity_def)


    @staticmethod
    def ref_from_type():
        return ChangeSetDeployment

    @staticmethod
    def ref_to_type():
        return ChangeSetEnvDeployment

    
        
    @property
    def order(self) -> int:
        return self._getter("order")

    @order.setter
    def order(self, value: int) -> None:
        self._setter("order", value)
    

    