'''
Created on Sep 20, 2011

@author: scottporter
'''
from Logging import Logger

from Core.BaseManager import FrameListenerManager

# Manages all of the Script Objects loaded in the Engine.
class ScriptManager(FrameListenerManager):
    
    def init(self):
        Logger.Log("Created ScriptManager")
        self._scripts = []
        
    def __del__(self):
        self.Shutdown()
    
    def Shutdown(self):
        for script in self._scripts:
            script.Shutdown()
    
    def on_frame_start(self):
        self.Update()
    
    def AddScript(self, new_script):
        self._scripts.append(new_script)
        
    # Remove the Script with the specified name
    def RemoveScriptByName(self, name):
        found = False
        
        for script in self._scripts:
            if script.name == name:
                script.Shutdown()
                found = True
                break
        if found:
            self._scripts.remove(script)
            
    # Remove the Script Object
    def RemoveScript(self, del_script):
        if del_script in self._scripts:
            del_script.Shutdown()
            self._scripts.remove(del_script)
    
    # Run the Initialise function for each of the registered scripts
    def InitialiseScripts(self):
        for script in self._scripts:
            script.Init()
    
    # This is run only once before first call to update
    def StartScripts(self):
        for script in self._scripts:
            if not script._has_started:
                script.Start()
                # This breaks the private member access theme but my python-foo isn't
                # strong enough to know of a better way to do this at this time
                script._has_started = True
    
    def Update(self):
        for script in self._scripts:
            script.Update()
            
        
    
    