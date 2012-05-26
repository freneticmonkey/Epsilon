'''
Created on May 23, 2012

Description: For lack of a better name this is the Main UI. It is built using Simpleui which inturn requires
             Pyglet.

@author: scottporter
'''

from UI.simplui import *

from Frameworks.PygletFramework import PygletFramework
from Core import Settings
from Logging import Logger
from Core.CoreEvents import QuitEvent

from Render.RenderEvents import ToggleWireFrameEvent, ToggleGridEvent
from Events.ListenerBase import ListenerBase

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

class MainUI(object):
    
    def __init__(self):
        pass
    
    def setup(self):
        # Get the Pyglet window
        pyglet_framework = PygletFramework.get_instance() 
        self._window = pyglet_framework.window
        
        # Configure the Settings for the GUI
        self._themes = [Theme('UI/simplui/themes/pywidget')]
        
        res = Settings.DisplaySettings.resolution
        self._frame = Frame(self._themes[0], w=res[0], h=res[1])
        self._window.push_handlers(self._frame)
        
        self._build_ui()
        
        self._listener = UIListener(self)
        
    def _build_ui(self):
        
        stats_layout = FoldingBox('stats', content=
                        # each box needs a content layout
                        VLayout(children =
                        [
                            Label('0.0 fps', name='fps_label'),
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
    
    # UI Control Events
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
        self._frame.draw()
    
        
