'''
Created on Apr 26, 2012

@author: scottporter
'''
import pyglet
#from pyglet.gl import *
from pyglet.window import key

# disable error checking for increased performance
pyglet.options['debug_gl'] = False

from epsilon.core.input import *

from epsilon.logging.logger import Logger
from epsilon.frameworks.baseframework import BaseFramework

from epsilon.core.settings import Settings

def on_key_press(symbols, modifiers):
    pass

def on_key_release(symbols, modifiers):
    pass

def on_mouse_press(x, y, button, modifiers):
    pass

def on_mouse_release(x, y, button, modifiers):
    pass

class PygletFramework(BaseFramework):
    def __init__(self):
        BaseFramework.__init__(self)
        Logger.Log("Using Pyglet Framework")
        
    def initialise_display(self, width, height, title="Pyglet Window"):
        self._width = width
        self._height = height
        self._title = title
    
        self._window = pyglet.window.Window(self._width, self._height, self._title, True, vsync=False)
        self._window.set_location(Settings.get('DisplaySettings','location')[0], Settings.get('DisplaySettings','location')[1])
        self._window.on_draw = self._draw
        
        # Configure the input object
        self._input = PygletInput(self._window)
        
        self._fps_display = pyglet.clock.ClockDisplay()
        
        Logger.Log("Initialised Pyglet window")
    
    def _draw(self):
        self._window.clear()
        
        if not self._draw is None:
            self._drawfunc()
        
        # Doesn't appear to be working...
        #self._fps_display.draw()
        
    @property
    def window(self):
        return self._window
        
    @property
    def on_draw(self):
        return self._drawfunc
        
    @on_draw.setter
    def on_draw(self, set_on_draw):
        self._drawfunc = set_on_draw
        
    def start(self):
        self._setup()
        pyglet.clock.schedule(self._run_loop)
        pyglet.app.run()
        
    def stop(self):
        location = self._window.get_location() # returns a tuple? So convert to array
        
        Settings.set('DisplaySettings','location', [location[0], location[1]] )
        
        self._shutdown()
        pyglet.app.exit()
        

class PygletInput(Input):
    
    def __init__(self, window):
        self._window = window
        Input.__init__(self)
        Input._instance = self
    
    def _framework_init(self):
        if self._window:
            # Add Key Handler
            self._keys = pyglet.window.key.KeyStateHandler()
            self._window.push_handlers(self._keys)
            
            # Input Handlers
            self._window.on_key_press = self._on_key_press
            self._window.on_key_release = self._on_key_release
            self._window.on_mouse_press = self._on_mouse_press
            self._window.on_mouse_release = self._on_mouse_release
            self._window.on_mouse_drag = self._on_mouse_drag
            self._window.on_mouse_motion = self._on_mouse_move
            
            Logger.Log("Listening to Pyglet Input events")
        else:
            Logger.Log("ERROR: Unable to use Pyglet Input Events. Missing Window object")
            
        self._mouse_moved = False
        self._mouse_rel_x_change = 0.0
        self._mouse_rel_y_change = 0.0
    
    def on_frame_start(self):
        self._mouse_moved = False
        
    def on_frame_end(self):
        if self._mouse_moved:
            self._mouse_rel_x = self._mouse_rel_x_change
            self._mouse_rel_y = self._mouse_rel_y_change
        else:
            self._mouse_rel_x = 0.0
            self._mouse_rel_y = 0.0
    
    def set_windowlistener(self, window):
        self._window = window
        # Re/initialise the input listeners
        self._framework_init()
        
    def _on_key_press(self, symbol, modifiers):
        self._process_input()
        
    def _on_key_release(self, symbol, modifiers):
        self._process_input()
        
    def _process_input(self):
        
        for button, state in self._keys.iteritems():
            
            # Re-map any special keys to their epsilon key values
            if button > 65000:
            
                if button == key.TAB:
                    button = Input.KEY_TAB
                elif button == key.BACKSPACE:
                    button = Input.KEY_DEL
                elif button == key.RETURN:
                    button = Input.KEY_RETURN
                elif button == key.ESCAPE:
                    button = Input.KEY_ESCAPE
                elif button == key.SPACE:
                    button = Input.KEY_SPACE
                
                # DIRECTIONAL
                elif button == key.UP:
                    button = Input.KEY_UP
                elif button == key.DOWN:
                    button = Input.KEY_DOWN
                elif button == key.RIGHT:
                    button = Input.KEY_RIGHT
                elif button == key.LEFT:
                    button = Input.KEY_LEFT
                    
                # MODIFIERS
                elif button == key.CAPSLOCK:
                    button = Input.KEY_CAPS
                elif button == key.RSHIFT:
                    button = Input.KEY_RIGHT_SHIFT
                elif button == key.LSHIFT:
                    button = Input.KEY_LEFT_SHIFT
                elif button == key.LCTRL:
                    button = Input.KEY_CTRL
                #elif button == key.RCTRL:
                
                elif button == key.RALT:
                    button = Input.KEY_RIGHT_ALT
                elif button == key.LALT:
                    button = Input.KEY_LEFT_ALT
                elif button == key.LCOMMAND:
                    button = Input.KEY_LEFT_CMD
                elif button == key.RCOMMAND:
                    button = Input.KEY_RIGHT_CMD
            
            self._process_input_state(button, state)
                
    def _on_mouse_press(self, x, y, button, modifiers):
        self._mouse_x = x
        self._mouse_y = y
        
#        Logger.Log("Mouse button: %d pressed @ x: %d y: %d" % (button, x, y))
        
        # Adjust pyglet mouse button to epsilon mouse button
        button -= 1
        
        self._process_input_state(button, True)
        
    def _on_mouse_release(self, x, y, button, modifiers):
        self._mouse_x = x
        self._mouse_y = y
        
#        Logger.Log("Mouse button: %d released @ x: %d y: %d" % (button, x, y))
        
        # Adjust pyglet mouse button to epsilon mouse button
        button -= 1
        
        self._process_input_state(button, False)
        
    def _on_mouse_move(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        self._mouse_x = mouse_x
        self._mouse_y = mouse_y
        
        self._mouse_rel_x = 0.0
        self._mouse_rel_y = 0.0
        
#        self._mouse_rel_x = mouse_dx
#        self._mouse_rel_y = mouse_dy
        
#        Logger.Log("Mouse moved: @ x: %d y: %d" % (mouse_x, mouse_y))
        
    def _on_mouse_drag(self, mouse_x, mouse_y, mouse_dx, mouse_dy, buttons, modifiers):
        self._mouse_x = mouse_x
        self._mouse_y = mouse_y
        
        self._mouse_rel_x_change = mouse_dx
        self._mouse_rel_y_change = mouse_dy
        
        self._mouse_moved = True
        
#        Logger.Log("Mouse dragged: @ x: %d y: %d dx: %f dy: %f" % (mouse_x, mouse_y, mouse_dx, mouse_dy))
        
    def _set_mouse_pos(self, mouse_x, mouse_y):
        # Pyglet can't set the mouse position :/
        pass
    
    def set_exclusive_mouse(self, exclusive):
        self._window.set_exclusive_mouse(exclusive)

    