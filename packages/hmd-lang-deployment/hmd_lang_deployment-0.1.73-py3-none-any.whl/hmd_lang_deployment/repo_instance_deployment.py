

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class RepoInstanceDeployment(Noun):

    _entity_def = \
        {'name': 'repo_instance_deployment', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'attributes': {'hmd_region': {'type': 'string', 'description': 'an hmd region identifier if different from the default', 'required': False}, 'deployment_id': {'type': 'string', 'description': 'The deployment id.', 'required': True, 'business_id': True}, 'instance_configuration': {'type': 'mapping', 'description': 'The instance configuration used for this deployment.', 'required': False}, 'config_artifact_spec': {'type': 'string', 'description': 'The configuration artifact ref used.', 'required': False}, 'status': {'type': 'enum', 'description': 'The status of the instance deployment.', 'required': False, 'enum_def': ['NOT_DEPLOYED', 'DEPLOYED', 'DEPLOY_NEXT', 'DESTROY_NEXT', 'DESTROYED', 'FAILED', 'SKIPPED']}, 'start': {'type': 'timestamp', 'description': 'The time the deployment was done.', 'required': False}, 'end': {'type': 'timestamp', 'description': 'The time the deployment was removed or a new version was deployed.', 'required': False}, 'image_only': {'type': 'string', 'description': 'Present if the instance deployment is for the docker image only.', 'required': False}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return RepoInstanceDeployment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(RepoInstanceDeployment._entity_def)


    

    
        
    @property
    def hmd_region(self) -> str:
        return self._getter("hmd_region")

    @hmd_region.setter
    def hmd_region(self, value: str) -> None:
        self._setter("hmd_region", value)
    
        
    @property
    def deployment_id(self) -> str:
        return self._getter("deployment_id")

    @deployment_id.setter
    def deployment_id(self, value: str) -> None:
        self._setter("deployment_id", value)
    
        
    @property
    def instance_configuration(self) -> Dict:
        return self._getter("instance_configuration")

    @instance_configuration.setter
    def instance_configuration(self, value: Dict) -> None:
        self._setter("instance_configuration", value)
    
        
    @property
    def config_artifact_spec(self) -> str:
        return self._getter("config_artifact_spec")

    @config_artifact_spec.setter
    def config_artifact_spec(self, value: str) -> None:
        self._setter("config_artifact_spec", value)
    
        
    @property
    def status(self) -> str:
        return self._getter("status")

    @status.setter
    def status(self, value: str) -> None:
        self._setter("status", value)
    
        
    @property
    def start(self) -> datetime:
        return self._getter("start")

    @start.setter
    def start(self, value: datetime) -> None:
        self._setter("start", value)
    
        
    @property
    def end(self) -> datetime:
        return self._getter("end")

    @end.setter
    def end(self, value: datetime) -> None:
        self._setter("end", value)
    
        
    @property
    def image_only(self) -> str:
        return self._getter("image_only")

    @image_only.setter
    def image_only(self, value: str) -> None:
        self._setter("image_only", value)
    

    
        
    def get_to_change_set_env_deployment_has_repo_instance_deployment_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.change_set_env_deployment_has_repo_instance_deployment"]
    
        
    def get_to_repo_instance_has_repo_instance_deployment_hmd_lang_deployment(self):
        return self.to_rels["hmd_lang_deployment.repo_instance_has_repo_instance_deployment"]
    
    
        
    def get_from_repo_instance_deployment_has_repo_class_version_hmd_lang_deployment(self):
        return self.from_rels["hmd_lang_deployment.repo_instance_deployment_has_repo_class_version"]
    