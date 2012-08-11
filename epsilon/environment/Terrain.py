
class Terrain:
    def __init__(self):
        self._generatedTerrain = None
        self._heightmapFilename = ""
#        self._terrainManager = RenderCore().sceneManager
    
    def generateHeightmap(self):
        self._heightmapFilename = ""
    
    def loadHeightmap(self):
        pass
        # Create the terrain
#        self._terrainManager.setWorldGeometry ("terrain/generatedTerrain.cfg")
            
#    def generateTerrain(self):
#        #Generate Random Lookup Table
#        pass