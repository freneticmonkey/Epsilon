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

from Render.Camera import CameraGL
from Render.Light import GLLight
from Render.Material import GLMaterial
from Render.Colour import Colour, Preset
from Scene.Node import Node, Plane
from Render.MeshFactory import MeshFactory, MeshTypes
from Geometry.euclid import Vector3, Quaternion

from Core.Time import Time
from time import time

from Scripting.TestScripts import ( RotateScript, 
                                  MoveController,  
                                  CameraMoveController,  
                                  DisplayCoordinate, 
                                  SettingsController )

from Core.Settings import *

## Central Class to the Epsilon System

class FrameStarted(EventBase):
    def __init__(self):
        EventBase.__init__(self, "frame_started", True)
        
class FrameEnded(EventBase):
    def __init__(self):
        EventBase.__init__(self, "frame_ended", True)


class EpsilonManager(object):
    #_renderCore = None
    #_eventsCore = None
    #_aiCore = None
    #_enviroCore = None
    
    
    def __init__(self):
        #Start Logger
        Logger.Configure(LoggerSettings.method, LoggerSettings.filename, LoggerSettings.log_to_console)
        Logger.Log('Initialising Core Systems')
        
        
        # The order of initialisation in this function is extremely important
        # as it determines the order in which classes will receive events.
        # For instance it is important that input is processed
        
        # Start Event System so it can receive new listeners when the
        # classes below are initialised 
        self._eventCore = EventManager.get_instance()
        
        # Initialise Time
        self._time = Time.get_instance()
        
        # Create a Scene
        self._scene = SceneManager.get_instance()
        self._scene.init()
        
        #Start Render System
        self._renderCore = RenderManager.get_instance()
        self._renderCore.Init(DisplaySettings.resolution[0],DisplaySettings.resolution[1],DisplaySettings.window_title)
                
        # Initialise Input
        self._input = Input.get_instance()
        
        # Setup Frame Start/End Events
        self._frame_start = FrameStarted()
        self._frame_end = FrameEnded()
        
        #Register Core Event Listener for detecting quit
        self._keepAlive = True
        self._coreListener = CoreListener(False)
        
        #Get the Texture Manager
        self._texture_manager = TextureManager.get_instance()
        
        # Start the ShaderManager
        self._shader_manager = ShaderManager.get_instance()
        
        # Start Scripting System
        self._scriptCore = ScriptManager.get_instance()
        
        self._ui_manager = UIManager.get_instance()
        
        # Configure the ResourceManager
        self._resource_manager = ResourceManager.get_instance()
        # enable Image Loading
        self._resource_manager.add_handler(ImageResourceHandler())
        # enable Scene Loading
        self._resource_manager.add_handler(SceneResourceHandler())
        # enable Wavefront Obj Loading
        self._resource_manager.add_handler(WavefrontResourceHandler())
        
        #Start EnvironmentSystem
        #self._enviroCore = EnvironmentCore()
        
        #Start AI System
        #self._aiCore = AICore()
        
    def __del__(self):
        self.Shutdown()
        
    def SetScene(self):
#        
#        root = self._scene.root
#                
        # Scripts that run in the scene - This is done first to
        # ensure that these scripts are given priority over the scripts
        # attached to nodes

#        scene_scripts = Node()
#        root.AddChild(scene_scripts)
#        scene_scripts.AddScript(SettingsController())
        
        
        # Load Shaders
#        vs = "lighting.vert"
#        fs = "lighting.frag"
#        GetShaderManager().AddShaderFromFiles("lighting", vs, fs)
        
        # Default Shaders
#        self._shader_manager.AddShaderObject("phong", PhongShader())
        self._shader_manager.AddShaderObject("phong_simple", PhongSimple())
        
        # Testing loading using the ResourceManager
        
        self._resource_manager.process_resource("scene.xml")
        
#        ssfilename = "/Users/scottporter/Development/Projects/Python/Epsilon/src/UnitTests/checkerboard64.png"
#        self._resource_manager.process_resource(ssfilename)
        
        return
        
        # Load a Texture
        ssfilename = "/Users/scottporter/Development/Projects/Python/Epsilon/src/UnitTests/checkerboard64.png"
        sstex = self._texture_manager.create_texture(ssfilename)
        
        
        # Add a Camera
        camera = CameraGL()
        root.AddChild(camera)
        
        camera.position = Vector3(2,1,-10)
        camera.AddScript(CameraMoveController(speed=20))
#        cameraBase.AddChild(camera)

        self._renderCore.SetCamera(camera)
                
#        octom = Node()
#        root.AddChild(octom)
#        octom.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
#        octom.local_scale = Vector3(0.1, 0.1, 0.1)
        
        if False:
            octo = Node(name="parent")
            octo.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
            octo.scale = Vector3(1,1,1)
            octo.position = Vector3(0,3,0)
            root.AddChild(octo)
        
        # Add an object
#        octo2 = Node(name="child")
#        octo2.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
#        octo2.local_scale = Vector3(1, 1, 1)
#        octo2.local_position = Vector3(-2,0,0)
#        octo2.AddScript(RotateScript(rate=360))
#        octo2.material = GLMaterial()
#        octo2.material.shader = "comp_lighting"
#        octo.AddChild(octo2)
        
