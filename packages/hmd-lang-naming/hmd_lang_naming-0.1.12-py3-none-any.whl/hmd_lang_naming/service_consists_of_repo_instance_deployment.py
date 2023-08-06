

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_naming.service import Service
from hmd_lang_deployment.repo_instance_deployment import RepoInstanceDeployment
from datetime import datetime
from typing import List, Dict, Any

class ServiceConsistsOfRepoInstanceDeployment(Relationship):

    _entity_def = \
        {'name': 'service_consists_of_repo_instance_deployment', 'namespace': 'hmd_lang_naming', 'metatype': 'relationship', 'ref_from': 'hmd_lang_naming.service', 'ref_to': 'hmd_lang_deployment.repo_instance_deployment', 'attributes': {}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ServiceConsistsOfRepoInstanceDeployment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ServiceConsistsOfRepoInstanceDeployment._entity_def)


    @staticmethod
    def ref_from_type():
        return Service

    @staticmethod
    def ref_to_type():
        return RepoInstanceDeployment

    

    