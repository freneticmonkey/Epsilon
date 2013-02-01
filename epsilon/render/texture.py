
'''
Created on Oct 8, 2011

This class controls the loading and OpenGL setup for textures.

It should only be created by the TextureManager class

@author: scottporter
'''

#import Image

from pyglet import image

from OpenGL.GL import *

from epsilon.logging.logger import Logger

from epsilon.resource.resourcebase import ResourceBase, ResourceType

class Texture(ResourceBase):
    
    def __init__(self, filename, name=None):
        ResourceBase.__init__(self, filename=filename)
        self._type = ResourceType.IMAGE
        if name is None:
            name = "Texture_" + str(self._id)
        
        self._name = name
        self._opengl_id = None
        self._size_x = None
        self._size_y = None
        
        self._pyglet_image = None

        self._smoothed = True
        self._wrapped = True
        
    def __del__(self):
        if not self._opengl_id is None:
            glDeleteTextures(1, self._opengl_id)
            self._loaded = False
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name
    
    def size(self):
        return [self._size_x, self._size_y]
    
    def width(self):
        return self._size_x
    
    def height(self):
        return self._size_y

    @property
    def image(self):
        return self._pyglet_image

    @property
    def smoothed(self):
        return self._smoothed

    @smoothed.setter
    def smoothed(self, new_value):
        self._smoothed = new_value

    @property
    def wrapped(self):
        return self._wrapped

    @wrapped.setter
    def wrapped(self, new_value):
        self._wrapped = new_value
        
    def load(self):
        self._pyglet_image = image.load(self._filename)
        self._size_x = self._pyglet_image.width
        self._size_y = self._pyglet_image.height
        
        self._opengl_id = self._pyglet_image.get_texture().id
        self._loaded = True
        
#        # Open the image file
#        image = Image.open(self._filename)
#        self._size_x = image.size[0]
#        self._size_y = image.size[1]
#        
#        # Read the image data - I don't think we should hold onto this because
#        # it will chew a lot of ram.
#        self._opengl_buffer = None
#        
#        try:
#            self._opengl_buffer = image.tostring("raw","RGBA",0,-1)
#        except SystemError:
#            self._opengl_buffer = image.tostring("raw","RGBX",0,-1)
#        
#        if self._opengl_buffer is not None:
#            # Setup the GL Texture and its properties
#            self._opengl_id = glGenTextures(1)
#            glBindTexture(GL_TEXTURE_2D, self._opengl_id)
#            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
#            
#            # Copy image data into the Texture buffer
#            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self._size_x, self._size_y, 0, GL_RGBA, GL_UNSIGNED_BYTE, self._opengl_buffer )
#            
#            # Indicate that the texture has been loaded
#            self._loaded = True
#            Logger.Log("Texture Loaded: %s" % self._filename)
#        else:
#            Logger.Log("TextureError: Couldn't read: %s" % self._filename)
    
    def unload(self):
        if not self._opengl_id is None:
            glDeleteTextures(1, self._opengl_id)
            self._opengl_id = None
            self._loaded = False

    def set(self):
        if self._loaded:
            # Configure OpenGL to use the texture
            glEnable(GL_TEXTURE_2D)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

            glBindTexture(GL_TEXTURE_2D, self._opengl_id)

            if not self._smoothed:
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            # if self._wrapped:
            #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            # else:
            
            # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            
        
    def unset(self):
        if self._loaded:
            glDisable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 0)

    def bound_query(self):
        bt = glGetIntegerv(GL_TEXTURE_BINDING_2D)
        print "Bound texture: %d" % bt
        
        
        
class GeneratedTexture(Texture):

    def __init__(self, name=None, width=128, height=128, format="RGBA", data=None):
        Texture.__init__(self, "", name)
        self._size_x = width
        self._size_y = height
        self._format = format
        self._pyglet_image = image.create(self._size_x, self._size_y, image.CheckerImagePattern())
        self._opengl_id = self._pyglet_image.get_texture().id

        if data is not None:
            self.set_data(self._format, len(self._format) * self._size_x, data) 
        self._loaded = True
        
    def load(self):
        pass

    # Data param is an array of GLubyte s
    def set_data(self, format, pitch, data):
        if data is not None:
            self._format = format
            self._pitch = pitch
            self._pyglet_image.set_data(self._format, self._pitch, data)
            self._opengl_id = self._pyglet_image.get_texture().id

            #Logger.Log("GeneratedTexture: set_data(): Texture data changed: %d" % self._opengl_id)

            self._loaded = True
            # try:
            #     #loaded_data = image.ImageData(width, height, "RGBA", data)
            #     self._pyglet_image.blit_into(data,0,0,0)
            # except:
            #     Logger.Log("GeneratedTexture: set_data(): Unable to bind texture data")
        else:
            Logger.Log("GeneratedTexture: set_data(): Texture data is None")




    
    
        
        