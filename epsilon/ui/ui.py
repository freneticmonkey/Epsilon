'''
Created on May 23, 2012

Description: For lack of a better name this is the Main UI. It is built using Simpleui which inturn requires
             Pyglet.

@author: scottporter
'''
from epsilon.ui.simplui import *
from epsilon.ui.uibasewindow import UIBaseWindow
from epsilon.core.time import Time

from epsilon.logging.logger import Logger
from epsilon.core.coreevents import QuitEvent

from epsilon.render.renderevents import ToggleWireFrameEvent, ToggleGridEvent
from epsilon.events.listenerbase import ListenerBase

from epsilon.scene.scenemanager import SceneManager
from epsilon.geometry.euclid import Vector3, Quaternion

class UIListener(ListenerBase):
    event_types = ['MouseEnterUI','MouseExitUI']
    def __init__(self, ui):
        ListenerBase.__init__(self, event_types=self.event_types)
        self._ui = ui
        
    def _process_event(self, new_event):
        if not self._ui is None:
            if new_event.name == 'MouseEnterUI':
                self._ui.set_mouse_over(True)
            elif new_event.name == 'MouseExitUI':
                self._ui.set_mouse_over(False)

class MainUI(UIBaseWindow):
        
    def _setup_ui(self):
        
        self._camera = None
        
        self._listener = UIListener(self)
        self._build_ui()
        
    def _build_ui(self):
        
        stats_layout = FoldingBox('stats', content=
                        # each box needs a content layout
                        VLayout(children =
                        [
                            Label('0000.0 fps', name='fps_label'),
                            Label('Camera Pos'),
                            Label('x: 000.00 y: 000.00 z: 000.00', name='camera_pos_label'),
                            HLayout(children=
                            [
                                Label('MoUI:', hexpand=False),
                                Label('', name='mouse_over')
                            ]),
                            ])
                        )
        
        settings_layout = FoldingBox('settings', content=
                                VLayout(children=
                                [
                                    # a checkbox, note the action function is provided directly
                                    Checkbox('Show wireframe', h=100, action=self.show_wireframe_action),
                                    Checkbox('Show Grid', h=100, action=self.show_grid_action),
                                    Button('Reset Camera', action=self.reset_camera),
                                    Button('Quit', action=self.quit_action),
                                ])
                            )
        
        self._dialog = Dialogue('Inspector',
                                x=20,
                                y=550, 
                                content=
                                VLayout(autosizex=True, 
                                        hpadding=0, 
                                        children=
                                        [
                                         stats_layout,
                                         settings_layout
                                        ])
                                )
        
        self._console = Dialogue('Python console', 
                                 x=20, 
                                 y=110,
                                 content=VLayout(autosizex=True,
                                                 hpadding=0,
                                                 children=
                                                 [
                                                    Label('text\nsome\nthing',w=390, h=300),
                                                    TextInput(text=">>>", w=390)
                                                 ]))
        
        self._frame.add(self._dialog)
        # Disabled until a console is written
        #self._frame.add(self._console)
        
        self._mouse_over_label = self._frame.get_element_by_name('mouse_over')
        self._fps_label = self._frame.get_element_by_name('fps_label')
        self._camera_pos_label = self._frame.get_element_by_name('camera_pos_label')
    
    # UI Control Events
    def reset_camera(self, button):
        if self._camera is None:
            self._camera = SceneManager.get_instance().current_scene.active_camera
        self._camera.position = Vector3(2, 1, -10)
        if hasattr( self._camera, 'LookAt'):
            self._camera.look_at_position = Vector3(0,0,0)
    
    def button_action(self, button):
        Logger.Log("A button was clicked!")
        
    def show_wireframe_action(self, checkbox):
        ToggleWireFrameEvent(checkbox.value).send()
        
    def show_grid_action(self, checkbox):
        ToggleGridEvent(checkbox.value).send()
        
    def quit_action(self, button):
        QuitEvent().send()
        
    # UIListener accessors
    def set_mouse_over(self, mouse_over):
        text = "Mouse Off"
        if mouse_over:
            text = "Mouse On"
        
        if not self._mouse_over_label is None:
            self._mouse_over_label.text = text
        
    def draw(self):
        #self._window.clear()
        self._fps_label.text = "FPS: %3.2f " % Time.fps
        
        if self._camera is None:
            self._camera = SceneManager.get_instance().current_scene.active_camera
        
        if not self._camera is None:
            pos = self._camera.node_parent.transform.position
            self._camera_pos_label.text = "x: %3.2f y: %3.2f z: %3.2f" % (pos.x, pos.y, pos.z) 
        self._frame.draw()
    
        
