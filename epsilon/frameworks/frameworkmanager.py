'''
Created on Apr 26, 2012

@author: scottporter
'''

from epsilon.core.settings import Frameworks, FrameworkSettings
from epsilon.core.basesingleton import BaseSingleton

from epsilon.frameworks.pygameframework import PyGameFramework
from epsilon.frameworks.pygletframework import PygletFramework

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
