'''
Created on Sep 20, 2011

@author: scottporter
'''
from Core import Time
from Scripting.Script import Script
from Geometry.euclid import Vector3, Quaternion
from Render import RenderCore

from pygame import *

import math

from Core import Input

class RotateScript(Script):
    
    def __init__(self, parent_node=None, rate=15):
        Script.__init__(self, 'RotateScript', parent_node)
        self._rate = rate
    
    def Init(self):
        pass
        
    def Start(self):
        pass
            
    def Update(self):
        up = Vector3(0,1,0)
        angle = self._rate * (math.pi/180)
        angle_inc = angle * Time.deltaTime
#        rot = self._node.transform.local_rotation
        if self._node:
            self._node.rotate( Quaternion().new_rotate_axis(angle_inc, up) )
        
#        self._node.translate( Vector3(1*Time.deltaTime,0,0))
        
    def Shutdown(self):
        pass
            
class MoveController(Script):
    
    def __init__(self, parent_node=None,speed=10,angle_speed=120):
        Script.__init__(self, 'MoveController', parent_node)
        self._speed = speed
        self._angle_speed = angle_speed
    
    def Update(self):
        
        if Input.GetKey(K_a):
            self._node.translate(  ( Vector3.RIGHT() * self._speed * Time.deltaTime ) )
        if Input.GetKey(K_d):
            self._node.translate(  ( Vector3.RIGHT() * -self._speed * Time.deltaTime ) )
        if Input.GetKey(K_w):
            self._node.translate( ( Vector3.FORWARD() * self._speed * Time.deltaTime ) )
        if Input.GetKey(K_s):
            self._node.translate( ( Vector3.FORWARD() * -self._speed * Time.deltaTime ) )
            
        if Input.GetKey(K_r):
            self._node.translate( ( Vector3.UP() * self._speed * Time.deltaTime ) )
        if Input.GetKey(K_f):
            self._node.translate( ( Vector3.UP() * -self._speed * Time.deltaTime ) )
        
        angle = self._angle_speed * Time.deltaTime
        angle = angle * (math.pi / 180 )
#        rot = self._node.rotation
        if Input.GetKey(K_q):
            self._node.rotate(Quaternion().rotate_axis(angle, Vector3(0,1,0)) )
            
        if Input.GetKey(K_e):
            self._node.rotate( Quaternion().rotate_axis(-angle, Vector3(0,1,0)) )
            
class CameraMoveController(MoveController):
    
    def Update(self):
        
        pos = self._node.position
        forward = self._node.forward
        
        # Mouse Controls
        angle = self._angle_speed * (math.pi / 180)
        angle = 0.002
        mx, my = Input.GetMouseMove()
        h_angle = angle * -mx
        v_angle = angle * my
        self._node.rotate(Quaternion().rotate_axis(h_angle, Vector3(0,1,0)) )
        self._node.rotate(Quaternion().rotate_axis(v_angle, Vector3(1,0,0)) )
        
        
        if hasattr( self._node, 'LookAt'):
            self._node.look_at = pos + ( forward * self._speed)
            
        MoveController.Update(self)
            
class DisplayCoordinate(Script):
    
    def __init__(self, parent_node=None):
        Script.__init__(self, 'DisplayCoordinate', parent_node)
        self._last_pos = Vector3()
    
    
    def Update(self):
#        if not self._node.transform.position == self._last_pos:
            self._last_pos = self._node.position 
            print self._node.name + ": " + str(self._last_pos)
            
class SettingsController(Script):
    
    def __init__(self, parent_node=None):
        Script.__init__(self, 'SettingsController', parent_node)
        self._wireframe = False
        self._grid = True 
        self._renderer = RenderCore.GetRenderCore()._renderer
    
    def Update(self):
        
        if Input.GetKeyDown(K_0):
            self._wireframe = not self._wireframe
            self._renderer.wireframe = self._wireframe
        
        if Input.GetKeyDown(K_9):
            self._grid = not self._grid
            self._renderer.grid = self._grid
    