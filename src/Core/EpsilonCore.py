from Logging import Logger
from Events.EventCore import *
from Input import InputProcessor
from Render import RenderCore
from Scene import SceneManager  
from Scripting.ScriptManager import ScriptManager
from Render import TextureManager
from Render.Material import GLMaterial
from Render.ShaderManager import *
from Render.Shader import PhongShader

from CoreEvents import CoreListener

from Render.Camera import CameraGL
from Render.Light import GLLight
from Render.Material import GLMaterial
from Render.Colour import Colour, Preset
from Scene.Node import Node, Plane
from Render.MeshFactory import MeshFactory, MeshTypes
from Geometry.euclid import Vector3, Quaternion

from Core import Time
from time import time

from Scripting.TestScripts import ( RotateScript, 
                                  MoveController,  
                                  CameraMoveController,  
                                  DisplayCoordinate, 
                                  SettingsController )
## Central Class to the Epsilon System

class EpsilonCore:
    #_renderCore = None
    #_eventsCore = None
    #_aiCore = None
    #_enviroCore = None
    
    
    def __init__(self):
        #Start Logger
        
        Logger.Configure('file', 'EpsilonLog.txt', True)
        Logger.Log('Initialising Core Systems')
        
        #Start Event System
        self._eventCore = GetEventCore()
        
        #Register Core Event Listener for detecting quit
        self._keepAlive = True
        self._coreListener = CoreListener(False)
        GetEventCore().AddListener(self._coreListener)
        
        # Create a Scene
        self._scene = GetSceneManager()
        self._scene.Init()
        
        #Start Render System
        self._renderCore = RenderCore.GetRenderCore()
        self._renderCore.Init(800,600,"Epsilon")
        
        #Get the Texture Manager
        self._texture_manager = TextureManager.GetTextureManager()
        
        # Start Scripting System
        self._scriptCore = ScriptManager.GetInstance()
        
        # Initialise Input
        self._inputProcessor = InputProcessor()
        
        #Start EnvironmentSystem
        #self._enviroCore = EnvironmentCore()
        
        #Start AI System
        #self._aiCore = AICore()
        
    def __del__(self):
        self.Shutdown()
        
    def SetScene(self):
        
        root = self._scene.root
        
        # Load a Texture
        ssfilename = "/Users/scottporter/Development/Projects/python_tests/my_projects/src/Epsilon/src/UnitTests/checkerboard64.png"
        sstex = self._texture_manager.CreateTexture(ssfilename)
        
        # Load Shaders
#        vs = "lighting.vert"
#        fs = "lighting.frag"
#        GetShaderManager().AddShaderFromFiles("lighting", vs, fs)
        
        GetShaderManager().AddShaderObject("comp_lighting", PhongShader())
        
        
        # Add a Camera
        camera = CameraGL()
        root.AddChild(camera)
        
        camera.local_position = Vector3(2,1,-10)
        camera.AddScript(CameraMoveController(speed=20))
#        cameraBase.AddChild(camera)
        
#        octom = Node()
#        root.AddChild(octom)
#        octom.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
#        octom.local_scale = Vector3(0.1, 0.1, 0.1)
        
        octo = Node(name="parent")
        octo.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
        octo.local_scale = Vector3(1,1,1)
        octo.local_position = Vector3(0,3,0)
        octo.material = GLMaterial()
        octo.material.texture = sstex
        octo.material.shader = "comp_lighting"
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
        if True:
            red_light = GLLight()
            red_light.diffuse = Preset.red
            red_light.specular = Preset.red
            red_light.local_position = Vector3(1.0,1.0,1.0)
            root.AddChild(red_light)
        
        # Add a blue light
        if True:
            blue_light = GLLight()
            blue_light.diffuse = Preset.blue
            blue_light.specular = Preset.blue
            blue_light.local_position = Vector3(-1.0,1.0,2.0)
            root.AddChild(blue_light)
        
        # Add a light
        light = GLLight(name="light")#Node(name="light")
        light.attenuation = 0.25
#        light.local_position = Vector3(0, 0.5, 0)
#        light.AddScript(MoveController())

        marker = Node(name="marker")
        marker.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
        marker.local_scale = Vector3(0.2, 0.2, 0.2)
        marker.material = GLMaterial()
        marker.material.shader = "comp_lighting"
        light.AddChild(marker)

#        root.AddChild(light)
        light.local_position = Vector3(0, 0.0, 10)
        camera.AddChild(light)

        hidetail = Node()
        hidetail.mesh = MeshFactory.GetMesh(MeshTypes.SPHERE)
        hidetail.local_position = Vector3(2.0,1,0)
        hidetail.material = GLMaterial()
        hidetail.material.shader = "comp_lighting"
        hidetail.material.texture = sstex
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
        
        # Ground plane
        ground = Node()
        ground.mesh = MeshFactory.GetMesh(MeshTypes.PLANE_HI)
        ground.local_scale = Vector3(10,1,10)
        ground.material = GLMaterial()
        ground.material.shader = "comp_lighting"
        ground.material.texture = sstex
        root.AddChild(ground)
        
#        # Scripts that run in the scene
        scene_scripts = Node()
        root.AddChild(scene_scripts)
        scene_scripts.AddScript(SettingsController())
        
        self._renderCore.SetCamera(camera)
        
    def Run(self):
        
        # Load Textures
        self._texture_manager.LoadTextures()
        
        # Initialise Scripts
        self._scriptCore.InitialiseScripts()
        
        # Start Scripts
        self._scriptCore.StartScripts()
        
        # Get the current time
        _frame_start = time()
        
        # Until a Quit Event is detected process engine systems
        while self._keepAlive == True:
            
            GetShaderManager().OnFrameStart()
            
            Time.UpdateDelta()
            
#            self._physicsCore.Update()
            
#            self._enviroCore._processEnvironment()
            
            #self._aiCore._processAI()
            
            # Update Scripts
            self._scriptCore.Update()
            
            # Render the Scene
            self._renderCore.Draw()
            
            # Process Keyboard input
            self._inputProcessor._process_input()
            
            # Last so that any change to _keepAlive through the event system is detected
            self._eventCore._processEvents()
            
            # Update SceneManager
            self._scene.Update()
            
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

    
    
    
    