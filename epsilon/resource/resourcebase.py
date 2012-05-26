'''
Created on Mar 4, 2012

@author: scottporter
'''

from os.path import dirname

class ResourceType:
    IMAGE   = 0
    MESH    = 1
    SCENE   = 2
    SCRIPT  = 3
    SHADER  = 4
    TEXT    = 5
    PATH    = 6
    ARCHIVE = 7

class ResourceBase(object):
    _rid = 0
    @classmethod
    def get_id(cls):
        cls._rid += 1
        return cls._rid
    
    def __init__(self, filename = "", resource_type=None, data=None, loaded=False):
        self._filename = filename
        self._path = dirname(filename)
        self._type = resource_type
        self._id = ResourceBase.get_id()
        
        # If this needs to be updated at run-time it will be updated by the Classes
        # that inherit from ResourceBase
        self._loaded = loaded
            
    @property
    def rid(self):
        return self._id
    
    @property 
    def filename(self):
        return self._filename
    
    @property
    def path(self):
        return self._path
    
    @property
    def loaded(self):
        return self._loaded
            
    
    