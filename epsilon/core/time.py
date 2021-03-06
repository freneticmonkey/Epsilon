'''
Created on Sep 20, 2011

@author: scottporter
'''
#from time import time as p_time
#from time import clock as p_clock

from datetime import datetime
#import pygame

from epsilon.core.basemanager import BaseSingleton

#MAX_FPS = 1000
#delta_time = 0.000001

class Time(BaseSingleton):
    delta_time = 0
    SMOOTH_A = 0.9
    SMOOTH_B = 0.1
    
    def __init__(self):
        self._last_frame_start = datetime.now()
        self._delta_time = 0.00001
        self._last_delta_time = 0.0001
        self._fps = 0.0
#        self._last_frame_start = datetime.now()
        #self._pygame_clock = pygame.time.Clock()
        
#    @property
#    def delta_time(self):
#        return self._delta_time
    
    def update_delta(self):
        # This method is not ideal, but until I can figure out some kind of 
        # class property...
        
        #self._delta_time = self._pygame_clock.tick(MAX_FPS) / 1000.0
        now = datetime.now()
        self._delta_time = (now - self._last_frame_start).total_seconds()
        self._last_frame_start = now
        self.__class__.delta_time = self._delta_time
        
        self._fps = 1000 / ( (self._delta_time * self.SMOOTH_A + self._last_delta_time + self.SMOOTH_B) * 100)
        self.__class__.fps = self._fps
        