

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class TimestampRecord(Noun):

    _entity_def = \
        {'name': 'timestamp_record', 'namespace': 'hmd_lang_deployment', 'metatype': 'noun', 'description': 'A labeled timestamp for monitoring purposes.', 'attributes': {'type': {'type': 'string', 'description': 'A label.', 'required': True}, 'timestamp': {'type': 'timestamp', 'description': 'The timestamp.', 'required': True}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return TimestampRecord._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(TimestampRecord._entity_def)


    

    
        
    @property
    def type(self) -> str:
        return self._getter("type")

    @type.setter
    def type(self, value: str) -> None:
        self._setter("type", value)
    
        
    @property
    def timestamp(self) -> datetime:
        return self._getter("timestamp")

    @timestamp.setter
    def timestamp(self, value: datetime) -> None:
        self._setter("timestamp", value)
    

    
    