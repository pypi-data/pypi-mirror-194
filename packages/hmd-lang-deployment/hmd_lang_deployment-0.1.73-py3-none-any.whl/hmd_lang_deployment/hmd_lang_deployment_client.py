# The code in this file is generated automatically.
# DO NOT EDIT!
from hmd_graphql_client.hmd_base_client import BaseClient
from typing import List
from hmd_schema_loader.hmd_schema_loader import get_default_loader, get_schema_root


from .change_set import ChangeSet
from .change_set_deployment import ChangeSetDeployment
from .change_set_env_deployment import ChangeSetEnvDeployment
from .deployment_set import DeploymentSet
from .environment import Environment
from .environment_action import EnvironmentAction
from .environment_action_execution import EnvironmentActionExecution
from .environment_action_version import EnvironmentActionVersion
from .external_artifact import ExternalArtifact
from .repo_class import RepoClass
from .repo_class_version import RepoClassVersion
from .repo_class_version_notes import RepoClassVersionNotes
from .repo_instance import RepoInstance
from .repo_instance_deployment import RepoInstanceDeployment
from .timestamp_record import TimestampRecord



from .change_set_deployment_has_change_set import ChangeSetDeploymentHasChangeSet


from .change_set_deployment_has_change_set_env_deployment import ChangeSetDeploymentHasChangeSetEnvDeployment


from .change_set_deployment_has_deployment_set import ChangeSetDeploymentHasDeploymentSet


from .change_set_env_deployment_has_environment import ChangeSetEnvDeploymentHasEnvironment


from .change_set_env_deployment_has_environment_action_execution import ChangeSetEnvDeploymentHasEnvironmentActionExecution


from .change_set_env_deployment_has_repo_instance_deployment import ChangeSetEnvDeploymentHasRepoInstanceDeployment


from .environment_action_execution_has_environment_action_version import EnvironmentActionExecutionHasEnvironmentActionVersion


from .environment_action_has_environment_action_version import EnvironmentActionHasEnvironmentActionVersion


from .environment_has_repo_instance import EnvironmentHasRepoInstance


from .repo_class_has_repo_class_version import RepoClassHasRepoClassVersion


from .repo_class_version_has_external_artifact import RepoClassVersionHasExternalArtifact


from .repo_class_version_has_repo_class_version_notes import RepoClassVersionHasRepoClassVersionNotes


from .repo_class_version_req_repo_class import RepoClassVersionReqRepoClass


from .repo_instance_deployment_has_repo_class_version import RepoInstanceDeploymentHasRepoClassVersion


from .repo_instance_has_repo_instance_deployment import RepoInstanceHasRepoInstanceDeployment


from .repo_instance_isa_repo_class import RepoInstanceIsaRepoClass


from .repo_instance_req_repo_instance import RepoInstanceReqRepoInstance

def get_client_loader():
    return get_default_loader("hmd_lang_deployment")

def get_client_schema_root():
    return get_schema_root("hmd_lang_deployment")

