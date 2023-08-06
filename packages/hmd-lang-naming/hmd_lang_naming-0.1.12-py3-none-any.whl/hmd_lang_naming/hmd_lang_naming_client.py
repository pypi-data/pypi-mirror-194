# The code in this file is generated automatically.
# DO NOT EDIT!
from hmd_graphql_client.hmd_base_client import BaseClient
from typing import List
from hmd_schema_loader.hmd_schema_loader import get_default_loader, get_schema_root


from .service import Service



from hmd_lang_deployment.repo_instance_deployment import RepoInstanceDeployment

from .service_consists_of_repo_instance_deployment import ServiceConsistsOfRepoInstanceDeployment


from hmd_lang_deployment.environment import Environment

from .service_is_in_environment import ServiceIsInEnvironment

def get_client_loader():
    return get_default_loader("hmd_lang_naming")

def get_client_schema_root():
    return get_schema_root("hmd_lang_naming")

class HmdLangNamingClient:
    def __init__(self, base_client: BaseClient):
        self._base_client = base_client

    # Generic upsert...
    def upsert(self, entity):
        return self._base_client.upsert_entity(entity)

    # Generic delete...
    def delete(self, entity):
        self._base_client.delete_entity(entity.get_namespace_name(), entity.identifier)

    # Nouns...

    # hmd_lang_naming_service
    def get_service_hmd_lang_naming(self, id_: str) -> Service:
        return self._base_client.get_entity(Service.get_namespace_name(), id_)

    def delete_service_hmd_lang_naming(self, id_: str) -> None:
        self._base_client.delete_entity(Service.get_namespace_name(), id_)

    def upsert_service_hmd_lang_naming(self, entity: Service) -> Service:
        if not isinstance(entity, Service):
            raise Exception("entity must be an instance of Service")
        return self._base_client.upsert_entity(entity)

    
    def search_service_hmd_lang_naming(self, filter_: dict) -> List[Service]:
        return self._base_client.search_entity(Service.get_namespace_name(), filter_)


    # Relationships...

    # hmd_lang_naming_service_consists_of_repo_instance_deployment
    def delete_service_consists_of_repo_instance_deployment_hmd_lang_naming(self, id_: str) -> None:
        self._base_client.delete_entity(ServiceConsistsOfRepoInstanceDeployment.get_namespace_name(), id_)

    def upsert_service_consists_of_repo_instance_deployment_hmd_lang_naming(self, entity: ServiceConsistsOfRepoInstanceDeployment) -> ServiceConsistsOfRepoInstanceDeployment:
        if not isinstance(entity, ServiceConsistsOfRepoInstanceDeployment):
            raise Exception("entity must be an instance of ServiceConsistsOfRepoInstanceDeployment")
        return self._base_client.upsert_entity(entity)

    def get_from_service_consists_of_repo_instance_deployment_hmd_lang_naming(self, entity: Service) -> List[ServiceConsistsOfRepoInstanceDeployment]:
        if not isinstance(entity, Service):
            raise Exception("entity must be an instance of Service")
        return self._base_client.get_relationships_from(entity, ServiceConsistsOfRepoInstanceDeployment.get_namespace_name())

    def get_to_service_consists_of_repo_instance_deployment_hmd_lang_naming(self, entity: RepoInstanceDeployment) -> List[ServiceConsistsOfRepoInstanceDeployment]:
        if not isinstance(entity, RepoInstanceDeployment):
            raise Exception("entity must be an instance of RepoInstanceDeployment")
        return self._base_client.get_relationships_to(entity, ServiceConsistsOfRepoInstanceDeployment.get_namespace_name())



    # hmd_lang_naming_service_is_in_environment
    def delete_service_is_in_environment_hmd_lang_naming(self, id_: str) -> None:
        self._base_client.delete_entity(ServiceIsInEnvironment.get_namespace_name(), id_)

    def upsert_service_is_in_environment_hmd_lang_naming(self, entity: ServiceIsInEnvironment) -> ServiceIsInEnvironment:
        if not isinstance(entity, ServiceIsInEnvironment):
            raise Exception("entity must be an instance of ServiceIsInEnvironment")
        return self._base_client.upsert_entity(entity)

    def get_from_service_is_in_environment_hmd_lang_naming(self, entity: Service) -> List[ServiceIsInEnvironment]:
        if not isinstance(entity, Service):
            raise Exception("entity must be an instance of Service")
        return self._base_client.get_relationships_from(entity, ServiceIsInEnvironment.get_namespace_name())

    def get_to_service_is_in_environment_hmd_lang_naming(self, entity: Environment) -> List[ServiceIsInEnvironment]:
        if not isinstance(entity, Environment):
            raise Exception("entity must be an instance of Environment")
        return self._base_client.get_relationships_to(entity, ServiceIsInEnvironment.get_namespace_name())


