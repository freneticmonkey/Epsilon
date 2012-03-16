'''
Created on Sep 20, 2011

@author: scottporter


NOTE: Considering giving scripts priority settings to move them within the
      ScriptManager's array -> higher priority = further towards the start
      of the array

'''

from Logging import Logger

from Core import Time
from Core import Settings
from Events.EventBase import EventBase
from Events.ListenerBase import ListenerBase
from Scripting.Script import Script
from Scripting.Script import ScriptParamTypes
from Geometry.euclid import Vector3, Quaternion
from Render.RenderManager import RenderManager

from pygame import *

import math

from Core.Input import Input

class RotateScript(Script):
    
    def __init__(self, parent_node=None, rate=15, axis=Vector3(0,1,0)):
        Script.__init__(self, 'RotateScript', parent_node)
        self._param_types = {"rate":ScriptParamTypes.FLOAT, 
                             "axis": ScriptParamTypes.VEC3 
                            }
        self._rate = rate
        self._axis = axis
        
    
    def Init(self):
        pass
        
    def Start(self):
        pass
            
    def Update(self):
        angle = self._rate * (math.pi/180)
        angle_inc = angle * Time.delta_time
#        rot = self._node.transform.local_rotation
        if self._node:
            self._node.rotate( Quaternion().new_rotate_axis(angle_inc, self._axis) )
        
#        self._node.translate( Vector3(1*Time.deltaTime,0,0))
        
    def Shutdown(self):
        pass
            
class MoveController(Script, ListenerBase):
    event_types = ['MouseEnterUI','MouseExitUI']
    def __init__(self, parent_node=None,speed=10,angle_speed=120):
        Script.__init__(self, name='MoveController', parent_node=parent_node)
        ListenerBase.__init__(self, eventTypes=self.event_types)
        
        self._param_types = {"speed":ScriptParamTypes.FLOAT, 
                             "angle_speed": ScriptParamTypes.FLOAT 
                            }
        
        self._speed = speed
        self._angle_speed = angle_speed
        
        self._initial_mouse_down = False
        self._initial_mouse_up = False
        self._res = Settings.DisplaySettings.resolution
        self._h_res = [self._res[0]/2, self._res[1]/2]
        mouse.set_visible(True)
        
        self._mouse_over_ui = False
        
        Logger.Log("Initialised MoveController")
    
    def _processEvent(self, new_event):
        if new_event.name == 'MouseEnterUI':
            self._mouse_over_ui = True
        elif new_event.name == 'MouseExitUI':
            self._mouse_over_ui = False
    
    def Update(self):
        
        if not self._mouse_over_ui:
            # If the left mouse button is down
            mouse_left_down = Input.get_mouse_left()
            
            # If the left mouse is down 
            if mouse_left_down:
                # Hide the cursor
                mouse.set_visible(False)
                
                # And its not the initial frame
                if not self._initial_mouse_down:
                    # Reset the mouse position to the centre of the screen
                    self._mouse_x, self._mouse_y = mouse.get_pos()
                    self._mouse_x -= self._h_res[0]
                    self._mouse_y -= self._h_res[1]
                    Input.set_mouse_pos(self._mouse_x, self._mouse_y)
                else:
                    self._initial_mouse_down = False
                    Input.set_mouse_pos(0, 0)
                mouse.set_pos(self._h_res[0],self._h_res[1])
                self._initial_mouse_up = True
                
                # Handle Keyboard
                if Input.get_key(K_a):
                    self._node.translate(  ( Vector3.RIGHT() * self._speed * Time.delta_time ) )
                if Input.get_key(K_d):
                    self._node.translate(  ( Vector3.RIGHT() * -self._speed * Time.delta_time ) )
                if Input.get_key(K_w):
                    self._node.translate( ( Vector3.FORWARD() * self._speed * Time.delta_time ) )
                if Input.get_key(K_s):
                    self._node.translate( ( Vector3.FORWARD() * -self._speed * Time.delta_time ) )
                    
                if Input.get_key(K_r):
                    self._node.translate( ( Vector3.UP() * self._speed * Time.delta_time ) )
                if Input.get_key(K_f):
                    self._node.translate( ( Vector3.UP() * -self._speed * Time.delta_time ) )
                
                angle = self._angle_speed * Time.delta_time
                angle = angle * (math.pi / 180 )
        #        rot = self._node.rotation
                if Input.get_key(K_q):
                    self._node.rotate(Quaternion().rotate_axis(angle, Vector3(0,1,0)) )
                    
                if Input.get_key(K_e):
                    self._node.rotate( Quaternion().rotate_axis(-angle, Vector3(0,1,0)) )
                
            else:
                self._initial_mouse_down = True
                if self._initial_mouse_up:
                    # Show the cursor
                    mouse.set_visible(True)
                    self._initial_mouse_up = False
            
class CameraMoveController(MoveController):
    def __init__(self, parent_node=None,speed=10,angle_speed=120):
        super(CameraMoveController, self).__init__(parent_node,speed,angle_speed)
        
        self._param_types = {"speed":ScriptParamTypes.FLOAT, 
                             "angle_speed": ScriptParamTypes.FLOAT 
                            }
    
    def Update(self):
        super(CameraMoveController, self).Update()
        
        if Input.get_mouse_left() and not self._mouse_over_ui:
            pos = self._node.position
            forward = self._node.forward
            
            # Mouse Controls
    #        angle = self._angle_speed * (math.pi / 180)
            angle = 0.002
            mx, my = Input.get_mouse_move()
            h_angle = angle * -mx
            v_angle = angle * my
            self._node.rotate(Quaternion().rotate_axis(h_angle, Vector3(0,1,0)) )
            self._node.rotate(Quaternion().rotate_axis(v_angle, Vector3(1,0,0)) )
            
            
            if hasattr( self._node, 'LookAt'):
                self._node.look_at = pos + ( forward * self._speed)
            
            
class DisplayCoordinate(Script):
    
    def __init__(self, parent_node=None):
        Script.__init__(self, 'DisplayCoordinate', parent_node)
        self._last_pos = Vector3()
    
    
    def Update(self):
#        if not self._node.transform.position == self._last_pos:
            self._last_pos = self._node.position 
            print self._node.name + ": " + str(self._last_pos)

class QuitEvent(EventBase):
    def __init__(self):
        EventBase.__init__(self, 'Quit', True)
    
class SettingsController(Script):
    
    def __init__(self, parent_node=None):
        Script.__init__(self, 'SettingsController', parent_node)
        self._wireframe = False
        self._grid = True 
        self._renderer = RenderManager.get_instance()._renderer
        self._quit_detected = False
    
    def Update(self):
        
        if Input.get_key_down(K_0):
            self._wireframe = not self._wireframe
            self._renderer.wireframe = self._wireframe
        
        if Input.get_key_down(K_9):
            self._grid = not self._grid
            self._renderer.grid = self._grid
            
        if Input.get_key_down(K_ESCAPE) or Input.get_quit_detected():
            # Fire a Quit Event
            QuitEvent().Send()
            
        
    