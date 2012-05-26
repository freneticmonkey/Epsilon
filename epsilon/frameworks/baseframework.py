'''
Created on Apr 26, 2012

@author: scottporter
'''
from epsilon.core.basesingleton import BaseSingleton

class BaseFramework(BaseSingleton):
    
    def __init__(self):
        # Functions
        self._setup = None
        self._run_loop = None
        self._drawfunc = None
        
    @property
    def run_loop(self):
        return self._run_loop
    
    @run_loop.setter
    def run_loop(self, new_run_loop):
        self._run_loop = new_run_loop
        
    @property
    def setup(self):
        return self._setup
    
    @setup.setter
    def setup(self, new_setup):
        self._setup = new_setup
        
    @property
    def on_draw(self):
        return self._drawfunc
    
    @on_draw.setter
    def on_draw(self, set_on_draw):
        self._drawfunc = set_on_draw
    
    def stop(self):
        pass
    
    def initialise_display(self, width, height, title):
        pass
    
    def start(self):
        self._setup()
        self._run_loop()
    
    