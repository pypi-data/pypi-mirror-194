

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_deployment.change_set_deployment import ChangeSetDeployment
from hmd_lang_deployment.change_set import ChangeSet
from datetime import datetime
from typing import List, Dict, Any

class ChangeSetDeploymentHasChangeSet(Relationship):

    _entity_def = \
        {'name': 'change_set_deployment_has_change_set', 'namespace': 'hmd_lang_deployment', 'metatype': 'relationship', 'ref_from': 'hmd_lang_deployment.change_set_deployment', 'ref_to': 'hmd_lang_deployment.change_set', 'attributes': {}, 'adornments': {'ref_from': {'arrow': False, 'cardinality': '1'}, 'ref_to': {'arrow': True, 'cardinality': '1'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ChangeSetDeploymentHasChangeSet._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ChangeSetDeploymentHasChangeSet._entity_def)


    @staticmethod
    def ref_from_type():
        return ChangeSetDeployment

    @staticmethod
    def ref_to_type():
        return ChangeSet

    

    