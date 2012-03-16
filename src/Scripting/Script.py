'''
Created on Sep 20, 2011

@author: scottporter
'''
from Scripting.ScriptManager import ScriptManager
from Core import Input
from pygame import *
from Geometry.euclid import Vector2, Vector3

# This is the base class that all Scripts inherit from

class ScriptParamTypes:
    INT     = "int"
    FLOAT   = "float"
    DOUBLE  = "double"
    STR     = "str"
    VEC2    = "vec2"
    VEC3    = "vec3"

# Script node notes
# =================
# As part of the scene loading implementation scripts can now be attached
# to nodes within the XML scene definition.  In order for the default 
# parameters of the Script nodes to be set from the XML they must be cast
# into the correct type.  For this to happen the following features need
# to be added to classes inheriting from Script.
#
# the parameter names for the initialise functions must be identical to
# the internal name of the object, WITHOUT the underscore prefix. 
#
# E.g.
# def __init__(self, parent_node=None, rate=15):
#    Script.__init__(self, parent_node)
#    self._rate = rate    <============== 

# Also if scripts have parameters they MUST define the 
# types of their parameters within the self._param_types dictionary
# using the parameter name not the internal name.
#
# E.g. Using the class above again
#  
# def __init__(self, parent_node=None, rate=15):
#    Script.__init__(self, parent_node)
#    self._rate = rate
#    self._param_types = { "rate": ScriptParamTypes.FLOAT } <========
#

class Script(object):
    
    def __init__(self, name, parent_node=None):
        # Set the Script's name
        self._name = name
        # The Node that the script is attached to.
        self._node = parent_node
        # This indicates whether Start has been called
        self._has_started = False
        # This holds the types of each of the parameters for the script
        self._param_types = {}
        
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
            
    def init_parameters(self, params):
        for key in params:
            parameter_name = key
            internal_name = "_"+key 
            if parameter_name in self._param_types:
                thetype = self._param_types[parameter_name]
                
                if thetype == ScriptParamTypes.STR:
                    setattr(self, internal_name, params[parameter_name])
                elif thetype == ScriptParamTypes.INT:
                    setattr(self, internal_name, int(params[parameter_name]))
                elif thetype == ScriptParamTypes.FLOAT:
                    setattr(self, internal_name, float(params[parameter_name]))
                elif thetype == ScriptParamTypes.VEC2:
                    xy = params[parameter_name].split(" ")
                    setattr(self, internal_name, Vector2(float(xy[0]), float(xy[1])))
                elif thetype == ScriptParamTypes.VEC3:
                    xyz = params[parameter_name].split(" ")
                    setattr(self, internal_name, Vector3(float(xyz[0]), float(xyz[1]), float(xyz[2])))
        
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
    
    