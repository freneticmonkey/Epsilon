'''
Created on Feb 4, 2012

@author: scottporter
'''
from epsilon.core.basemanager import FrameListenerManager
from epsilon.logging import Logger
from epsilon.core.settings import DisplaySettings
#import pyui

from epsilon.ui.ui import MainUI

class UIManager(FrameListenerManager):
    def init(self):
        Logger.Log("Created UIManager")
        self._ui = MainUI()
        
        self._ui.setup()
        # Initialise GUI Sub-system
        #pyui.init(DisplaySettings.resolution[0],DisplaySettings.resolution[1], "p3d", DisplaySettings.fullscreen)
            
        # A python console
        #self._console = pyui.dialogs.Console(10,10,400,400)
        
        # Stats dialog
        height = 100
        buffer = 10
        width = 200
        x = buffer
        y = DisplaySettings.resolution[1]-(height+buffer)
        # Position at the bottom of the screen
        #self._stats = pyui.widgets.Frame(x,y,width,height, "Render Stats")
        #self._stats = pyui.dialogs.StdDialog("Render Stats:", "Some stats here")#x,y,width,height, "Render Stats")
        
#    @property
#    def stats_dialog(self):
#        return self._stats
#    
    def draw(self):
        self._ui.draw()
#        pyui.draw()
#        pyui.update_epsilon()
        
    def on_frame_start(self):
        pass
    
    def on_frame_end(self):
        pass