class HmdLangDeploymentClient:
    def __init__(self, base_client: BaseClient):
        self._base_client = base_client

    # Generic upsert...
    def upsert(self, entity):
        return self._base_client.upsert_entity(entity)

    # Generic delete...
    def delete(self, entity):
        self._base_client.delete_entity(entity.get_namespace_name(), entity.identifier)

    # Nouns...

    # hmd_lang_deployment_change_set
    def get_change_set_hmd_lang_deployment(self, id_: str) -> ChangeSet:
        return self._base_client.get_entity(ChangeSet.get_namespace_name(), id_)

    def delete_change_set_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSet.get_namespace_name(), id_)

    def upsert_change_set_hmd_lang_deployment(self, entity: ChangeSet) -> ChangeSet:
        if not isinstance(entity, ChangeSet):
            raise Exception("entity must be an instance of ChangeSet")
        return self._base_client.upsert_entity(entity)

    
    def search_change_set_hmd_lang_deployment(self, filter_: dict) -> List[ChangeSet]:
        return self._base_client.search_entity(ChangeSet.get_namespace_name(), filter_)

    # hmd_lang_deployment_change_set_deployment
    def get_change_set_deployment_hmd_lang_deployment(self, id_: str) -> ChangeSetDeployment:
        return self._base_client.get_entity(ChangeSetDeployment.get_namespace_name(), id_)

    def delete_change_set_deployment_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSetDeployment.get_namespace_name(), id_)

    def upsert_change_set_deployment_hmd_lang_deployment(self, entity: ChangeSetDeployment) -> ChangeSetDeployment:
        if not isinstance(entity, ChangeSetDeployment):
            raise Exception("entity must be an instance of ChangeSetDeployment")
        return self._base_client.upsert_entity(entity)

    
    def search_change_set_deployment_hmd_lang_deployment(self, filter_: dict) -> List[ChangeSetDeployment]:
        return self._base_client.search_entity(ChangeSetDeployment.get_namespace_name(), filter_)

    # hmd_lang_deployment_change_set_env_deployment
    def get_change_set_env_deployment_hmd_lang_deployment(self, id_: str) -> ChangeSetEnvDeployment:
        return self._base_client.get_entity(ChangeSetEnvDeployment.get_namespace_name(), id_)

    def delete_change_set_env_deployment_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSetEnvDeployment.get_namespace_name(), id_)

    def upsert_change_set_env_deployment_hmd_lang_deployment(self, entity: ChangeSetEnvDeployment) -> ChangeSetEnvDeployment:
        if not isinstance(entity, ChangeSetEnvDeployment):
            raise Exception("entity must be an instance of ChangeSetEnvDeployment")
        return self._base_client.upsert_entity(entity)

    
    def search_change_set_env_deployment_hmd_lang_deployment(self, filter_: dict) -> List[ChangeSetEnvDeployment]:
        return self._base_client.search_entity(ChangeSetEnvDeployment.get_namespace_name(), filter_)

    # hmd_lang_deployment_deployment_set
    def get_deployment_set_hmd_lang_deployment(self, id_: str) -> DeploymentSet:
        return self._base_client.get_entity(DeploymentSet.get_namespace_name(), id_)

    def delete_deployment_set_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(DeploymentSet.get_namespace_name(), id_)

    def upsert_deployment_set_hmd_lang_deployment(self, entity: DeploymentSet) -> DeploymentSet:
        if not isinstance(entity, DeploymentSet):
            raise Exception("entity must be an instance of DeploymentSet")
        return self._base_client.upsert_entity(entity)

    
    def search_deployment_set_hmd_lang_deployment(self, filter_: dict) -> List[DeploymentSet]:
        return self._base_client.search_entity(DeploymentSet.get_namespace_name(), filter_)

    # hmd_lang_deployment_environment
    def get_environment_hmd_lang_deployment(self, id_: str) -> Environment:
        return self._base_client.get_entity(Environment.get_namespace_name(), id_)

    def delete_environment_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(Environment.get_namespace_name(), id_)

    def upsert_environment_hmd_lang_deployment(self, entity: Environment) -> Environment:
        if not isinstance(entity, Environment):
            raise Exception("entity must be an instance of Environment")
        return self._base_client.upsert_entity(entity)

    
    def search_environment_hmd_lang_deployment(self, filter_: dict) -> List[Environment]:
        return self._base_client.search_entity(Environment.get_namespace_name(), filter_)

    # hmd_lang_deployment_environment_action
    def get_environment_action_hmd_lang_deployment(self, id_: str) -> EnvironmentAction:
        return self._base_client.get_entity(EnvironmentAction.get_namespace_name(), id_)

    def delete_environment_action_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(EnvironmentAction.get_namespace_name(), id_)

    def upsert_environment_action_hmd_lang_deployment(self, entity: EnvironmentAction) -> EnvironmentAction:
        if not isinstance(entity, EnvironmentAction):
            raise Exception("entity must be an instance of EnvironmentAction")
        return self._base_client.upsert_entity(entity)

    
    def search_environment_action_hmd_lang_deployment(self, filter_: dict) -> List[EnvironmentAction]:
        return self._base_client.search_entity(EnvironmentAction.get_namespace_name(), filter_)

    # hmd_lang_deployment_environment_action_execution
    def get_environment_action_execution_hmd_lang_deployment(self, id_: str) -> EnvironmentActionExecution:
        return self._base_client.get_entity(EnvironmentActionExecution.get_namespace_name(), id_)

    def delete_environment_action_execution_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(EnvironmentActionExecution.get_namespace_name(), id_)

    def upsert_environment_action_execution_hmd_lang_deployment(self, entity: EnvironmentActionExecution) -> EnvironmentActionExecution:
        if not isinstance(entity, EnvironmentActionExecution):
            raise Exception("entity must be an instance of EnvironmentActionExecution")
        return self._base_client.upsert_entity(entity)

    
    def search_environment_action_execution_hmd_lang_deployment(self, filter_: dict) -> List[EnvironmentActionExecution]:
        return self._base_client.search_entity(EnvironmentActionExecution.get_namespace_name(), filter_)

    # hmd_lang_deployment_environment_action_version
    def get_environment_action_version_hmd_lang_deployment(self, id_: str) -> EnvironmentActionVersion:
        return self._base_client.get_entity(EnvironmentActionVersion.get_namespace_name(), id_)

    def delete_environment_action_version_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(EnvironmentActionVersion.get_namespace_name(), id_)

    def upsert_environment_action_version_hmd_lang_deployment(self, entity: EnvironmentActionVersion) -> EnvironmentActionVersion:
        if not isinstance(entity, EnvironmentActionVersion):
            raise Exception("entity must be an instance of EnvironmentActionVersion")
        return self._base_client.upsert_entity(entity)

    
    def search_environment_action_version_hmd_lang_deployment(self, filter_: dict) -> List[EnvironmentActionVersion]:
        return self._base_client.search_entity(EnvironmentActionVersion.get_namespace_name(), filter_)

    # hmd_lang_deployment_external_artifact
    def get_external_artifact_hmd_lang_deployment(self, id_: str) -> ExternalArtifact:
        return self._base_client.get_entity(ExternalArtifact.get_namespace_name(), id_)

    def delete_external_artifact_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ExternalArtifact.get_namespace_name(), id_)

    def upsert_external_artifact_hmd_lang_deployment(self, entity: ExternalArtifact) -> ExternalArtifact:
        if not isinstance(entity, ExternalArtifact):
            raise Exception("entity must be an instance of ExternalArtifact")
        return self._base_client.upsert_entity(entity)

    
    def search_external_artifact_hmd_lang_deployment(self, filter_: dict) -> List[ExternalArtifact]:
        return self._base_client.search_entity(ExternalArtifact.get_namespace_name(), filter_)

    # hmd_lang_deployment_repo_class
    def get_repo_class_hmd_lang_deployment(self, id_: str) -> RepoClass:
        return self._base_client.get_entity(RepoClass.get_namespace_name(), id_)

    def delete_repo_class_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoClass.get_namespace_name(), id_)

    def upsert_repo_class_hmd_lang_deployment(self, entity: RepoClass) -> RepoClass:
        if not isinstance(entity, RepoClass):
            raise Exception("entity must be an instance of RepoClass")
        return self._base_client.upsert_entity(entity)

    
    def search_repo_class_hmd_lang_deployment(self, filter_: dict) -> List[RepoClass]:
        return self._base_client.search_entity(RepoClass.get_namespace_name(), filter_)

    # hmd_lang_deployment_repo_class_version
    def get_repo_class_version_hmd_lang_deployment(self, id_: str) -> RepoClassVersion:
        return self._base_client.get_entity(RepoClassVersion.get_namespace_name(), id_)

    def delete_repo_class_version_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoClassVersion.get_namespace_name(), id_)

    def upsert_repo_class_version_hmd_lang_deployment(self, entity: RepoClassVersion) -> RepoClassVersion:
        if not isinstance(entity, RepoClassVersion):
            raise Exception("entity must be an instance of RepoClassVersion")
        return self._base_client.upsert_entity(entity)

    
    def search_repo_class_version_hmd_lang_deployment(self, filter_: dict) -> List[RepoClassVersion]:
        return self._base_client.search_entity(RepoClassVersion.get_namespace_name(), filter_)

    # hmd_lang_deployment_repo_class_version_notes
    def get_repo_class_version_notes_hmd_lang_deployment(self, id_: str) -> RepoClassVersionNotes:
        return self._base_client.get_entity(RepoClassVersionNotes.get_namespace_name(), id_)

    def delete_repo_class_version_notes_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoClassVersionNotes.get_namespace_name(), id_)

    def upsert_repo_class_version_notes_hmd_lang_deployment(self, entity: RepoClassVersionNotes) -> RepoClassVersionNotes:
        if not isinstance(entity, RepoClassVersionNotes):
            raise Exception("entity must be an instance of RepoClassVersionNotes")
        return self._base_client.upsert_entity(entity)

    
    def search_repo_class_version_notes_hmd_lang_deployment(self, filter_: dict) -> List[RepoClassVersionNotes]:
        return self._base_client.search_entity(RepoClassVersionNotes.get_namespace_name(), filter_)

    # hmd_lang_deployment_repo_instance
    def get_repo_instance_hmd_lang_deployment(self, id_: str) -> RepoInstance:
        return self._base_client.get_entity(RepoInstance.get_namespace_name(), id_)

    def delete_repo_instance_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoInstance.get_namespace_name(), id_)

    def upsert_repo_instance_hmd_lang_deployment(self, entity: RepoInstance) -> RepoInstance:
        if not isinstance(entity, RepoInstance):
            raise Exception("entity must be an instance of RepoInstance")
        return self._base_client.upsert_entity(entity)

    
    def search_repo_instance_hmd_lang_deployment(self, filter_: dict) -> List[RepoInstance]:
        return self._base_client.search_entity(RepoInstance.get_namespace_name(), filter_)

    # hmd_lang_deployment_repo_instance_deployment
    def get_repo_instance_deployment_hmd_lang_deployment(self, id_: str) -> RepoInstanceDeployment:
        return self._base_client.get_entity(RepoInstanceDeployment.get_namespace_name(), id_)

    def delete_repo_instance_deployment_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoInstanceDeployment.get_namespace_name(), id_)

    def upsert_repo_instance_deployment_hmd_lang_deployment(self, entity: RepoInstanceDeployment) -> RepoInstanceDeployment:
        if not isinstance(entity, RepoInstanceDeployment):
            raise Exception("entity must be an instance of RepoInstanceDeployment")
        return self._base_client.upsert_entity(entity)

    
    def search_repo_instance_deployment_hmd_lang_deployment(self, filter_: dict) -> List[RepoInstanceDeployment]:
        return self._base_client.search_entity(RepoInstanceDeployment.get_namespace_name(), filter_)

    # hmd_lang_deployment_timestamp_record
    def get_timestamp_record_hmd_lang_deployment(self, id_: str) -> TimestampRecord:
        return self._base_client.get_entity(TimestampRecord.get_namespace_name(), id_)

    def delete_timestamp_record_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(TimestampRecord.get_namespace_name(), id_)

    def upsert_timestamp_record_hmd_lang_deployment(self, entity: TimestampRecord) -> TimestampRecord:
        if not isinstance(entity, TimestampRecord):
            raise Exception("entity must be an instance of TimestampRecord")
        return self._base_client.upsert_entity(entity)

    
    def search_timestamp_record_hmd_lang_deployment(self, filter_: dict) -> List[TimestampRecord]:
        return self._base_client.search_entity(TimestampRecord.get_namespace_name(), filter_)


    # Relationships...

    # hmd_lang_deployment_change_set_deployment_has_change_set
    def delete_change_set_deployment_has_change_set_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSetDeploymentHasChangeSet.get_namespace_name(), id_)

    def upsert_change_set_deployment_has_change_set_hmd_lang_deployment(self, entity: ChangeSetDeploymentHasChangeSet) -> ChangeSetDeploymentHasChangeSet:
        if not isinstance(entity, ChangeSetDeploymentHasChangeSet):
            raise Exception("entity must be an instance of ChangeSetDeploymentHasChangeSet")
        return self._base_client.upsert_entity(entity)

    def get_from_change_set_deployment_has_change_set_hmd_lang_deployment(self, entity: ChangeSetDeployment) -> List[ChangeSetDeploymentHasChangeSet]:
        if not isinstance(entity, ChangeSetDeployment):
            raise Exception("entity must be an instance of ChangeSetDeployment")
        return self._base_client.get_relationships_from(entity, ChangeSetDeploymentHasChangeSet.get_namespace_name())

    def get_to_change_set_deployment_has_change_set_hmd_lang_deployment(self, entity: ChangeSet) -> List[ChangeSetDeploymentHasChangeSet]:
        if not isinstance(entity, ChangeSet):
            raise Exception("entity must be an instance of ChangeSet")
        return self._base_client.get_relationships_to(entity, ChangeSetDeploymentHasChangeSet.get_namespace_name())



    # hmd_lang_deployment_change_set_deployment_has_change_set_env_deployment
    def delete_change_set_deployment_has_change_set_env_deployment_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSetDeploymentHasChangeSetEnvDeployment.get_namespace_name(), id_)

    def upsert_change_set_deployment_has_change_set_env_deployment_hmd_lang_deployment(self, entity: ChangeSetDeploymentHasChangeSetEnvDeployment) -> ChangeSetDeploymentHasChangeSetEnvDeployment:
        if not isinstance(entity, ChangeSetDeploymentHasChangeSetEnvDeployment):
            raise Exception("entity must be an instance of ChangeSetDeploymentHasChangeSetEnvDeployment")
        return self._base_client.upsert_entity(entity)

    def get_from_change_set_deployment_has_change_set_env_deployment_hmd_lang_deployment(self, entity: ChangeSetDeployment) -> List[ChangeSetDeploymentHasChangeSetEnvDeployment]:
        if not isinstance(entity, ChangeSetDeployment):
            raise Exception("entity must be an instance of ChangeSetDeployment")
        return self._base_client.get_relationships_from(entity, ChangeSetDeploymentHasChangeSetEnvDeployment.get_namespace_name())

    def get_to_change_set_deployment_has_change_set_env_deployment_hmd_lang_deployment(self, entity: ChangeSetEnvDeployment) -> List[ChangeSetDeploymentHasChangeSetEnvDeployment]:
        if not isinstance(entity, ChangeSetEnvDeployment):
            raise Exception("entity must be an instance of ChangeSetEnvDeployment")
        return self._base_client.get_relationships_to(entity, ChangeSetDeploymentHasChangeSetEnvDeployment.get_namespace_name())



    # hmd_lang_deployment_change_set_deployment_has_deployment_set
    def delete_change_set_deployment_has_deployment_set_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSetDeploymentHasDeploymentSet.get_namespace_name(), id_)

    def upsert_change_set_deployment_has_deployment_set_hmd_lang_deployment(self, entity: ChangeSetDeploymentHasDeploymentSet) -> ChangeSetDeploymentHasDeploymentSet:
        if not isinstance(entity, ChangeSetDeploymentHasDeploymentSet):
            raise Exception("entity must be an instance of ChangeSetDeploymentHasDeploymentSet")
        return self._base_client.upsert_entity(entity)

    def get_from_change_set_deployment_has_deployment_set_hmd_lang_deployment(self, entity: ChangeSetDeployment) -> List[ChangeSetDeploymentHasDeploymentSet]:
        if not isinstance(entity, ChangeSetDeployment):
            raise Exception("entity must be an instance of ChangeSetDeployment")
        return self._base_client.get_relationships_from(entity, ChangeSetDeploymentHasDeploymentSet.get_namespace_name())

    def get_to_change_set_deployment_has_deployment_set_hmd_lang_deployment(self, entity: DeploymentSet) -> List[ChangeSetDeploymentHasDeploymentSet]:
        if not isinstance(entity, DeploymentSet):
            raise Exception("entity must be an instance of DeploymentSet")
        return self._base_client.get_relationships_to(entity, ChangeSetDeploymentHasDeploymentSet.get_namespace_name())



    # hmd_lang_deployment_change_set_env_deployment_has_environment
    def delete_change_set_env_deployment_has_environment_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSetEnvDeploymentHasEnvironment.get_namespace_name(), id_)

    def upsert_change_set_env_deployment_has_environment_hmd_lang_deployment(self, entity: ChangeSetEnvDeploymentHasEnvironment) -> ChangeSetEnvDeploymentHasEnvironment:
        if not isinstance(entity, ChangeSetEnvDeploymentHasEnvironment):
            raise Exception("entity must be an instance of ChangeSetEnvDeploymentHasEnvironment")
        return self._base_client.upsert_entity(entity)

    def get_from_change_set_env_deployment_has_environment_hmd_lang_deployment(self, entity: ChangeSetEnvDeployment) -> List[ChangeSetEnvDeploymentHasEnvironment]:
        if not isinstance(entity, ChangeSetEnvDeployment):
            raise Exception("entity must be an instance of ChangeSetEnvDeployment")
        return self._base_client.get_relationships_from(entity, ChangeSetEnvDeploymentHasEnvironment.get_namespace_name())

    def get_to_change_set_env_deployment_has_environment_hmd_lang_deployment(self, entity: Environment) -> List[ChangeSetEnvDeploymentHasEnvironment]:
        if not isinstance(entity, Environment):
            raise Exception("entity must be an instance of Environment")
        return self._base_client.get_relationships_to(entity, ChangeSetEnvDeploymentHasEnvironment.get_namespace_name())



    # hmd_lang_deployment_change_set_env_deployment_has_environment_action_execution
    def delete_change_set_env_deployment_has_environment_action_execution_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSetEnvDeploymentHasEnvironmentActionExecution.get_namespace_name(), id_)

    def upsert_change_set_env_deployment_has_environment_action_execution_hmd_lang_deployment(self, entity: ChangeSetEnvDeploymentHasEnvironmentActionExecution) -> ChangeSetEnvDeploymentHasEnvironmentActionExecution:
        if not isinstance(entity, ChangeSetEnvDeploymentHasEnvironmentActionExecution):
            raise Exception("entity must be an instance of ChangeSetEnvDeploymentHasEnvironmentActionExecution")
        return self._base_client.upsert_entity(entity)

    def get_from_change_set_env_deployment_has_environment_action_execution_hmd_lang_deployment(self, entity: ChangeSetEnvDeployment) -> List[ChangeSetEnvDeploymentHasEnvironmentActionExecution]:
        if not isinstance(entity, ChangeSetEnvDeployment):
            raise Exception("entity must be an instance of ChangeSetEnvDeployment")
        return self._base_client.get_relationships_from(entity, ChangeSetEnvDeploymentHasEnvironmentActionExecution.get_namespace_name())

    def get_to_change_set_env_deployment_has_environment_action_execution_hmd_lang_deployment(self, entity: EnvironmentActionExecution) -> List[ChangeSetEnvDeploymentHasEnvironmentActionExecution]:
        if not isinstance(entity, EnvironmentActionExecution):
            raise Exception("entity must be an instance of EnvironmentActionExecution")
        return self._base_client.get_relationships_to(entity, ChangeSetEnvDeploymentHasEnvironmentActionExecution.get_namespace_name())



    # hmd_lang_deployment_change_set_env_deployment_has_repo_instance_deployment
    def delete_change_set_env_deployment_has_repo_instance_deployment_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(ChangeSetEnvDeploymentHasRepoInstanceDeployment.get_namespace_name(), id_)

    def upsert_change_set_env_deployment_has_repo_instance_deployment_hmd_lang_deployment(self, entity: ChangeSetEnvDeploymentHasRepoInstanceDeployment) -> ChangeSetEnvDeploymentHasRepoInstanceDeployment:
        if not isinstance(entity, ChangeSetEnvDeploymentHasRepoInstanceDeployment):
            raise Exception("entity must be an instance of ChangeSetEnvDeploymentHasRepoInstanceDeployment")
        return self._base_client.upsert_entity(entity)

    def get_from_change_set_env_deployment_has_repo_instance_deployment_hmd_lang_deployment(self, entity: ChangeSetEnvDeployment) -> List[ChangeSetEnvDeploymentHasRepoInstanceDeployment]:
        if not isinstance(entity, ChangeSetEnvDeployment):
            raise Exception("entity must be an instance of ChangeSetEnvDeployment")
        return self._base_client.get_relationships_from(entity, ChangeSetEnvDeploymentHasRepoInstanceDeployment.get_namespace_name())

    def get_to_change_set_env_deployment_has_repo_instance_deployment_hmd_lang_deployment(self, entity: RepoInstanceDeployment) -> List[ChangeSetEnvDeploymentHasRepoInstanceDeployment]:
        if not isinstance(entity, RepoInstanceDeployment):
            raise Exception("entity must be an instance of RepoInstanceDeployment")
        return self._base_client.get_relationships_to(entity, ChangeSetEnvDeploymentHasRepoInstanceDeployment.get_namespace_name())



    # hmd_lang_deployment_environment_action_execution_has_environment_action_version
    def delete_environment_action_execution_has_environment_action_version_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(EnvironmentActionExecutionHasEnvironmentActionVersion.get_namespace_name(), id_)

    def upsert_environment_action_execution_has_environment_action_version_hmd_lang_deployment(self, entity: EnvironmentActionExecutionHasEnvironmentActionVersion) -> EnvironmentActionExecutionHasEnvironmentActionVersion:
        if not isinstance(entity, EnvironmentActionExecutionHasEnvironmentActionVersion):
            raise Exception("entity must be an instance of EnvironmentActionExecutionHasEnvironmentActionVersion")
        return self._base_client.upsert_entity(entity)

    def get_from_environment_action_execution_has_environment_action_version_hmd_lang_deployment(self, entity: EnvironmentActionExecution) -> List[EnvironmentActionExecutionHasEnvironmentActionVersion]:
        if not isinstance(entity, EnvironmentActionExecution):
            raise Exception("entity must be an instance of EnvironmentActionExecution")
        return self._base_client.get_relationships_from(entity, EnvironmentActionExecutionHasEnvironmentActionVersion.get_namespace_name())

    def get_to_environment_action_execution_has_environment_action_version_hmd_lang_deployment(self, entity: EnvironmentActionVersion) -> List[EnvironmentActionExecutionHasEnvironmentActionVersion]:
        if not isinstance(entity, EnvironmentActionVersion):
            raise Exception("entity must be an instance of EnvironmentActionVersion")
        return self._base_client.get_relationships_to(entity, EnvironmentActionExecutionHasEnvironmentActionVersion.get_namespace_name())



    # hmd_lang_deployment_environment_action_has_environment_action_version
    def delete_environment_action_has_environment_action_version_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(EnvironmentActionHasEnvironmentActionVersion.get_namespace_name(), id_)

    def upsert_environment_action_has_environment_action_version_hmd_lang_deployment(self, entity: EnvironmentActionHasEnvironmentActionVersion) -> EnvironmentActionHasEnvironmentActionVersion:
        if not isinstance(entity, EnvironmentActionHasEnvironmentActionVersion):
            raise Exception("entity must be an instance of EnvironmentActionHasEnvironmentActionVersion")
        return self._base_client.upsert_entity(entity)

    def get_from_environment_action_has_environment_action_version_hmd_lang_deployment(self, entity: EnvironmentAction) -> List[EnvironmentActionHasEnvironmentActionVersion]:
        if not isinstance(entity, EnvironmentAction):
            raise Exception("entity must be an instance of EnvironmentAction")
        return self._base_client.get_relationships_from(entity, EnvironmentActionHasEnvironmentActionVersion.get_namespace_name())

    def get_to_environment_action_has_environment_action_version_hmd_lang_deployment(self, entity: EnvironmentActionVersion) -> List[EnvironmentActionHasEnvironmentActionVersion]:
        if not isinstance(entity, EnvironmentActionVersion):
            raise Exception("entity must be an instance of EnvironmentActionVersion")
        return self._base_client.get_relationships_to(entity, EnvironmentActionHasEnvironmentActionVersion.get_namespace_name())



    # hmd_lang_deployment_environment_has_repo_instance
    def delete_environment_has_repo_instance_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(EnvironmentHasRepoInstance.get_namespace_name(), id_)

    def upsert_environment_has_repo_instance_hmd_lang_deployment(self, entity: EnvironmentHasRepoInstance) -> EnvironmentHasRepoInstance:
        if not isinstance(entity, EnvironmentHasRepoInstance):
            raise Exception("entity must be an instance of EnvironmentHasRepoInstance")
        return self._base_client.upsert_entity(entity)

    def get_from_environment_has_repo_instance_hmd_lang_deployment(self, entity: Environment) -> List[EnvironmentHasRepoInstance]:
        if not isinstance(entity, Environment):
            raise Exception("entity must be an instance of Environment")
        return self._base_client.get_relationships_from(entity, EnvironmentHasRepoInstance.get_namespace_name())

    def get_to_environment_has_repo_instance_hmd_lang_deployment(self, entity: RepoInstance) -> List[EnvironmentHasRepoInstance]:
        if not isinstance(entity, RepoInstance):
            raise Exception("entity must be an instance of RepoInstance")
        return self._base_client.get_relationships_to(entity, EnvironmentHasRepoInstance.get_namespace_name())



    # hmd_lang_deployment_repo_class_has_repo_class_version
    def delete_repo_class_has_repo_class_version_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoClassHasRepoClassVersion.get_namespace_name(), id_)

    def upsert_repo_class_has_repo_class_version_hmd_lang_deployment(self, entity: RepoClassHasRepoClassVersion) -> RepoClassHasRepoClassVersion:
        if not isinstance(entity, RepoClassHasRepoClassVersion):
            raise Exception("entity must be an instance of RepoClassHasRepoClassVersion")
        return self._base_client.upsert_entity(entity)

    def get_from_repo_class_has_repo_class_version_hmd_lang_deployment(self, entity: RepoClass) -> List[RepoClassHasRepoClassVersion]:
        if not isinstance(entity, RepoClass):
            raise Exception("entity must be an instance of RepoClass")
        return self._base_client.get_relationships_from(entity, RepoClassHasRepoClassVersion.get_namespace_name())

    def get_to_repo_class_has_repo_class_version_hmd_lang_deployment(self, entity: RepoClassVersion) -> List[RepoClassHasRepoClassVersion]:
        if not isinstance(entity, RepoClassVersion):
            raise Exception("entity must be an instance of RepoClassVersion")
        return self._base_client.get_relationships_to(entity, RepoClassHasRepoClassVersion.get_namespace_name())



    # hmd_lang_deployment_repo_class_version_has_external_artifact
    def delete_repo_class_version_has_external_artifact_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoClassVersionHasExternalArtifact.get_namespace_name(), id_)

    def upsert_repo_class_version_has_external_artifact_hmd_lang_deployment(self, entity: RepoClassVersionHasExternalArtifact) -> RepoClassVersionHasExternalArtifact:
        if not isinstance(entity, RepoClassVersionHasExternalArtifact):
            raise Exception("entity must be an instance of RepoClassVersionHasExternalArtifact")
        return self._base_client.upsert_entity(entity)

    def get_from_repo_class_version_has_external_artifact_hmd_lang_deployment(self, entity: RepoClassVersion) -> List[RepoClassVersionHasExternalArtifact]:
        if not isinstance(entity, RepoClassVersion):
            raise Exception("entity must be an instance of RepoClassVersion")
        return self._base_client.get_relationships_from(entity, RepoClassVersionHasExternalArtifact.get_namespace_name())

    def get_to_repo_class_version_has_external_artifact_hmd_lang_deployment(self, entity: ExternalArtifact) -> List[RepoClassVersionHasExternalArtifact]:
        if not isinstance(entity, ExternalArtifact):
            raise Exception("entity must be an instance of ExternalArtifact")
        return self._base_client.get_relationships_to(entity, RepoClassVersionHasExternalArtifact.get_namespace_name())



    # hmd_lang_deployment_repo_class_version_has_repo_class_version_notes
    def delete_repo_class_version_has_repo_class_version_notes_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoClassVersionHasRepoClassVersionNotes.get_namespace_name(), id_)

    def upsert_repo_class_version_has_repo_class_version_notes_hmd_lang_deployment(self, entity: RepoClassVersionHasRepoClassVersionNotes) -> RepoClassVersionHasRepoClassVersionNotes:
        if not isinstance(entity, RepoClassVersionHasRepoClassVersionNotes):
            raise Exception("entity must be an instance of RepoClassVersionHasRepoClassVersionNotes")
        return self._base_client.upsert_entity(entity)

    def get_from_repo_class_version_has_repo_class_version_notes_hmd_lang_deployment(self, entity: RepoClassVersion) -> List[RepoClassVersionHasRepoClassVersionNotes]:
        if not isinstance(entity, RepoClassVersion):
            raise Exception("entity must be an instance of RepoClassVersion")
        return self._base_client.get_relationships_from(entity, RepoClassVersionHasRepoClassVersionNotes.get_namespace_name())

    def get_to_repo_class_version_has_repo_class_version_notes_hmd_lang_deployment(self, entity: RepoClassVersionNotes) -> List[RepoClassVersionHasRepoClassVersionNotes]:
        if not isinstance(entity, RepoClassVersionNotes):
            raise Exception("entity must be an instance of RepoClassVersionNotes")
        return self._base_client.get_relationships_to(entity, RepoClassVersionHasRepoClassVersionNotes.get_namespace_name())



    # hmd_lang_deployment_repo_class_version_req_repo_class
    def delete_repo_class_version_req_repo_class_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoClassVersionReqRepoClass.get_namespace_name(), id_)

    def upsert_repo_class_version_req_repo_class_hmd_lang_deployment(self, entity: RepoClassVersionReqRepoClass) -> RepoClassVersionReqRepoClass:
        if not isinstance(entity, RepoClassVersionReqRepoClass):
            raise Exception("entity must be an instance of RepoClassVersionReqRepoClass")
        return self._base_client.upsert_entity(entity)

    def get_from_repo_class_version_req_repo_class_hmd_lang_deployment(self, entity: RepoClassVersion) -> List[RepoClassVersionReqRepoClass]:
        if not isinstance(entity, RepoClassVersion):
            raise Exception("entity must be an instance of RepoClassVersion")
        return self._base_client.get_relationships_from(entity, RepoClassVersionReqRepoClass.get_namespace_name())

    def get_to_repo_class_version_req_repo_class_hmd_lang_deployment(self, entity: RepoClass) -> List[RepoClassVersionReqRepoClass]:
        if not isinstance(entity, RepoClass):
            raise Exception("entity must be an instance of RepoClass")
        return self._base_client.get_relationships_to(entity, RepoClassVersionReqRepoClass.get_namespace_name())



    # hmd_lang_deployment_repo_instance_deployment_has_repo_class_version
    def delete_repo_instance_deployment_has_repo_class_version_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoInstanceDeploymentHasRepoClassVersion.get_namespace_name(), id_)

    def upsert_repo_instance_deployment_has_repo_class_version_hmd_lang_deployment(self, entity: RepoInstanceDeploymentHasRepoClassVersion) -> RepoInstanceDeploymentHasRepoClassVersion:
        if not isinstance(entity, RepoInstanceDeploymentHasRepoClassVersion):
            raise Exception("entity must be an instance of RepoInstanceDeploymentHasRepoClassVersion")
        return self._base_client.upsert_entity(entity)

    def get_from_repo_instance_deployment_has_repo_class_version_hmd_lang_deployment(self, entity: RepoInstanceDeployment) -> List[RepoInstanceDeploymentHasRepoClassVersion]:
        if not isinstance(entity, RepoInstanceDeployment):
            raise Exception("entity must be an instance of RepoInstanceDeployment")
        return self._base_client.get_relationships_from(entity, RepoInstanceDeploymentHasRepoClassVersion.get_namespace_name())

    def get_to_repo_instance_deployment_has_repo_class_version_hmd_lang_deployment(self, entity: RepoClassVersion) -> List[RepoInstanceDeploymentHasRepoClassVersion]:
        if not isinstance(entity, RepoClassVersion):
            raise Exception("entity must be an instance of RepoClassVersion")
        return self._base_client.get_relationships_to(entity, RepoInstanceDeploymentHasRepoClassVersion.get_namespace_name())



    # hmd_lang_deployment_repo_instance_has_repo_instance_deployment
    def delete_repo_instance_has_repo_instance_deployment_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoInstanceHasRepoInstanceDeployment.get_namespace_name(), id_)

    def upsert_repo_instance_has_repo_instance_deployment_hmd_lang_deployment(self, entity: RepoInstanceHasRepoInstanceDeployment) -> RepoInstanceHasRepoInstanceDeployment:
        if not isinstance(entity, RepoInstanceHasRepoInstanceDeployment):
            raise Exception("entity must be an instance of RepoInstanceHasRepoInstanceDeployment")
        return self._base_client.upsert_entity(entity)

    def get_from_repo_instance_has_repo_instance_deployment_hmd_lang_deployment(self, entity: RepoInstance) -> List[RepoInstanceHasRepoInstanceDeployment]:
        if not isinstance(entity, RepoInstance):
            raise Exception("entity must be an instance of RepoInstance")
        return self._base_client.get_relationships_from(entity, RepoInstanceHasRepoInstanceDeployment.get_namespace_name())

    def get_to_repo_instance_has_repo_instance_deployment_hmd_lang_deployment(self, entity: RepoInstanceDeployment) -> List[RepoInstanceHasRepoInstanceDeployment]:
        if not isinstance(entity, RepoInstanceDeployment):
            raise Exception("entity must be an instance of RepoInstanceDeployment")
        return self._base_client.get_relationships_to(entity, RepoInstanceHasRepoInstanceDeployment.get_namespace_name())



    # hmd_lang_deployment_repo_instance_isa_repo_class
    def delete_repo_instance_isa_repo_class_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoInstanceIsaRepoClass.get_namespace_name(), id_)

    def upsert_repo_instance_isa_repo_class_hmd_lang_deployment(self, entity: RepoInstanceIsaRepoClass) -> RepoInstanceIsaRepoClass:
        if not isinstance(entity, RepoInstanceIsaRepoClass):
            raise Exception("entity must be an instance of RepoInstanceIsaRepoClass")
        return self._base_client.upsert_entity(entity)

    def get_from_repo_instance_isa_repo_class_hmd_lang_deployment(self, entity: RepoInstance) -> List[RepoInstanceIsaRepoClass]:
        if not isinstance(entity, RepoInstance):
            raise Exception("entity must be an instance of RepoInstance")
        return self._base_client.get_relationships_from(entity, RepoInstanceIsaRepoClass.get_namespace_name())

    def get_to_repo_instance_isa_repo_class_hmd_lang_deployment(self, entity: RepoClass) -> List[RepoInstanceIsaRepoClass]:
        if not isinstance(entity, RepoClass):
            raise Exception("entity must be an instance of RepoClass")
        return self._base_client.get_relationships_to(entity, RepoInstanceIsaRepoClass.get_namespace_name())



    # hmd_lang_deployment_repo_instance_req_repo_instance
    def delete_repo_instance_req_repo_instance_hmd_lang_deployment(self, id_: str) -> None:
        self._base_client.delete_entity(RepoInstanceReqRepoInstance.get_namespace_name(), id_)

    def upsert_repo_instance_req_repo_instance_hmd_lang_deployment(self, entity: RepoInstanceReqRepoInstance) -> RepoInstanceReqRepoInstance:
        if not isinstance(entity, RepoInstanceReqRepoInstance):
            raise Exception("entity must be an instance of RepoInstanceReqRepoInstance")
        return self._base_client.upsert_entity(entity)

    def get_from_repo_instance_req_repo_instance_hmd_lang_deployment(self, entity: RepoInstance) -> List[RepoInstanceReqRepoInstance]:
        if not isinstance(entity, RepoInstance):
            raise Exception("entity must be an instance of RepoInstance")
        return self._base_client.get_relationships_from(entity, RepoInstanceReqRepoInstance.get_namespace_name())

    def get_to_repo_instance_req_repo_instance_hmd_lang_deployment(self, entity: RepoInstance) -> List[RepoInstanceReqRepoInstance]:
        if not isinstance(entity, RepoInstance):
            raise Exception("entity must be an instance of RepoInstance")
        return self._base_client.get_relationships_to(entity, RepoInstanceReqRepoInstance.get_namespace_name())


