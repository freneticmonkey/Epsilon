'''
Created on Feb 4, 2012

@author: scottporter
'''
from epsilon.core.basemanager import FrameListenerManager
from epsilon.logging.logger import Logger
from epsilon.core.settings import DisplaySettings

class UIManager(FrameListenerManager):
    def init(self):
        Logger.Log("Created UIManager")
        self._ui_list = []
                
    # TODO: Add layer management?
    def add_ui(self, new_ui):
        self._ui_list.append(new_ui)
        
        new_ui.setup()
        
    def remove_ui(self, del_ui):
        if del_ui in self._ui_list:
            self._ui_list.remove(del_ui)

    def draw(self):
        for ui in self._ui_list:
            ui.draw()
        
    def on_frame_start(self):
        pass
    
    def on_frame_end(self):
        pass