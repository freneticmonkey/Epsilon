'''
Created on Feb 4, 2012

@author: scottporter
'''
#from Geometry.euclid import Vector2

class DisplaySettings:
    resolution = [1000, 600]
    window_title = "Epsilon"
    fullscreen = False
    
    
class LoggerSettings:
    method = 'file'
    filename = 'EpsilonLog.txt'
    log_to_console = True
    
class Frameworks:
    PYGAME = 1
    PYGLET = 2
    
class FrameworkSettings:
    use_framework = Frameworks.PYGLET
    #use_framework = Frameworks.PYGAME
    