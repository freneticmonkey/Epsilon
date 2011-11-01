'''
Created on Sep 20, 2011

@author: scottporter
'''
from time import time, clock
from datetime import datetime
import pygame

MAX_FPS = 1000

deltaTime = 0.00001

#_frame_start = clock() 
_frame_start = datetime.now()

_pygame_clock = None

def UpdateDelta():
    global deltaTime
    global _pygame_clock
    if _pygame_clock is None:
        _pygame_clock = pygame.time.Clock()
    
#    global _frame_start
#    el = datetime.now() - _frame_start
#    deltaTime = el.microseconds / 1000000.0
#    _frame_start = datetime.now()

    deltaTime = _pygame_clock.tick(MAX_FPS) / 1000.0
    
def GetFPS():
    global _pygame_clock
    if _pygame_clock is None:
        _pygame_clock = pygame.time.Clock()
    
    return _pygame_clock.get_fps()