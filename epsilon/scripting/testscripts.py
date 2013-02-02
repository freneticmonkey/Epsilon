'''
Created on Sep 20, 2011

@author: scottporter


NOTE: Considering giving scripts priority settings to move them within the
      ScriptManager's array -> higher priority = further towards the start
      of the array

'''

from epsilon.logging.logger import Logger

from epsilon.core.time import Time
from epsilon.core import settings
from epsilon.core.coreevents import QuitEvent
from epsilon.events.listenerbase import ListenerBase
from epsilon.scripting.script import Script
from epsilon.scripting.script import ScriptParamTypes
from epsilon.geometry.euclid import Vector3, Quaternion
from epsilon.render.rendermanager import RenderManager
from epsilon.render.transform import Space

#from pygame import *

import math

from epsilon.core.input import Input

from epsilon.ui.simplui import *
from epsilon.ui.uibasewindow import UIBaseWindow

from epsilon.scene.scenemanager import SceneManager

class MoveWindow(UIBaseWindow):
    def __init__(self, 
                 base_speed=10.0, 
                 max_speed=50.0,
                 angle_speed=120, 
                 max_angle_speed=720):

        self._base_speed = base_speed
        self._max_speed = max_speed

        self._base_angle_speed = angle_speed
        self._max_angle_speed = max_angle_speed

        self._current_speed = self._base_speed
        self._current_angle_speed = self._base_angle_speed

        self._camera = None

        UIBaseWindow.__init__(self)

    def _setup_ui(self):
        self._dialog = Dialogue('Camera Controls',
                                x=800,
                                y=250,
                                content=
                                VLayout(hpadding=5, 
                                        children=
                                        [
                                            Label('Camera Pos'),
                                            Label('x: 000.00 y: 000.00 z: 000.00', 
                                                  name='camera_pos_lbl'),
                                            Label('Speed: Current: %3.2f' % self._current_speed, 
                                                  name='camera_spd_lbl'),
                                            Slider(value=self._base_speed, 
                                                   min=0.01, 
                                                   max=self._max_speed, 
                                                   action=self.on_speed_scroll
                                                   ),
                                            Label('Angle Speed: Current: %3.2f' % self._current_angle_speed, 
                                                  name='camera_ang_spd_lbl'),
                                            Slider(value=self._base_angle_speed, 
                                                   min=1, 
                                                   max=self._max_angle_speed, 
                                                   action=self.on_angle_scroll),
                                            Button('Reset Camera', 
                                                   action=self.reset_camera),
                                        ])
                                )
        self._frame.add(self._dialog)
        self._camera_pos_label = self._frame.get_element_by_name('camera_pos_lbl')
        self._camera_spd_label = self._frame.get_element_by_name('camera_spd_lbl')
        self._camera_ang_spd_label = self._frame.get_element_by_name('camera_ang_spd_lbl')

    @property
    def speed(self):
        return self._current_speed

    @property
    def angle_speed(self):
        return self._current_angle_speed

    # UI Control Events
    def on_speed_scroll(self, slider):
        self._current_speed = slider.value
        self._camera_spd_label.text = 'Speed: Current: %3.2f' % self._current_speed

    def on_angle_scroll(self, slider):
        self._current_angle_speed = slider.value
        self._camera_ang_spd_label.text = 'Angle Speed: Current: %3.2f' % self._current_angle_speed

    def reset_camera(self, button):
        if self._camera is None:
            self._camera = SceneManager.get_instance().current_scene.active_camera

        if not self._camera is None:
            self._camera.node_parent.transform.position = Vector3(0, 1, -300)
            if hasattr( self._camera, 'look_at_position'):
                self._camera.node_parent.transform.rotation = Quaternion()
                self._camera.look_at_position = Vector3(0,0,0)


    def draw(self):
        if self._camera is None:
            self._camera = SceneManager.get_instance().current_scene.active_camera
        
        if not self._camera is None:
            pos = self._camera.node_parent.transform.position
            self._camera_pos_label.text = "x: %3.2f y: %3.2f z: %3.2f" % (pos.x, pos.y, pos.z) 
        self._frame.draw()
    

class RotateScript(Script):
    
    def __init__(self, parent_node=None, rate=15, axis=Vector3(0,1,0)):
        Script.__init__(self, 'RotateScript', parent_node)
        self._param_types = {"rate": ScriptParamTypes.FLOAT, 
                             "axis": ScriptParamTypes.VEC3 
                            }
        self._rate = rate
        self._axis = axis
            
    def update(self):
        angle = self._rate * (math.pi/180)
        angle_inc = angle * Time.delta_time
