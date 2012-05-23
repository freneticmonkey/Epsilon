'''
Created on Apr 26, 2012

@author: scottporter
'''

from Core.Settings import Frameworks, FrameworkSettings
from Core.BaseSingleton import BaseSingleton

from Frameworks.PyGameFramework import PyGameFramework
from Frameworks.PygletFramework import PygletFramework

class FrameworkManager(BaseSingleton):
    def __init__(self):
        self._framework = None
        
        if FrameworkSettings.use_framework == Frameworks.PYGAME:
            self._framework = PyGameFramework.get_instance()
            
        elif FrameworkSettings.use_framework == Frameworks.PYGLET:
            self._framework = PygletFramework.get_instance()
            
    @property
    def framework(self):
        return self._framework
    
    def stop(self):
        self._framework.stop()
