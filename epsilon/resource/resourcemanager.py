'''
Created on Nov 19, 2011

@author: scottporter
'''
import os
from os.path import join, realpath, dirname, isabs, splitext, exists

from epsilon.core.basesingleton import BaseSingleton

from epsilon.logging.logger import ClassLogger

class ResourceManagerLog(ClassLogger):
    
    def __init__(self):
        ClassLogger.__init__(self)
        self._classname = "ResourceManager"

# The ResourceManager reads a resource file which contains the 
# directories in which resources can be found.  The ResourceManager
# then parses the directories and builds a dictionary of 
# Resource objects for each file within the directories.  This 
# dictionary can then be used by the ResourceManager to keep track of
# which files are in use. 
# 
# Handling resources in this way would allow for things like 
# zip files to be specified as resource paths the decompression of
# which would also be handled by the ResourceManager.
#
# 

class ResourceManager(BaseSingleton):
    
    def __init__(self):        
        # Set the current path as the current Epsilon execution path
        self._current_path = os.getcwd()
        
        self._log = ResourceManagerLog()
        
        self._handlers = []
        self._resources = {}
        
    def init(self):
        self._load_resources()
        
    @property
    def current_path(self):
        return self._current_path
    
    @current_path.setter
    def current_path(self, new_current_path):
        self._current_path = new_current_path
        
    # Add a handler for loading specific Resources
    def add_handler(self, new_handler):
        
        # Disabling Class check... and instead checking for raw attributes due to circular import issue with ResourceHandler
#        if isinstance(new_handler, ResourceHandler):
        
        if hasattr(new_handler, "filetypes") and  hasattr(new_handler, "process_resource"):
            self._handlers.append(new_handler)
        else:
            self._log.Log("The Resource Handler class: %s is not derived from ResourceHandler." % (new_handler.__class__.__name__))
    
    
    def _load_resources(self):
        # Parse resources file
        pass
    
    # External function that can in turn be called by the ResourceHandlers allowing for recursive loading
    def process_resource(self, filename):
        
        # check if this resource has already been loaded
        new_resource = self.get_resource_by_filename(filename)
        
        # If the resource hasn't already been loaded, load it
        if new_resource is None:
            # Check file extension to see if this type is handled by this ResourceHandler
            parts = splitext(filename)
            # trim the period and ensure lowercase
            extension = parts[1][1:].lower()
            
            the_handler = None
            for handler in self._handlers:
                if extension in handler.filetypes:
                    the_handler = handler
                    break
                
            # If a handler for the filetype is found
            if not the_handler is None:
                # Get the current path set in the ResourceManager
                current_resource_path = self._current_path
                
                # get the path of the new Resource
                abs_filename = filename
                # if the path is relative
                if not isabs(filename):
                    # Make it absolute
                    abs_filename = realpath(join(current_resource_path, filename))
                
                
                if not exists(filename):
                    self._log.Log("Resource could not be loaded: %s" % filename)
                    self._log.Log("Current path: %s" % os.getcwd())
                else:
                    # Set the new path as the path in the ResourceManager
                    self._current_path = dirname(abs_filename)
                    
                    # Process the Resource
                    new_resource = the_handler.process_resource(abs_filename)
                    if not new_resource is None:
                        self._add_resource(new_resource)
                    
                    # Rollback the current relative path set in the ResourceManager
                    self._current_path = current_resource_path
            else:
                self._log.Log("There is no handler registered to handle the specified filetype: %s for file: %s" % (extension.upper(), filename))
        
        return new_resource
    
    def _add_resource(self, new_resource):
        if not new_resource.rid in self._resources:
            self._resources[new_resource.rid] = new_resource
        else:
            self._log.Log("Resource already exists with id: %d filename: %s" % (new_resource.rid, new_resource.filename))
    
    def remove_resource(self, filename="", rid=-1):
        # Find the resource and remove it using the appropriate handler
        # Will the resource have to notify its manager owners?  or is this a cleanup
        pass
    
    def get_resource_by_id(self, rid):
        if rid in self._resources:
            return self._resources[rid]
        else:
            return None
    
    def get_resource_by_filename(self, filename):
        found_resource = None
        for rid in self._resources:
            if self._resources[rid].filename == filename:
                found_resource = self._resources[rid]
                break
        return found_resource
    
    # Temporary function to test loading the test XML scene.
    def load_scene(self, scenefile):
        # In future create full path to file based on ResourceManager file
        scenefile = os.path.join(os.path.dirname(__file__),"..",scenefile)
        self._scene_loader.load_scene_file(scenefile)
        
        
            
            
            
            
        

        