#        rot = self._node.transform.local_rotation
        if self._node:
            self._node.transform.rotate( Quaternion().new_rotate_axis(angle_inc, self._axis) )
        
#        self._node.translate( Vector3(1*Time.deltaTime,0,0))
        
    def Shutdown(self):
        pass
            
class MoveController(Script, ListenerBase):
    event_types = ['MouseEnterUI','MouseExitUI']
    def __init__(self, parent_node=None,speed=10,adj_speed=5,angle_speed=120):
        Script.__init__(self, name='MoveController', parent_node=parent_node)
        ListenerBase.__init__(self, event_types=self.event_types)
        
        self._param_types = {"speed":ScriptParamTypes.FLOAT, 
                             "adj_speed":ScriptParamTypes.FLOAT, 
                             "angle_speed": ScriptParamTypes.FLOAT 
                            }
        
        self._speed = speed
        self._angle_speed = angle_speed
        self._adj_speed = adj_speed
        
        self._final_speed = speed
        
        self._mouse_over_ui = False
        self._unlock_mouse = False

    # exposing for ui modification
    @property
    def speed(self):
        return self._final_speed

    @speed.setter
    def speed(self, new_speed):
        self._final_speed = new_speed

    @property
    def angle_speed(self):
        return self._angle_speed

    @angle_speed.setter
    def angle_speed(self, new_angle_speed):
        self._angle_speed = new_angle_speed
    
    def _process_event(self, new_event):
        if new_event.name == 'MouseEnterUI':
            self._mouse_over_ui = True
        elif new_event.name == 'MouseExitUI':
            self._mouse_over_ui = False
    
    def update(self):
        
        if not self._mouse_over_ui:
            # If the left mouse button is down
            mouse_left_down = Input.get_mouse_left()
            
            # If the left mouse is down 
            if mouse_left_down:
                
                if not self._unlock_mouse:
                    Input.set_lock_mouse(True)
                self._unlock_mouse = True
#                # Hide the cursor
#                #mouse.set_visible(False)
#                
#                # And its not the initial frame
#                if not self._initial_mouse_down:
#                    # Reset the mouse position to the centre of the screen
#                    #self._mouse_x, self._mouse_y = mouse.get_pos()
#                    self._mouse_x, self._mouse_y = Input.get_mouse_move()
#                    self._mouse_x -= self._h_res[0]
#                    self._mouse_y -= self._h_res[1]
#                    Input.set_mouse_pos(self._mouse_x, self._mouse_y)
#                else:
#                    self._initial_mouse_down = False
#                    Input.set_mouse_pos(0, 0)
#                    
#                #mouse.set_pos(self._h_res[0],self._h_res[1])
#                Input.set_mouse_pos(self._h_res[0],self._h_res[1])
#                
#                self._initial_mouse_up = True
                
                # Handle Keyboard
                
                # Handle adjusting normal speed
                if Input.get_key(Input.KEY_BACKSLASH):
                    self._final_speed -= self._adj_speed * Time.delta_time
                    if self._final_speed < 0:
                        self._final_speed = self._adj_speed
                    
                if Input.get_key(Input.KEY_EQUALS):
                    self._final_speed += self._adj_speed * Time.delta_time 
                    
                applied_speed = self._final_speed
                    
                # Handle temporary speed boost
                if Input.get_key(Input.KEY_LEFT_SHIFT):
                    applied_speed *= 10.0
                
                if Input.get_key(Input.KEY_A):
                    self._node.transform.translate(  ( Vector3.RIGHT() * applied_speed * Time.delta_time ) )
                if Input.get_key(Input.KEY_D):
                    self._node.transform.translate(  ( Vector3.RIGHT() * -applied_speed * Time.delta_time ) )
                if Input.get_key(Input.KEY_W):
                    self._node.transform.translate( ( Vector3.FORWARD() * applied_speed * Time.delta_time ) )
                if Input.get_key(Input.KEY_S):
                    self._node.transform.translate( ( Vector3.FORWARD() * -applied_speed * Time.delta_time ) )
                    
                if Input.get_key(Input.KEY_R):
                    self._node.transform.translate( ( Vector3.UP() * applied_speed * Time.delta_time ) )
                if Input.get_key(Input.KEY_F):
                    self._node.transform.translate( ( Vector3.UP() * -applied_speed * Time.delta_time ) )
                
                angle = self._angle_speed * Time.delta_time
                angle = angle * (math.pi / 180 )
                
                if Input.get_key(Input.KEY_Q):
                    self._node.transform.rotate(Quaternion().rotate_axis(angle, Vector3(0,1,0)) )
                    
                if Input.get_key(Input.KEY_E):
                    self._node.transform.rotate( Quaternion().rotate_axis(-angle, Vector3(0,1,0)) )
                
            else:
                if self._unlock_mouse:
                    Input.set_lock_mouse(False)
                    self._unlock_mouse = False
