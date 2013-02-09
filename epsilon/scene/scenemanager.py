'''
Created on Sep 17, 2011

@author: scottporter
'''

from epsilon.events.listenerbase import *
from epsilon.core.basemanager import BaseSingleton

# Events used by the SceneManager
class SceneManagerEvents:
    events = ['CameraAdded',
              'CameraRemoved',
              'SetActive',
              'LightAdded',
              'LightRemoved'
             ]
    
# This class holds all of the scenes objects.
# It performs any scene culling on objects that don't need
# to be sent to the Card

class SceneManager(BaseSingleton):
    
    @classmethod
    def get_current_scene(cls):
        return cls.get_instance().current_scene

    def __init__(self):
        #self._root = None
        #self._cameras = []
        #self._lights = []
        self._active_camera = None
        self._scenes = []
        self._current_scene = None
        
    def init(self):
#        self._root = Node(name='scene_root')
#        self._scene_listener = SceneManagerListener()
        pass
    
#    @property
#    def root(self):
#        return self._root
    
    def add_scene(self, new_scene):
        if not len(self._scenes):
            self._current_scene = new_scene
            new_scene.active = True
        self._scenes.append(new_scene)
        
    def remove_scene(self, del_scene):
        if del_scene == self._current_scene:
            self._current_scene.active = False
            self._current_scene = None
        self._scenes.remove(del_scene)

    @property
    def scenes(self):
        return self._scenes
    
    @property
    def current_scene(self):
        return self._current_scene
    
    def update(self):
        # Update the scenegraph transforms.
        if not self._current_scene is None:
            self._current_scene.update()
            
        # Cull invisible geometry
        if not self._current_scene is None:
            self._current_scene.cull()
        
        
    
class SceneManagerListener(ListenerBase):

    def __init__(self):
        ListenerBase.__init__(self, SceneManagerEvents.events)
        self._sm = SceneManager.get_instance()
        
    def _process_event(self, new_event):
        if new_event.name == 'CameraAdded':
            self._sm.AddCamera(new_event.data )
        elif new_event.name == 'CameraRemoved':
            self._sm.RemoveCamera(new_event.data)
        elif new_event.name == 'SetActive':
            self._sm.SetActiveCamera(new_event.data)
        if new_event.name == 'LightAdded':
            self._sm.AddLight(new_event.data )
        elif new_event.name == 'LightRemoved':
            self._sm.RemoveLight(new_event.data)