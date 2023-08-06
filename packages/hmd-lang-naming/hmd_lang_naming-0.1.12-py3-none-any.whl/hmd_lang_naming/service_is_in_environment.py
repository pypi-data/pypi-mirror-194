

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_naming.service import Service
from hmd_lang_deployment.environment import Environment
from datetime import datetime
from typing import List, Dict, Any

class ServiceIsInEnvironment(Relationship):

    _entity_def = \
        {'name': 'service_is_in_environment', 'namespace': 'hmd_lang_naming', 'metatype': 'relationship', 'ref_from': 'hmd_lang_naming.service', 'ref_to': 'hmd_lang_deployment.environment', 'attributes': {}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return ServiceIsInEnvironment._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(ServiceIsInEnvironment._entity_def)


    @staticmethod
    def ref_from_type():
        return Service

    @staticmethod
    def ref_to_type():
        return Environment

    

    