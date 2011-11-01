'''
Created on Sep 17, 2011

@author: scottporter
'''

from Scene.Node import Node
from Events.ListenerBase import *

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
#1
_instance = None

def GetSceneManager():
    global _instance
    if _instance is None:
        _instance = SceneManager()
    return _instance

class SceneManager(object):
    
    def __init__(self):
        self._root = None
        self._cameras = []
        self._active_camera = None
        
        self._lights = []
        
    def Init(self):
        self._root = Node(name='scene_root')
        self._scene_listener = SceneManagerListener()
        
    @property
    def root(self):
        return self._root
    
    def Update(self):
        if self._root._need_child_update or \
           self._root._need_parent_update or \
           len(self._root._children_to_update) > 0:
            # Update the Transform Nodes within the Scene
            self._root._Update(True, False)
    
    @property
    def cameras(self):
        return self._cameras
    
    @property
    def active_camera(self):
        return self._active_camera
    
    @property
    def lights(self):
        return self._lights
    
    # Add the camera parameter to the list of known cameras in the scene
    def AddCamera(self, new_camera):
        # If the camera isn't already on the list of cameras
        if not new_camera in self._cameras:
            self._cameras.append(new_camera)
            # If the camera is the only camera listed, it becomes the
            # active camera by default
            if len(self._cameras) == 1:
                self._active_camera = self._cameras[0]
            
    # Remove the camera param from the list of known cameras in the scene.
    def RemoveCamera(self, rm_camera):
        if rm_camera in self._cameras:
            self._cameras.remove(rm_camera)
            
            # If there is only a single camera in the scene, it becomes the
            # active camera by default
            self._active_camera = self._cameras[0]
            
    # Set the camera parameter as the scenes active camera
    def SetActiveCamera(self, active_camera):
        # If the camera is amongst the cameras that the SceneManager is aware of
        if active_camera in self._cameras:
            # Set all other cameras to be inactive
            for camera in self._cameras:
                camera.active = (camera==active_camera)
            # Set the SceneManagers active camera to be the parameter
            self._active_camera = active_camera       
            
    # Add the light parameter to the list of known lights in the scene
    def AddLight(self, new_light):
        # If the light isn't already on the list of lights
        if not new_light in self._lights:
            self._lights.append(new_light)
            
    # Remove the light param from the list of known lights in the scene.
    def RemoveLight(self, rm_light):
        if rm_light in self._lights:
            self._lights.remove(rm_light)
    

class SceneManagerListener(ListenerBase):

    def __init__(self):
        ListenerBase.__init__(self, SceneManagerEvents.events)
        self._sm = GetSceneManager()
        
    def _processEvent(self, new_event):
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