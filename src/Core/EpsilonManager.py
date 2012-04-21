from Logging import Logger
from Events.EventManager import EventManager
from Events.EventBase import EventBase
from Input import Input
from Render.RenderManager import RenderManager
from Scene.SceneManager import SceneManager  
from Scripting.ScriptManager import ScriptManager
from UI.UIManager import UIManager
from Render.TextureManager import TextureManager
from Render.ShaderManager import ShaderManager
from Render.Shaders.Phong import PhongShader
from Render.Shaders.PhongSimple import PhongSimple

# Sceneloading
from Resource.ResourceManager import ResourceManager
from Resource.ImageResourceHandler import ImageResourceHandler
from Resource.SceneResourceHandler import SceneResourceHandler
from Resource.WavefrontResourceHandler import WavefrontResourceHandler

from CoreEvents import CoreListener

#from Render.Camera import CameraGL
#from Render.Light import GLLight
#from Render.Material import GLMaterial
#from Render.Colour import Colour, Preset
#from Scene.Node import Node, Plane
#from Render.MeshFactory import MeshFactory, MeshTypes
#from Geometry.euclid import Vector3, Quaternion

from Core.Time import Time
from time import time

#from Scripting.TestScripts import ( RotateScript, 
#                                  MoveController,  
#                                  CameraMoveController,  
#                                  DisplayCoordinate, 
#                                  SettingsController )

from Core.Settings import *

## Central Class to the Epsilon System

class FrameStarted(EventBase):
    def __init__(self):
        EventBase.__init__(self, "frame_started", True)
        
class FrameEnded(EventBase):
    def __init__(self):
        EventBase.__init__(self, "frame_ended", True)


class EpsilonManager(object):
    
    def __init__(self):
        #Start Logger
        Logger.Configure(LoggerSettings.method, LoggerSettings.filename, LoggerSettings.log_to_console)
        Logger.Log('Initialising Core Systems')
        
        # The order of initialisation in this function is extremely important
        # as it determines the order in which classes will receive events.
        # For instance it is important that input is processed
        
        # Start Event System so it can receive new listeners when the
        # classes below are initialised 
        self._event_manager = EventManager.get_instance()
        
        # Initialise Time
        self._time = Time.get_instance()
        
        # Create a Scene
        self._scene = SceneManager.get_instance()
        self._scene.init()
        
        #Start Render System
        self._render_manager = RenderManager.get_instance()
        self._render_manager.init(DisplaySettings.resolution[0],DisplaySettings.resolution[1],DisplaySettings.window_title)
                
        # Initialise Input
        self._input = Input.get_instance()
        
        # Setup Frame Start/End Events
        self._frame_start = FrameStarted()
        self._frame_end = FrameEnded()
        
        #Register Core Event Listener for detecting quit
        self._keep_alive = True
        self._core_listener = CoreListener(False)
        
        #Get the Texture Manager
        self._texture_manager = TextureManager.get_instance()
        
        # Start the ShaderManager
        self._shader_manager = ShaderManager.get_instance()
        
        # Start Scripting System
        self._script_manager = ScriptManager.get_instance()
        
        self._ui_manager = UIManager.get_instance()
        
        # Configure the ResourceManager
        self._resource_manager = ResourceManager.get_instance()
        # enable Image Loading
        self._resource_manager.add_handler(ImageResourceHandler())
        # enable Scene Loading
        self._resource_manager.add_handler(SceneResourceHandler())
        # enable Wavefront Obj Loading
        self._resource_manager.add_handler(WavefrontResourceHandler())
        
    def __del__(self):
        self.shutdown()
        
    def set_scene(self):
        # Default Shaders
        self._shader_manager.AddShaderObject("phong_simple", PhongSimple())
        
        # Testing loading using the ResourceManager
        #self._resource_manager.process_resource("scene.xml")
        self._resource_manager.process_resource("empty_scene.xml")
        
    def run(self):
        
        # Load Textures
        self._texture_manager.load_textures()
        
        # Initialise Scripts
        self._script_manager.initialise_scripts()
        
        # Start Scripts
        self._script_manager.start_scripts()
        
        # Until a Quit Event is detected process engine systems
        while self._keep_alive == True:
            
            self._time.update_delta()
            
            # Send Frame Started Event
            self._frame_start.send()
            
            # Process Events
            self._event_manager.process_events()
            
            # Render the Scene
            self._render_manager.draw()
            
            # Update SceneManager
            self._scene.update()
            
            self._keep_alive = not self._core_listener.quitting
            
        Logger.Log("Finished")
        
    def shutdown(self):
        del self._render_manager


    
    
    
    