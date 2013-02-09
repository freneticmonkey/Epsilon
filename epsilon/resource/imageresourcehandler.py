'''
Created on Mar 4, 2012

@author: scottporter
'''

from epsilon.resource.resourcebase import ResourceType, ResourceBase
from epsilon.resource.resourcehandler import ResourceHandlerBase

from epsilon.render.texture import Texture
from epsilon.render.texturemanager import TextureManager

class ImageResourceHandler(ResourceHandlerBase):
    def __init__(self):
        ResourceHandlerBase.__init__(self)
        self._resource_type = ResourceType.IMAGE
        self._filetypes = ["jpg","png"]
        
    def process_resource(self, filename, name):
        
#        new_texture = None
        # Does the Texture already exist in the Texture Manager
        new_texture = TextureManager.get_instance().get_texture_by_filename(filename)
#        for texture in TextureManager.get_instance().textures:
#            if texture.filename == filename:
#                new_texture = texture
#                break
        
        # If the texture isn't in the texture manager
        if new_texture is None:
            # Load the image
            new_texture = Texture(filename=filename, name=name)
            
            # Add it to the TextureManager
            TextureManager.get_instance().add_texture(new_texture)
            
            # Create a Resource object that also contains the Texture object within the data property
#            new_resource = Texture(filename=filename)
        
        # Return the new Resource
        return new_texture
        
    def remove_resource(self, resource):
        # Remove it from the TextureManager
        TextureManager.get_instance().remove_texture(resource)
        
        
        
        