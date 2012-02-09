'''
Created on Feb 4, 2012

@author: scottporter
'''
from Core.BaseManager import FrameListenerManager
from Logging import Logger
from Core.Settings import DisplaySettings
import pyui

class UIManager(FrameListenerManager):
    def init(self):
        Logger.Log("Created UIManager")
        
        # Initialise GUI Sub-system
        pyui.init(DisplaySettings.resolution[0],DisplaySettings.resolution[1], "p3d", DisplaySettings.fullscreen)
            
        # Create a default window
        #frame = pyui.widgets.Frame(10,10,200,200, "hello world")#, theme=self._desktop.theme)
        self._console = pyui.dialogs.Console(10,10,400,400)
    
    def draw(self):
        pyui.draw()
        pyui.update_epsilon()
        
    def on_frame_start(self):
        pass
    
    def on_frame_end(self):
        pass