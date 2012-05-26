'''
Created on Sep 20, 2011

@author: scottporter
'''
from epsilon.logging import Logger

from epsilon.core.basemanager import FrameListenerManager

# Manages all of the Script Objects loaded in the Engine.
class ScriptManager(FrameListenerManager):
    
    def init(self):
        Logger.Log("Created ScriptManager")
        self._scripts = []
        
    def __del__(self):
        self.shutdown()
    
    def shutdown(self):
        for script in self._scripts:
            script.shutdown()
    
    def on_frame_start(self):
        self.update()
    
    def add_script(self, new_script):
        self._scripts.append(new_script)
        
    # Remove the Script with the specified name
    def remove_script_by_name(self, name):
        found = False
        
        for script in self._scripts:
            if script.name == name:
                script.shutdown()
                found = True
                break
        if found:
            self._scripts.remove(script)
            
    # Remove the Script Object
    def remove_script(self, del_script):
        if del_script in self._scripts:
            del_script.shutdown()
            self._scripts.remove(del_script)
    
    # Run the Initialise function for each of the registered scripts
    def initialise_scripts(self):
        for script in self._scripts:
            script.init()
    
    # This is run only once before first call to update
    def start_scripts(self):
        for script in self._scripts:
            if not script._has_started:
                script.start()
                # This breaks the private member access theme but my python-foo isn't
                # strong enough to know of a better way to do this at this time
                script._has_started = True
    
    def update(self):
        for script in self._scripts:
            script.update()
            
        
    
    