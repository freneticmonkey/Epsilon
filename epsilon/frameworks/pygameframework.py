'''
Created on Apr 26, 2012

@author: scottporter
'''
import pygame
from pygame import mouse 

from epsilon.logging import Logger
from epsilon.frameworks.baseframework import BaseFramework

from epsilon.core.input import Input
import epsilon.core.settings as Settings

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
        Logger.Log("Initialised PyGame Window")
        
        self._input = PyGameInput()
        
    def start(self):
        self._setup()
        
        # Until a Quit Event is detected process engine systems
        while self._keep_alive == True:
            self.run_loop()
            self._drawfunc()
            pygame.display.flip()
            
    def stop(self):
        self._keep_alive = False
        

class PyGameInput(Input):
    
    def __init__(self):
        Input.__init__(self)
        Input._instance = self
    
    def _framework_init(self):
        self._key_events = []
        
        # Configure exclusive mouse properties
        self._initial_mouse_down = False
        self._initial_mouse_up = False
        self._res = Settings.DisplaySettings.resolution
        self._h_res = [self._res[0]/2, self._res[1]/2]
        
        self._init_mouse_x = 0
        self._init_mouse_y = 0
        
        self._exclusive_mouse = False
        self._mouse_rel_x = 0.0
        self._mouse_rel_y = 0.0
        self._mouse_moved = False
    
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
        
        # TODO: Hmm relative mouse movement is busted here. This needs to be fixed. Too tired atm.
        #       Look at PygletInput for ideas. 
        
        # Set mouse position
        if self._exclusive_mouse:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self._mouse_rel_x = mouse_x - self._init_mouse_x
            self._mouse_rel_y = mouse_y - self._init_mouse_y
        else:
            self._mouse_x, self._mouse_y = pygame.mouse.get_pos()
            self._mouse_rel_x = 0.0
            self._mouse_rel_y = 0.0
        
        mouse_buttons = pygame.mouse.get_pressed()
        
        for button in range(0, len(mouse_buttons)):
            
            state = mouse_buttons[button]
            
            self._process_input_state(button, state)
        # Keyboard
        keys = pygame.key.get_pressed()
                
        # Check for Keys pressed this frame
        for key in range(0, len(keys)):
            
            state = keys[key]
            
            self._process_input_state(key, state)
            
        self._ready = True
        
        # Clear on each frame
        self._key_events = []
        
        # Store the pygame key events for pyui access        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._key_events.append(event)
            elif event.type == pygame.KEYUP:
                self._key_events.append(event)
            elif event.type == pygame.QUIT:
                self._quit_detected = True
                
    def set_exclusive_mouse(self, exclusive):
        
        self._exclusive_mouse = exclusive
        
        if exclusive:
            mouse.set_visible(False)
            
            # And its not the initial frame
            if not self._initial_mouse_down:
                # Reset the mouse position to the centre of the screen
                #self._mouse_x, self._mouse_y = mouse.get_pos()
                
#                self._mouse_x, self._mouse_y = self.get_mouse_move()
                self._init_mouse_x = self._h_res[0]
                self._init_mouse_y = self._h_res[1]
                
#                self._mouse_x -= self._h_res[0]
#                self._mouse_y -= self._h_res[1]
#                Input.set_mouse_pos(self._mouse_x, self._mouse_y)
            else:
                self._initial_mouse_down = False
#                Input.set_mouse_pos(0, 0)
#                self._mouse_x = self._init_mouse_x
#                self._mouse_y = self._init_mouse_x
                
            #mouse.set_pos(self._h_res[0],self._h_res[1])
#            Input.set_mouse_pos(self._h_res[0],self._h_res[1])
            self._mouse_x = self._init_mouse_x
            self._mouse_y = self._init_mouse_y
            
            self._initial_mouse_up = True
            
        else:
            self._initial_mouse_down = True
            if self._initial_mouse_up:
                # Show the cursor
                mouse.set_visible(True)
                self._initial_mouse_up = False