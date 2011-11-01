# Used Singleton implementation from - http://wiki.forum.nokia.com/index.php/How_to_make_a_singleton_in_Python
from time import strftime
#import os

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
        Log(self._className + " : " + message)

## Logger Core
#  A Singleton class
class Logger( object ):
        
    def __init__(self, output_console=False):
        self._configured = False
        self._type = ''
        self._filename = ""
        self._file = None
        self._console_output = False
        
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
    
    
    ## Writes the Log output with a timestamp
    # @param text: The text string to be written out
    def Log(self, text):
        
        can_write = False
        
        currentTime = strftime('%H:%M:%S:')
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