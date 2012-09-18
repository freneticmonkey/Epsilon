# Used Singleton implementation from - http://wiki.forum.nokia.com/index.php/How_to_make_a_singleton_in_Python
#from time import strftime
from datetime import datetime

#import os
from epsilon.core.basesingleton import BaseSingleton

_log = None

def GetLogger():
    global _log
    if not _log:
        _log = Logger()
    return _log

def Log(text):
    GetLogger().Log(text)
    
def Configure(method, dest, out_console):
    GetLogger()._configure(method, dest, out_console)
    
def SetLogFile(file_name):
    GetLogger().filename = file_name
    
def Shutdown():
    GetLogger._shutdown()
    
# This is a helper class to simplify formatting log output for specific classes
#
class ClassLogger(object):
    
    def __init__(self):
        self._classname = "ClassLogger"
        
    def Log(self, message):
        Log(self._classname + " : " + message)

class LogListener(object):
    def __init__(self, name='unnamed log listener'):
        self._register()
        self._on_log_func = None

    def __del__(self):
        self._deregister()

    def _register(self):
        Logger.add_listener(self)

    def _deregister(self):
        Logger.remove_listener(self)

    def set_log_func(self, log_func):
        self._on_log_func = log_func

    def on_log(self, log_text):
        if not self._on_log_func is None:
            self._on_log_func(log_text)

## Logger Core
#  A Singleton class
class Logger( BaseSingleton ):
    
    # Class methods
    @classmethod
    def Configure(cls, method, dest, out_console):
        cls.get_instance()._configure(method, dest, out_console)
        
    @classmethod
    def Log(cls, text):
        cls.get_instance()._log(text)

    @classmethod
    def add_listener(cls, new_listener):
        cls.get_instance()._add_listener(new_listener)

    @classmethod
    def remove_listener(cls, del_listener):
        cls.get_instance()._remove_listener(del_listener)
    
    def __init__(self, output_console=False):
        self._configured = False
        self._type = ''
        self._filename = ""
        self._file = None
        self._console_output = False
        self._listeners = []
        
    ## When deleting the LoggingCore make sure that the log file is closed.    
    def __del__(self):
        self._shutdown()
            
    def _shutdown(self):
    	self.Log("Logger Shutdown")
        if self._type == 'file' and self._file:
            self._file.flush()
            self._file.close()

    @property
    def filename(self):
        return self._filename
            
    
    ## Create a file with the provided filename
    # @param fileName: The name of the file to be written to
    @filename.setter
    def filename(self, fileName):
        if len(fileName) > 0: 
            self._filename = fileName
        else:
            self._filename = 'log.txt'
            
        try: 
            self._file = open(self._filename, 'w')
            self._fileOpen = True
        except IOError:
            print 'Logger Error: File IO Error opening: ' + self._filename
    
    ## Configure the destination of the Log output
    # @param self The object pointer
    # @param ouputMethod The method of log output
    # @param outputDestination The destination of the file output - Filename, ip add etc.
    # Not all methods of output implemented yet
    def _configure(self, outputMethod, outputDestination, output_console):
        self._type = outputMethod
        self._fileOpen = False
        self._console_output = output_console
        
        if outputMethod == 'file':
            self.filename = outputDestination
        elif outputMethod == 'network':
            print 'Logger: Networking NYI' 
        
        self._configured = True

    # Adds a listener object which receives the output of the log
    def _add_listener(self, new_listener):
        self._listeners.append(new_listener)

    # Removes a log listener
    def _remove_listener(self, del_listener):
        if del_listener in self._listeners:
            self._listeners.remove(del_listener)
    
    ## Writes the Log output with a timestamp
    # @param text: The text string to be written out
    def _log(self, text):
        
        can_write = False
        
        #currentTime = strftime('%H:%M:%S:')
        currentTime = datetime.now().strftime("%H:%M:%S.%f")
        if self._configured:
            if self._fileOpen:
                can_write = True
        else:
            print currentTime + ' Logger output not configured. Using \'Log.txt\' default'
            self._configure('file', 'Log.txt',True)
            
            if self._configured:
                if self._fileOpen:
                    can_write = True
            else:
                print currentTime + ' Logger output not able to be written to file.'
                
        if can_write:
            output_text = currentTime + ' ' + text
            self._file.write( output_text + '\n')
            self._file.flush()
            
            if self._console_output:
                print output_text

            for listener in self._listeners:
                listener.on_log(output_text)
           
 
#    ## The constructor
#    #  @param self The object pointer.
#    def __init__( self ):
#        # Check whether we already have an instance
#        if LoggerCore._instance is None:
#            # Create and remember instance
#            LoggerCore._instance = LoggerCore.Singleton()
# 
#        # Store instance reference as the only member in the handle
#        self.__dict__['_EventHandler_instance'] = LoggerCore._instance        
        
    
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