'''
Created on Mar 4, 2012

@author: scottporter
'''
#from Resource.Resource import ResourceType
#from Resource.ResourceManager import ResourceManager

#from Logging import Logger
#from os.path import join, realpath, dirname, isabs, splitext

# Base class for all Resource Handlers
class ResourceHandlerBase(object):
    def __init__(self):
        
        self._resource_type = None
        self._filetypes = []
    
    @property
    def resource_type(self):
        return self._resource_type
    
    @property
    def filetypes(self):
        return self._filetypes
    
    def process_resource(self, filename, name):
        print "Errrpp you shouldn't be seeing this."
    
    def remove_resource(self, filename=""):
        pass
#        
#        # Check file extension to see if this type is handled by this ResourceHandler
#        parts = splitext(filename)
#        
#        if parts[1].lower() in self._filetypes:
#            
#            # Get the current path set in the ResourceManager
#            current_resource_path = ResourceManager.get_instance().current_path
#            
#            # get the path of the new Resource
#            abs_filename = filename
#            # if the path is relative
#            if not isabs(filename):
#                # Make it absolute
#                abs_filename = realpath(join(current_resource_path, filename))
#            
#            # Set the new path as the path in the ResourceManager
#            ResourceManager.get_instance().current_path = dirname(abs_filename)
#            
#            # Process the Resource
#            new_resource = self._proc_resource(abs_filename)
#            if not new_resource is None:
#                ResourceManager.get_instance().add_resource(new_resource)
#            
#            # Rollback the current relative path set in the ResourceManager
#            ResourceManager.get_instance().current_path = current_resource_path
#            
#        else:
#            Logger.Log("%s: The specified filetype cannot be handled: %s " % (self.__class__.__name__, filename))
    
#    def _proc_resource(self, filename):
#        pass
        
        
        
    
    
        
