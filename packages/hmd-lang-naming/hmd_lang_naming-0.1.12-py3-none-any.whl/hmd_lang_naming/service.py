

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class Service(Noun):

    _entity_def = \
        {'name': 'service', 'namespace': 'hmd_lang_naming', 'metatype': 'noun', 'attributes': {'name': {'type': 'string', 'description': 'Name of service', 'required': True}, 'description': {'type': 'string', 'description': 'Description of the service'}, 'httpEndpoint': {'type': 'string', 'description': 'HTTP URL endpoint used to access the service'}, 'arnEndpoint': {'type': 'string', 'description': 'Lambda ARN for the service'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return Service._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(Service._entity_def)


    

    
        
    @property
    def name(self) -> str:
        return self._getter("name")

    @name.setter
    def name(self, value: str) -> None:
        self._setter("name", value)
    
        
    @property
    def description(self) -> str:
        return self._getter("description")

    @description.setter
    def description(self, value: str) -> None:
        self._setter("description", value)
    
        
    @property
    def httpEndpoint(self) -> str:
        return self._getter("httpEndpoint")

    @httpEndpoint.setter
    def httpEndpoint(self, value: str) -> None:
        self._setter("httpEndpoint", value)
    
        
    @property
    def arnEndpoint(self) -> str:
        return self._getter("arnEndpoint")

    @arnEndpoint.setter
    def arnEndpoint(self, value: str) -> None:
        self._setter("arnEndpoint", value)
    

    
    
        
    def get_from_service_consists_of_repo_instance_deployment_hmd_lang_naming(self):
        return self.from_rels["hmd_lang_naming.service_consists_of_repo_instance_deployment"]
    
        
    def get_from_service_is_in_environment_hmd_lang_naming(self):
        return self.from_rels["hmd_lang_naming.service_is_in_environment"]
    