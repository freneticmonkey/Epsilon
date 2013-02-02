'''
Created on Apr 26, 2012

@author: scottporter
'''
import pygame
from pygame import mouse 

from epsilon.logging.logger import Logger
from epsilon.frameworks.baseframework import BaseFramework

from epsilon.core.input import Input

class PyGameFramework(BaseFramework):
    def __init__(self):
        BaseFramework.__init__(self)
        self._keep_alive = True
        Logger.Log("Using PyGame Framework")
    
    def initialise_display(self, width, height, title="PyGame Window"):
        self._width = width
        self._height = height
        self._title = title
        
        # Start PyGame
        pygame.init()
        
        # Configure Window
        pygame.display.set_mode((self._width, self._height), pygame.OPENGL|pygame.DOUBLEBUF)
        pygame.display.set_caption(self._title)
        
        self._input = PyGameInput()
        
        Logger.Log("Initialised PyGame Window")
        
    def start(self):
        self._setup()
        
        # Until a Quit Event is detected process engine systems
        while self._keep_alive == True:
            self.run_loop()
            self._drawfunc()
            pygame.display.flip()
            
    def stop(self):
        self._keep_alive = False
        self._shutdown()
        

class PyGameInput(Input):
    
    def __init__(self):
        Input.__init__(self)
        Input._instance = self
    
    def _framework_init(self):
#        self._key_events = []
        
        self._exclusive_mouse = False
        self._mouse_rel_x = 0.0
        self._mouse_rel_y = 0.0
        
        # Mouse Down position used for exclusive mode
        self._ex_mouse_x = 0 
        self._ex_mouse_y = 0
    
    @classmethod
    def get_key_events(cls):
        return cls._instance._key_events
    
    def _set_mouse_pos(self, mouse_x, mouse_y):
        pygame.mouse.set_pos(mouse_x, mouse_y)
        
    def on_frame_start(self):
        self._process_input()
        
    def on_frame_end(self):
        pass
    
    def _process_input(self):

        # Mouse
        self._mouse_x, self._mouse_y = pygame.mouse.get_pos()
        self._mouse_rel_x, self._mouse_rel_y = pygame.mouse.get_rel()
        
        mouse_buttons = pygame.mouse.get_pressed()
        
        for button in range(0, len(mouse_buttons)):
            
            state = mouse_buttons[button]
            
            self._process_input_state(button, state)
            
        # Keyboard
        keys = pygame.key.get_pressed()
                
        # Check for Keys pressed this frame
        for key in range(3, len(keys)):
            
            state = keys[key]
            
            self._process_input_state(key, state)
            
        self._ready = True
        
        # Clear on each frame
        self._key_events = []
        
#        # Store the pygame key events for pyui access        
        for event in pygame.event.get():
#            if event.type == pygame.KEYDOWN:
#                self._key_events.append(event)
#            elif event.type == pygame.KEYUP:
#                self._key_events.append(event)
            if event.type == pygame.QUIT:
                self._quit_detected = True
                
    def set_exclusive_mouse(self, exclusive):
        
        if not exclusive == self._exclusive_mouse:
            self._exclusive_mouse = exclusive
            
            if self._exclusive_mouse:
                mouse.set_visible(False)
                pygame.event.set_grab(True)
                
                self._ex_mouse_x, self._ex_mouse_y = pygame.mouse.get_pos()
            else:
                # Show the cursor
                mouse.set_visible(True)
                pygame.event.set_grab(False)
                pygame.mouse.set_pos(self._ex_mouse_x, self._ex_mouse_y)
            
        