'''
Created on Sep 20, 2011

@author: scottporter
'''
from time import time, clock
from datetime import datetime
import pygame

from Core.BaseManager import BaseSingleton

MAX_FPS = 1000

delta_time = 0.000001

class Time(BaseSingleton):
    
    def __init__(self):
        self.deltaTime = 0.00001
        self._frame_start = datetime.now()
        self._pygame_clock = pygame.time.Clock()
        
    @property
    def delta_time(self):
        return self._delta_time
        
    def update_delta(self):
        # This method is not ideal, but until I can figure out some kind of 
        # class property...
        global delta_time
        self._delta_time = self._pygame_clock.tick(MAX_FPS) / 1000.0
        delta_time = self._delta_time
        
    
    @classmethod
    def get_fps(cls):
        return cls._instance._pygame_clock.get_fps()