#        octo3 = Node()
#        octo3.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
#        octo3.local_scale = Vector3(0.2, 0.2, 0.2)
#        octo3.local_position = Vector3(2, 0.5, 0)
#        octo2.AddChild(octo3)
        
        # Add a red light
        if False:
            red_light = GLLight()
            red_light.diffuse = Preset.red
            red_light.specular = Preset.red
            red_light.position = Vector3(1.0,1.0,0.0)
            root.AddChild(red_light)
        
        # Add a blue light
        if True:
            blue_light = GLLight()
            blue_light.ambient = Preset.white
            blue_light.diffuse = Preset.white
            blue_light.specular = Preset.red
            blue_light.position = Vector3(-1.0,1.0,1.0)
            #blue_light.AddScript(CameraMoveController(speed=20))
            root.AddChild(blue_light)
            
        if False:    
            hidetail2 = Node()
            hidetail2.mesh = MeshFactory.GetMesh(MeshTypes.SPHERE)
            hidetail2.position = Vector3(-1.0,1.0,0.0)
            hidetail2.local_scale = Vector3(0.2,0.2,0.2)
            hidetail2.material = GLMaterial()
            root.AddChild(hidetail2)
        
        # Add a light
#        light = GLLight(name="light")#Node(name="light")
#        light.attenuation = 0.01
##        light.local_position = Vector3(0, 0.5, 0)
##        light.AddScript(MoveController())
#
#        marker = Node(name="marker")
#        marker.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
#        marker.local_scale = Vector3(0.2, 0.2, 0.2)
#        marker.material = GLMaterial()
#        marker.material.shader = "comp_lighting"
#        light.AddChild(marker)
#
##        root.AddChild(light)
#        light.local_position = Vector3(0, 0.0, 10)
#        camera.AddChild(light)
        if True:
            hidetail = Node()
            hidetail.mesh = MeshFactory.GetMesh(MeshTypes.SPHERE)
            hidetail.position = Vector3(2.0,1,0)
            hidetail.material = GLMaterial()
            hidetail.material.diffuse = Preset.green
#            hidetail.material.shininess = 0.1
            hidetail.material.shader = "phong_simple"
            
            root.AddChild(hidetail)
        
#        # Temp testing - A Grid of Spheres
#        for x in range( 10, 20, 2):
#            for z in range ( 10, 20, 2):
#                nhidetail = Node()
#                nhidetail.local_position = Vector3(x,0,z)
#                nhidetail.mesh = MeshFactory.GetMesh(MeshTypes.SPHERE)
#                nhidetail.material = GLMaterial()
#                nhidetail.material.shader = "comp_lighting"
#                root.AddChild(nhidetail)
        draw_ground = True
        if draw_ground:
            # Ground plane
            ground = Node()
            ground.mesh = MeshFactory.GetMesh(MeshTypes.PLANE_HI)
            #ground.local_scale = Vector3(10,1,10)
            ground.local_scale = Vector3(100,1,100)
            ground.material = GLMaterial()
            ground.material.shader = "phong_simple"
#            ground.material.shader = "phong"
            ground.material.shininess = 0.01
    #        ground.AddScript(RotateScript(rate=360,axis=Vector3(1,0,0)))
            root.AddChild(ground)
        
        draw_box = False
        if draw_box:
            # Left Plane
            left = Node()
            left.mesh = MeshFactory.GetMesh(MeshTypes.PLANE_HI)
            left.local_scale = Vector3(10,1,10)
            left.rotation = Quaternion().new_rotate_axis(1.5707, Vector3(0,0,1) )
            left.position = Vector3(5,5,0)
            root.AddChild(left)
            
            right = Node()
            right.mesh = MeshFactory.GetMesh(MeshTypes.PLANE_HI)
            right.local_scale = Vector3(10,1,10)
            right.rotation = Quaternion().new_rotate_axis(-1.5707, Vector3(0,0,1) )
            right.position = Vector3(-5,5,0)
            root.AddChild(right)
            
            rear = Node()
            rear.mesh = MeshFactory.GetMesh(MeshTypes.PLANE_HI)
            rear.local_scale = Vector3(10,1,10)
            rear.rotation = Quaternion().new_rotate_axis(-1.5707, Vector3(1,0,0) )
            rear.position = Vector3(0,5,5)
            root.AddChild(rear)
            
            top = Node()
            top.mesh = MeshFactory.GetMesh(MeshTypes.PLANE_HI)
            top.local_scale = Vector3(10,1,10)
            top.rotation = Quaternion().new_rotate_axis(-3.141562, Vector3(1,0,0) )
            top.position = Vector3(0,10,0)
            root.AddChild(top)
        
    def Run(self):
        
        # Load Textures
        self._texture_manager.load_textures()
        
        # Initialise Scripts
        self._scriptCore.InitialiseScripts()
        
        # Start Scripts
        self._scriptCore.StartScripts()
        
        # Until a Quit Event is detected process engine systems
        while self._keepAlive == True:
            
            self._time.update_delta()
            
            # Send Frame Started Event
            self._frame_start.Send()
            
            # Process Events
            self._eventCore._processEvents()
            
            # Render the Scene
            self._renderCore.Draw()
            
            # Update SceneManager
            self._scene.Update()
            
#            self._frame_end.Send()
            
            self._keepAlive = not self._coreListener.quitting
            
        Logger.Log("Finished")
        
    def Shutdown(self):
        # Cleanup the Cores
        #del self._aiCore
        #del self._enviroCore
        del self._renderCore
        

# if __name__ == '__main__':
# #    try:
#         core = EpsilonCore()
#         core.run()
#    except ogre.OgreException, e:
#        print e

    
    
    
    