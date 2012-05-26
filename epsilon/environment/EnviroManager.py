import Terrain
from Logging import LoggerCore
from Events import EventsCore

# Enviro Core
#  A Singleton class
class EnviroCore( object ):
    _instance = None
    #_listeners = []
    
    ## Class used with this Python singleton design pattern
    #  @todo Add all variables, and methods needed for the Singleton class below
    class Singleton:
        def __init__(self):
            #Initialise Terrain Class
            self._terrain = Terrain()
            
            #Generate Terrain Heightmap 
            
            # The logger
            self._logger = LoggerCore()
            self._logger._print('Initialised EnviroCore')            
            
    ## The constructor
    #  @param self The object pointer.
    def __init__( self ):
        # Check whether we already have an instance
        if EnviroCore._instance is None:
            # Create and remember instance
            EventsCore._instance = EnviroCore.Singleton()
 
        # Store instance reference as the only member in the handle
        self.__dict__['_EventHandler_instance'] = EnviroCore._instance
    
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