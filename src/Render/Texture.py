
'''
Created on Oct 8, 2011

This class controls the loading and OpenGL setup for textures.

It should only be created by the TextureManager class

@author: scottporter
'''

import Image

from OpenGL.GL import *

from Logging import Logger


class Texture(object):
    
    def __init__(self, filename, name):
        self._name = name
        self._filename = filename
        self._opengl_id = None
        self._opengl_buffer = None
        self._size_x = None
        self._size_y = None
        self._loaded = False
    
    @property
    def name(self):
        return self._name
    
    def size(self):
        return [self._size_x, self._size_y]
    
    def width(self):
        return self._size_x
    
    def height(self):
        return self._size_y
        
    def Load(self):
        # Open the image file
        image = Image.open(self._filename)
        self._size_x = image.size[0]
        self._size_y = image.size[1]
        
        # Read the image data - I don't think we should hold onto this because
        # it will chew a lot of ram.
        self._opengl_buffer = None
        
        try:
            self._opengl_buffer = image.tostring("raw","RGBA",0,-1)
        except SystemError:
            self._opengl_buffer = image.tostring("raw","RGBX",0,-1)
        
        if self._opengl_buffer is not None:
            # Setup the GL Texture and its properties
            self._opengl_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self._opengl_id)
            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            
            # Copy image data into the Texture buffer
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self._size_x, self._size_y, 0, GL_RGBA, GL_UNSIGNED_BYTE, self._opengl_buffer )
            self._loaded = True
            Logger.Log("Texture Loaded: %s" % self._filename)
        else:
            Logger.Log("TextureError: Couldn't read: %s" % self._filename)
            
    def Delete(self):
        glDeleteTextures(1, self._opengl_id)

    def Set(self):
        if self._loaded:
            # Configure OpenGL to use the texture
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            glBindTexture(GL_TEXTURE_2D, self._opengl_id)
        
    def Unset(self):
        if self._loaded:
            glDisable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 0)
        
        
        
    
    
    
    
        
        