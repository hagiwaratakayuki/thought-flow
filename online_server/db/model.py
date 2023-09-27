from google.cloud import datastore
import re
from typing import Iterable
client = None


def get_client():
    global client
    if client is None:
        client = datastore.Client()
    return client

PT = re.compile('^_')
class Model(object):
    _entity_options:dict
    _entity = None
    def __init__(self, eid=None, entry_options={}, path_args=[], kwargs={}) -> None:
        self._path_args = path_args
        self._kwargs = kwargs
        self._entity_options = entry_options
        self._eid = eid
        self._entity_options = entry_options
    @classmethod
    def query(cls):
        
        return get_client().query(kind=cls.__name__)
    def _filter(self, key):
        if PT.search(key) is not None:
            return False
        if callable(getattr(self, key)):
            return False
        return True

    def _update(self, path_args=None, kwargs=None, eid=None):
        eid = eid or self._eid
        path_args = path_args or self._path_args 
        kwargs = kwargs or self._kwargs

        client = get_client()
        with client.transaction():
            entity = self.get_entity(eid, path_args, kwargs) 

            client.put(entity)
        return entity
    def get_entity(self, eid=None, path_args=None, kwargs=None):
        if self._entity != None:
            entity = self._entity
        else:
            options = self._entity_options
            key = self.__class__._get_key(path_args or  self._path_args, kwargs or self._kwargs, eid or self._eid)
            entity = datastore.Entity(key=key, **options)
        data = {key:getattr(self, key) for key in  filter(self._filter, dir(self)) }
        
        entity.update(data)
        return entity
    @classmethod
    def get(cls, eid, *path_args, **kwargs):
        key = cls._get_key(path_args, kwargs, eid)
        return get_client().get(key)
    @classmethod
    def get_multi(cls, params):
        
        keys = [cls._get_key(**param) for param in params]

        return get_client().get_multi(keys)
    


    @classmethod
    def _get_key(cls, path_args=[], kwargs={}, eid=None):
        
        _path = path_args[:]
        _path.append(cls.__name__)
        if eid is not None:
            _path.append(eid)
        return get_client().key(*_path, **kwargs)
    def insert(self, *path_args, **kwrgs):
        return self._update(path_args, kwrgs)
    def upsert (self, eid=None, *path_args, **kwrgs):
        return self._update(path_args, kwrgs, eid)
    @classmethod
    def from_entity(cls, entity):
        ret = cls()
        for k, v in entity.items():
            setattr(ret, k, v)
        ret._entity = entity
        return ret


    
def put_multi(models:Iterable[Model]):
    entities = [model.get_entity() for model in models]
    get_client().put_multi(entities)
    return entities

    



