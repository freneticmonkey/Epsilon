'''
Created on Mar 4, 2012

@author: scottporter
'''

from ResourceBase import ResourceType, ResourceBase
from ResourceHandler import ResourceHandlerBase

from Render.Texture import Texture
from Render.TextureManager import TextureManager

class ImageResourceHandler(ResourceHandlerBase):
    def __init__(self):
        ResourceHandlerBase.__init__(self)
        self._resource_type = ResourceType.IMAGE
        self._filetypes = ["jpg","png"]
        
    def process_resource(self, filename):
        
        new_texture = None
        # Does the Texture already exist in the Texture Manager
        for texture in TextureManager.get_instance().textures:
            if texture.filenanme == filename:
                new_texture = texture
                break
        
        # If the texture isn't in the texture manager
        if new_texture is None:
            # Load the image
            new_texture = Texture(filename=filename)
            
            # Add it to the TextureManager
            TextureManager.get_instance().add_texture(new_texture)
            
            # Create a Resource object that also contains the Texture object within the data property
            new_resource = Texture(filename=filename)
        
        # Return the new Resource
        return new_resource
        
    def remove_resource(self, resource):
        # Remove it from the TextureManager
        TextureManager.get_instance().remove_texture(resource)
        
        
        
        