#from OgreApplication import OgreApplication
#from Events.EventsCore import *
#from Logging.LoggerCore import *
#from RenderOperations import *
#from RenderListeners import *

from Renderer import GLRenderer

from Core.BaseManager import BaseSingleton

_instance = None

class RenderManager(BaseSingleton):
    
    def __init__(self):
        # create a renderer
        self._renderer = GLRenderer()
        
    def __del__(self):
        del self._renderer
        
    def Init(self, width, height, title):
        self._renderer.InitialiseDisplay(width, height, title)
        
    def SetCamera(self, camera):
        self._renderer.camera = camera
        
    def Draw(self):
        self._renderer.Draw()
        

#    _instance = None
#        
#    ## Class used with this Python singleton design pattern
#    #  @todo Add all variables, and methods needed for the Singleton class below
#    class Singleton(OgreApplication):
#        def __init__(self):
#            OgreApplication.__init__(self)
#            
#            #Create and Init OGRE
#            # -- Done automatically currently in OgreApplication
#            
#            #Create RenderOperations Object for Listener Access to renderer
#            self._renderOps = RenderOperations(self.sceneManager)
#            
#            #Create and Init Event Listener
#            self._renderListener = RenderListener(self._renderOps)
#            EventsCore()._addListener(self._renderListener)
#            
#            #Configure Ogre
#            if not self._setUp():
#                return
#            if self._isPsycoEnabled():
#                self._activatePsyco()
#        
#            self.root.getRenderSystem()._initRenderTargets()
#                        
#            #Notify Manager that Renderer is online.
#        
#            # The logger
#            self._logger = LoggerCore()
#            self._logger._print('Initialised RenderCore')
#            
#        def _chooseSceneManager(self):
#            # Select the terrain scene manager.
#            self.sceneManager = self.root.createSceneManager (ogre.ST_EXTERIOR_CLOSE, 'TerrainSM')
#            
#        def _createScene(self):            
#            sceneManager = self.sceneManager
#            camera = self.camera
#            camera.setPosition(0,0,528)
#            #camera.setPosition(707,0,528)
#            
#            sceneManager.AmbientLight = ogre.ColourValue(0.5, 0.5, 0.5)
#            sceneManager.setSkyBox(True, 'Examples/SpaceSkyBox')
##    
##            entity = sceneManager.createEntity('head', 'ogrehead.mesh')
##            sceneManager.getRootSceneNode().attachObject(entity)
#            
#            # Create a scene with terrain, sky and fog.
# 
#            # Setup the fog.
#            #fadeColour = (0.9, 0.9, 0.9)
#            #self.renderWindow.getViewport (0).backgroundColour = fadeColour
#            #self.sceneManager.setFog (ogre.FOG_LINEAR, fadeColour, 0.0, 50, 500)
#            
#            # Create a sphere and use Blue Marble texture.
#            globe = sceneManager.createEntity('globe', 'sphere.mesh')
#            sceneManager.getRootSceneNode().attachObject(globe)
#            globe.setMaterialName('Examples/ShowNormals')
#            
##            light = sceneManager.createLight('MainLight')
# #           light.setType(ogre.Light.LT_POINT)
#  #          light.setPosition(0, 0, 528)
#             
#            # Create the terrain
#            #self.sceneManager.setWorldGeometry ("terrain/terrain.cfg")
#             
#            # Setup a sky plane.
#            #plane = ogre.Plane ((0, -1, 0), -10)
#            #self.sceneManager.setSkyPlane (True, plane, "Examples/CloudySky", 100, 45, True, 0.5, 150, 150)
#            
#            
#        ## Add a Listener Object to the list of listeners
#        # @param newListener: The new Listener to add
#        def _renderFrame(self):
#            self._renderListener._processEvents()
#            return self.goOneFrame()
# 
#    ## The constructor
#    #  @param self The object pointer.
#    def __init__( self ):
#        # Check whether we already have an instance
#        if RenderCore._instance is None:
#            # Create and remember instance
#            RenderCore._instance = RenderCore.Singleton()
# 
#        # Store instance reference as the only member in the handle
#        self.__dict__['_RenderHandler_instance'] = RenderCore._instance
#    
#    ## Delegate access to implementation.
#    #  @param self The object pointer.
#    #  @param attr Attribute wanted.
#    #  @return Attribute
#    def __getattr__(self, aAttr):
#        return getattr(self._instance, aAttr)
# 
# 
#    ## Delegate access to implementation.
#    #  @param self The object pointer.
#    #  @param attr Attribute wanted.
#    #  @param value Vaule to be set.
#    #  @return Result of operation.
#    def __setattr__(self, aAttr, aValue):
#        return setattr(self._instance, aAttr, aValue)
    
        
        
    
    
        