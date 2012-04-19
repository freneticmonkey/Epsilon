'''
Created on Mar 4, 2012

@author: scottporter
'''

from Resource.ResourceBase import ResourceBase, ResourceType

from Scene.Node import Node
from Events.ListenerBase import ListenerBase

class SceneBase(ResourceBase):
    
    def __init__(self, filename="", name="", root=None):
        ResourceBase.__init__(self)
        self._resource_type = ResourceType.SCENE
        
        # Scene Properties
        if root is None:
            self._root = Node(name="scene_root",scene=self)
        else:
            if isinstance(root, Node):
                self._root = root
                self._loaded = True
            #else:
                # root not is not assigned because it isn't a Node object
        self._cameras = []
        self._lights = []
        self._active_camera = None
        
        self._active = False
        
        self._scene_listener = SceneBaseListener(self)
        
    @property
    def root(self):
        return self._root
    
    @root.setter
    def root(self, new_root):
        if isinstance(new_root, Node):
            # delete the old root here?
            self._root = new_root
            self._loaded = True
            
    @property
    def need_update(self):
        return self._root.need_update
    
    def update(self, children=True, parent_changed=False):
        self._root._update(children, parent_changed)
    
    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, new_active):
        if new_active and not self._active:
            self._activate()
        elif not new_active and self._active:
            self._deactivate()
        
        self._active = new_active
            
    def _activate(self):
        if self._active_camera is None:
            self._active_camera = self._root.get_child_with_name("camera", recursive=True)
    
    def _deactivate(self):
        pass
    
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
    def add_camera(self, new_camera):
        # If the camera isn't already on the list of cameras
        if not new_camera in self._cameras:
            self._cameras.append(new_camera)
            # If the camera is the only camera listed, it becomes the
            # active camera by default
            if len(self._cameras) == 1:
                self._active_camera = self._cameras[0]
            
    # Remove the camera param from the list of known cameras in the scene.
    def remove_camera(self, rm_camera):
        if rm_camera in self._cameras:
            self._cameras.remove(rm_camera)
            
            # If there is only a single camera in the scene, it becomes the
            # active camera by default
            self._active_camera = self._cameras[0]
            
    # Set the camera parameter as the scenes active camera
    def set_active_camera(self, active_camera):
        # If the camera is amongst the cameras that the SceneManager is aware of
        if active_camera in self._cameras:
            # Set all other cameras to be inactive
            for camera in self._cameras:
                camera.active = (camera==active_camera)
            # Set the SceneManagers active camera to be the parameter
            self._active_camera = active_camera       
            
    # Add the light parameter to the list of known lights in the scene
    def add_light(self, new_light):
        # If the light isn't already on the list of lights
        if not new_light in self._lights:
            self._lights.append(new_light)
            
    # Remove the light param from the list of known lights in the scene.
    def remove_light(self, rm_light):
        if rm_light in self._lights:
            self._lights.remove(rm_light)

# Events used by the SceneManager
class SceneBaseEvents:
    events = ['CameraAdded',
              'CameraRemoved',
              'SetActiveCamera',
              'LightAdded',
              'LightRemoved'
             ]
           
class SceneBaseListener(ListenerBase):

    def __init__(self, scene):
        ListenerBase.__init__(self, SceneBaseEvents.events)
        self._scene = scene
        
    def _processEvent(self, new_event):
        # Check if the event is for this scene
        if hasattr(new_event.data, "scene"):
            # If the event is for this scene
            if new_event.data.scene == self._scene:
                # Process the event
                if new_event.name == 'CameraAdded':
                    self._scene.add_camera(new_event.data )
                elif new_event.name == 'CameraRemoved':
                    self._scene.remove_camera(new_event.data)
                elif new_event.name == 'SetActiveCamera':
                    self._scene.set_active_camera(new_event.data)
                if new_event.name == 'LightAdded':
                    self._scene.add_light(new_event.data )
                elif new_event.name == 'LightRemoved':
                    self._scene.remove_light(new_event.data)
    
    
        
        