'''
Created on Apr 26, 2012

@author: scottporter
'''

from epsilon.core.settings import Frameworks, Settings
from epsilon.core.basesingleton import BaseSingleton

class FrameworkManager(BaseSingleton):

    @classmethod
    def framework(cls):
        return cls.get_instance()._framework

    def __init__(self):
        self._current_framework = None
        
        selected_framework = Settings.get('FrameworkSettings','use_framework')

        if selected_framework == Frameworks.PYGAME:
            from epsilon.frameworks.pygameframework import PyGameFramework
            self._current_framework = PyGameFramework.get_instance()
            
        elif selected_framework == Frameworks.PYGLET:
            from epsilon.frameworks.pygletframework import PygletFramework
            self._current_framework = PygletFramework.get_instance()
            
    @property
    def _framework(self):
        return self._current_framework
    
    def stop(self):
        self._current_framework.stop()
