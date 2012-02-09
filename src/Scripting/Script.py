'''
Created on Sep 20, 2011

@author: scottporter
'''
from Scripting.ScriptManager import ScriptManager
from Core import Input
from pygame import *

# This is the base class that all Scripts inherit from

class Script(object):
    
    def __init__(self, name, parent_node=None):
        # Set the Script's name
        self._name = name
        # The Node that the script is attached to.
        self._node = parent_node
        # This indicates whether Start has been called
        self._has_started = False
        
        self._check_valid_node() 
            
    # This function checks whether the Script is correctly attached
    # to a Node object or not.  This way the Script is only active
    # if attached to a valid Node.
    def _check_valid_node(self):
        if self._node:
            # Add the Script to the ScriptManager
            ScriptManager.get_instance().AddScript(self)
        else:
            ScriptManager.get_instance().RemoveScript(self)
        
    @property
    def name(self):
        return self._name
    
    @property
    def node(self):
        return self._node
    
    @node.setter
    def node(self, parent):
        self._node = parent
        self._check_valid_node()
    
    def Init(self):
        pass
    
    def Start(self):
        pass
    
    def Update(self):
        pass
    
    def Shutdown(self):
        pass
    
    