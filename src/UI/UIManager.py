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
            
        # A python console
        self._console = pyui.dialogs.Console(10,10,400,400)
        
        # Stats dialog
        height = 100
        buffer = 10
        width = 200
        x = buffer
        y = DisplaySettings.resolution[1]-(height+buffer)
        # Position at the bottom of the screen
        #self._stats = pyui.widgets.Frame(x,y,width,height, "Render Stats")
        #self._stats = pyui.dialogs.StdDialog("Render Stats:", "Some stats here")#x,y,width,height, "Render Stats")
        
    @property
    def stats_dialog(self):
        return self._stats
    
    def draw(self):
        pyui.draw()
        pyui.update_epsilon()
        
    def on_frame_start(self):
        pass
    
    def on_frame_end(self):
        pass