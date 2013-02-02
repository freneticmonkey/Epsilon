import os

from epsilon.ui.simplui import Theme, Frame
from epsilon.ui.uimanager import UIManager

from epsilon.frameworks.pygletframework import PygletFramework
from epsilon.core.settings import Settings

class UIBaseWindow(object):
    
    # Register this ui with the UIManager
    def __init__(self):
        # Get the Pyglet window
        pyglet_framework = PygletFramework.get_instance() 
        self._window = pyglet_framework.window
        
        # Configure the Settings for the GUI
        theme_path = 'simplui/themes/pywidget'
        theme_path = os.path.join(os.path.dirname(__file__), theme_path)
        self._themes = [Theme(theme_path)]
        
        res = Settings.get("DisplaySettings","resolution")
        
        self._frame = Frame(self._themes[0], w=res[0], h=res[1])
        self._window.push_handlers(self._frame)
        
        # Add this UI Window to the UIManager
        UIManager.get_instance().add_ui(self)

    def shutdown(self):
        # Remove this UI Window from the UIManager
        UIManager.get_instance().remove_ui(self)
    
    # Setup the window
    def setup(self):
        self._setup_ui()        
    
    # This functions will be overwritten by custom setup in child classes
    def _setup_ui(self):
        pass
    
    def draw(self):
        self._frame.draw()
    
    # These aren't connected yet. Not sure if these will be used or not.
    def on_frame_start(self):
        pass
    
    def on_frame_end(self):
        pass