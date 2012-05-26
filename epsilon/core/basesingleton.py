'''
Created on Nov 19, 2011

@author: scottporter
'''

class BaseSingleton(object):
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            
        return cls._instance