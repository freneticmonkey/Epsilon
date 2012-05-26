from epsilon.logging import Logger

from epsilon.events.eventmanager import EventManager
from epsilon.events.eventbase import EventBase
#from epsilon.input import Input
from epsilon.render.rendermanager import RenderManager
from epsilon.scene.scenemanager import SceneManager  
from epsilon.scripting.scriptmanager import ScriptManager
from epsilon.ui.uimanager import UIManager
from epsilon.render.texturemanager import TextureManager
from epsilon.render.shadermanager import ShaderManager
from epsilon.render.shaders.phong import PhongShader
from epsilon.render.shaders.phongsimple import PhongSimple

from epsilon.frameworks.frameworkmanager import FrameworkManager

# Sceneloading
from epsilon.resource.resourcemanager import ResourceManager
from epsilon.resource.imageresourcehandler import ImageResourceHandler
from epsilon.resource.sceneresourcehandler import SceneResourceHandler
from epsilon.resource.wavefrontresourcehandler import WavefrontResourceHandler

from epsilon.core.coreevents import CoreListener

#from Render.Camera import CameraGL
#from Render.Light import GLLight
#from Render.Material import GLMaterial
#from Render.Colour import Colour, Preset
#from Scene.Node import Node, Plane
#from Render.MeshFactory import MeshFactory, MeshTypes
#from Geometry.euclid import Vector3, Quaternion

from epsilon.core.time import Time
from epsilon.core.settings import *

#from Scripting.TestScripts import ( RotateScript, 
#                                  MoveController,  
#                                  CameraMoveController,  
#                                  DisplayCoordinate, 
#                                  SettingsController )

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
        
        #Register Core Event Listener for detecting quit
        self._core_listener = CoreListener(False)
        
        # Initialise Time
        self._time = Time.get_instance()
        
        # Create a Scene
        self._scene = SceneManager.get_instance()
        self._scene.init()
        
        #Start Render System
        self._render_manager = RenderManager.get_instance()
        self._render_manager.init(DisplaySettings.resolution[0],
                                  DisplaySettings.resolution[1],
                                  DisplaySettings.window_title)
        
        # Setup the framework callbacks
        self._framework = FrameworkManager.get_instance().framework
        self._framework.setup = self.setup
        self._framework.run_loop = self.update
        self._framework.on_draw = self._render_manager.draw
                
        # Initialise Input
        #self._input = Input.get_instance()
        
        # Setup Frame Start/End Events
        self._frame_start = FrameStarted()
        self._frame_end = FrameEnded()
        
        #Get the Texture Manager
        self._texture_manager = TextureManager.get_instance()
        
        # Start the ShaderManager
        self._shader_manager = ShaderManager.get_instance()
        
        # Start Scripting System
        self._script_manager = ScriptManager.get_instance()
        
        # Start the UI Manager
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
        self._shader_manager.add_shader_object("phong_simple", PhongSimple())
        
        # Testing loading using the ResourceManager
        self._resource_manager.process_resource("scene.xml")
        #self._resource_manager.process_resource("empty_scene.xml")
        
    def run(self):
        self._framework.start()
    
    def setup(self):
        # Load Textures
        self._texture_manager.load_textures()
        
        # Initialise Scripts
        self._script_manager.initialise_scripts()
        
        # Start Scripts
        self._script_manager.start_scripts()
        
        Logger.Log("Finished Setup")
            
    def update(self, dt=0):
    
        self._time.update_delta()
        
        # Send Frame Started Event
        self._frame_start.send()
        
        # Process Events
        self._event_manager.process_events()
        
        # Render the Scene
        #self._render_manager.draw()
        
        # Update SceneManager
        self._scene.update()
        
        self._frame_end.send()
        
    def shutdown(self):
        del self._render_manager


    
    
    
    