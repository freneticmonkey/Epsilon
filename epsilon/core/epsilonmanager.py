from epsilon.core.settings import Settings # This must be included before any other epsilon component
from epsilon.core.configurationmanager import ConfigurationManager

from epsilon.logging.logger import Logger

from epsilon.events.eventmanager import EventManager
from epsilon.events.eventbase import EventBase
from epsilon.render.rendermanager import RenderManager
from epsilon.scene.scenemanager import SceneManager  
from epsilon.scripting.scriptmanager import ScriptManager
from epsilon.ui.uimanager import UIManager
from epsilon.ui.ui import MainUI
from epsilon.render.texturemanager import TextureManager
from epsilon.render.shadermanager import ShaderManager
from epsilon.render.gizmos.gizmomanager import GizmoManager

from epsilon.frameworks.frameworkmanager import FrameworkManager

# Sceneloading
from epsilon.resource.resourcemanager import ResourceManager
from epsilon.resource.imageresourcehandler import ImageResourceHandler
from epsilon.resource.sceneresourcehandler import SceneResourceHandler
from epsilon.resource.wavefrontresourcehandler import WavefrontResourceHandler

from epsilon.core.coreevents import CoreListener

# Terrain testing
from epsilon.environment.planet.planetsphere import PlanetSphere

from epsilon.render.gizmos.gizmos import WireCube
from epsilon.geometry.euclid import Vector3

from epsilon.core.time import Time
from epsilon.core.settings import *

from epsilon.render.meshfactory import MeshFactory, MeshTypes
from epsilon.scene.node import Node

## Central Class to the Epsilon System

class FrameStarted(EventBase):
    def __init__(self):
        EventBase.__init__(self, "frame_started", True)
        
class FrameEnded(EventBase):
    def __init__(self):
        EventBase.__init__(self, "frame_ended", True)


class EpsilonManager(object):
    
    def __init__(self):
        # Load Configuration settings
        ConfigurationManager.load_configuration()

        #Start Logger
        method = Settings.get('LoggerSettings','method')
        filename = Settings.get('LoggerSettings','filename')
        to_console = Settings.get('LoggerSettings','log_to_console')
        Logger.Configure(method, filename, to_console)
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

        self._render_manager.init( Settings.get('DisplaySettings','resolution')[0],
                                   Settings.get('DisplaySettings','resolution')[1],
                                   Settings.get('DisplaySettings','window_title')
                                 )
        
        # Setup the framework callbacks
        self._framework = FrameworkManager.framework()
        self._framework.setup = self.setup
        self._framework.run_loop = self.update
        self._framework.on_draw = self._render_manager.draw
        self._framework.on_shutdown = self.shutdown
                
        # Setup Frame Start/End Events
        self._frame_start = FrameStarted()
        self._frame_end = FrameEnded()
        
        #Get the Texture Manager
        self._texture_manager = TextureManager.get_instance()
        
        # Start the ShaderManager
        self._shader_manager = ShaderManager.get_instance()
        
        # Start Scripting System
        self._script_manager = ScriptManager.get_instance()
        
        # Start the UI Manager and setup the MainUI
        self._ui_manager = UIManager.get_instance()
        self._main_ui = MainUI()
        
        # Start the GizmoManager system
        self._gizmo_manager = GizmoManager.get_instance()
        
        # Configure the ResourceManager
        self._resource_manager = ResourceManager.get_instance()
        # enable Image Loading
        self._resource_manager.add_handler(ImageResourceHandler())
        # enable Scene Loading
        self._resource_manager.add_handler(SceneResourceHandler())
        # enable Wavefront Obj Loading
        self._resource_manager.add_handler(WavefrontResourceHandler())
        
    def set_scene(self):        
        # Testing loading using the ResourceManager
        self._resource_manager.process_resource("scene.xml")
        
        #self._planet = PlanetSphere()
        #self._scene.current_scene.root.transform.add_child(self._planet.transform)
        
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
                
        # Update SceneManager
        self._scene.update()
        
        #self._planet.update_sphere()

        # Cull Scene for rendering
        self._render_manager.cull()
        
        self._frame_end.send()
        
    def shutdown(self):

        self._ui_manager.shutdown()
        Logger.shutdown()
        ConfigurationManager.save_configuration()
        print "After EpsilonManager shutdown"


    
    
    
    