#                self._initial_mouse_down = True
#                if self._initial_mouse_up:
#                    # Show the cursor
#                    #mouse.set_visible(True)
#                    self._initial_mouse_up = False
            
class CameraMoveController(MoveController):
    def __init__(self, 
                 parent_node=None,
                 speed=10,
                 angle_speed=120,
                 mouse_speed_x=0.002, 
                 mouse_speed_y=0.002,
                 mouse_y_invert=False): # This should be in the Settings object.
        super(CameraMoveController, self).__init__(parent_node,speed=speed,angle_speed=angle_speed)
        
        self._param_types = {"speed":ScriptParamTypes.FLOAT, 
                             "angle_speed": ScriptParamTypes.FLOAT,
                             "mouse_speed_x": ScriptParamTypes.FLOAT,
                             "mouse_speed_y": ScriptParamTypes.FLOAT,
                             "mouse_y_invert": ScriptParamTypes.BOOL 
                            }
        
        self._mouse_speed_x = mouse_speed_x
        self._mouse_speed_y = mouse_speed_y
        self._mouse_y_invert = mouse_y_invert
        
        if self._mouse_y_invert:
            self._mouse_speed_y = -self._mouse_speed_y

        self._ui = MoveWindow(base_speed=speed, angle_speed=angle_speed)
    
    def update(self):
        # Get UI values
        self.speed = self._ui.speed
        self.angle_speed = self._ui.angle_speed

        super(CameraMoveController, self).update()

        if Input.get_mouse_left() and not self._mouse_over_ui:
            
            pos = self._node.transform.position
            forward = self._node.transform.forward
            
            mx, my = Input.get_mouse_move_relative()
            # FIXME: HACK to prevent immediate jump on initial mouse movement
            if math.fabs(mx) < 60.0 and math.fabs(my) < 60.0: # <== This makes mouse movement feel like 
                                                              # it's moving through molasses
                h_angle = self._mouse_speed_x * -mx
                v_angle = self._mouse_speed_y * -my
                
                self._node.transform.rotate(Quaternion().rotate_axis(h_angle, self._node.transform.up), Space.PARENT )
                self._node.transform.rotate(Quaternion().rotate_axis(v_angle, self._node.transform.right), Space.PARENT )

                #self._node.transform.rotate(Quaternion().rotate_axis(h_angle, Vector3(0,1,0)), Space.PARENT )
                #self._node.transform.rotate(Quaternion().rotate_axis(v_angle, Vector3(1,0,0)), Space.PARENT )
                
                self._node.camera.look_at_position = pos + ( forward * self._speed)
            
class DisplayCoordinate(Script):
    
    def __init__(self, parent_node=None):
        Script.__init__(self, 'DisplayCoordinate', parent_node)
        self._last_pos = Vector3()
    
    
    def update(self):
#        if not self._node.transform.position == self._last_pos:
            self._last_pos = self._node.transform.position 
            print self._node.name + ": " + str(self._last_pos)
    
class SettingsController(Script):
    
    def __init__(self, parent_node=None):
        Script.__init__(self, 'SettingsController', parent_node)
        self._wireframe = False
        self._grid = True 
        self._renderer = RenderManager.get_instance()._renderer
        self._quit_detected = False
        
        Logger.Log("Initialised Settings Controller")
    
    def update(self):
        
        if Input.get_key_down(Input.KEY_0):
            self._wireframe = not self._wireframe
            self._renderer.wireframe = self._wireframe
        
        if Input.get_key_down(Input.KEY_9):
            self._grid = not self._grid
            self._renderer.grid = self._grid
            
        if Input.get_key_down(Input.KEY_ESCAPE) or Input.get_quit_detected():
            # Fire a Quit Event
            QuitEvent().send()
            
        
    