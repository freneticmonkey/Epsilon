
import Terrain

class EnviroCore:
    _instance = None
        
    ## Class used with this Python singleton design pattern
    #  @todo Add all variables, and methods needed for the Singleton class below
    class Singleton(OgreApplication):
        def __init__(self):
            self._terrain = Terrain()            
            
            # The logger
            self._logger = LoggerCore()
            self._logger._print('Initialised EnviroCore')
            
    ## The constructor
    #  @param self The object pointer.
    def __init__( self ):
        # Check whether we already have an instance
        if RenderCore._instance is None:
            # Create and remember instance
            RenderCore._instance = RenderCore.Singleton()
 
        # Store instance reference as the only member in the handle
        self.__dict__['_RenderHandler_instance'] = RenderCore._instance
    
    ## Delegate access to implementation.
    #  @param self The object pointer.
    #  @param attr Attribute wanted.
    #  @return Attribute
    def __getattr__(self, aAttr):
        return getattr(self._instance, aAttr)
 
 
    ## Delegate access to implementation.
    #  @param self The object pointer.
    #  @param attr Attribute wanted.
    #  @param value Vaule to be set.
    #  @return Result of operation.
    def __setattr__(self, aAttr, aValue):
        return setattr(self._instance, aAttr, aValue)