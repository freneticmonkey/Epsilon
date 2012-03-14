'''
Created on Sep 25, 2011

@author: scottporter
'''
import os
import numpy
from ctypes import byref, c_char, c_char_p, c_int, cast, create_string_buffer, pointer, POINTER
from OpenGL.GL import *
from OpenGL.GL.shaders import *

from Render.Colour import Colour
from Logging import Logger

class ShaderError(Exception):
    pass

class CompileError(ShaderError):
    pass

class LinkError(ShaderError):
    pass

class ShaderConstants:
    shader_errors = {
                     GL_INVALID_VALUE: "GL_INVALID_VALUE (bad 1st argument)",
                     GL_INVALID_OPERATION: "GL_INVALID_OPERATION (bad id or immediate drawing mode in progress",
                     GL_INVALID_ENUM:"GL_INVALID_ENUM (bad 2nd argument)"
                    }

class Shader(object):
    
    _shader_type = None
    
    def __init__(self, files):
        if isinstance(files, basestring):
            self._files = [files]
        else:
            self._files = files
        
        self._shader_source = None
        self._id = None
    
    # Get Shader Parameter
    def GetParam(self, param_id):
        outvalue = c_int(0)
        glGetShaderiv(self._id, param_id, byref(outvalue))
        value = outvalue.value
        if value in ShaderConstants.shader_errors.keys():
            msg = '%s from glGetShader(%s, %s, &value)'
            raise ValueError(msg % (ShaderConstants.shader_errors[value], self._id, param_id))
        return value
    
    # Get the compile status of the Shader
    def GetCompileStatus(self):
        return bool(self.GetParam(GL_COMPILE_STATUS))
    
    # Get the length of the Shader info log
    def GetInfoLogLength(self):
        return self.GetParam(GL_INFO_LOG_LENGTH)
    
    # Get the Info Log of the shader
    def GetInfoLog(self):
        length = self.GetInfoLogLength()
        if length == 0:
            return ""
        buffer = create_string_buffer(length)
        glGetShaderInfoLog(self._id, length, None, buffer)
        return buffer.value
    
    def ShaderSourceToArray(self):
        num = len(self._shader_source)
        all_source = (c_char_p * num)(*self._shader_source)
        return num, cast(pointer(all_source), POINTER(POINTER(c_char)))
    
    # Read the contents of a file
    def LoadSource(self, fname):
        with open(fname) as fp:
            src = fp.read()
        return src
    
    # Load the source for all of the Shader source files
    def LoadShaderSource(self):
        return [self.LoadSource(fname) for fname in self._files]
    
    # Compile the Shader
    def Compile(self):
        self._id = glCreateShader(self._shader_type)
        self._shader_source = self.LoadShaderSource()
        
        try:
            self._id = compileShader(self._shader_source, self._shader_type)
        except RuntimeError, e:
            print "ERROR: Shader Compile Fail\n" + e.message
        
#        num, src = self.ShaderSourceToArray()
#        for source in src:
##            source = src[0]
##            glShaderSource(self._id, num, src, None)
##            self._id = glShaderSource(source, self._shader_type)
#            
#            self._id = compileShader(source, self._shader_type)
            
#            glCompileShader(self._id)
            
        if not self.GetCompileStatus():
            info = self.GetInfoLog()
            if len(info) == 0:
                print "No error Log for source:"
                print "\n".join(self._shader_source)
            raise CompileError(info)
        

class VertexShader(Shader):
    _shader_type = GL_VERTEX_SHADER
    
class FragmentShader(Shader):
    _shader_type = GL_FRAGMENT_SHADER    

class ShaderProgram(object):
    
    def __init__(self, *shaders):
        self._shaders = list(shaders)
        self._id = None
        
    def __enter__(self):
        self.Use()
        return self
        
    def __exit__(self, type, value, traceback):
        self.Disable()
        
    def GetParam(self, param_id):
        outvalue = c_int(0)
        glGetProgramiv(self._id, param_id, byref(outvalue))
        value = outvalue.value
        if value in ShaderConstants.shader_errors.keys():
            msg = "%s from glGetProgram(%s, %s, &value)"
            raise ValueError(msg % (ShaderConstants.shader_errors[value], self._id, param_id))
        return value
    
    def GetLinkStatus(self):
        return bool(self.GetParam(GL_LINK_STATUS))
    
    # Get the length of the Shader info log
    def GetInfoLogLength(self):
        return self.GetParam(GL_INFO_LOG_LENGTH)
    
    # Get the Info Log of the shader
    def GetInfoLog(self):
        length = self.GetInfoLogLength()
        if length == 0:
            return ""
        buffer = create_string_buffer(length)
        buffer = glGetProgramInfoLog(self._id)#, buffer)#length, None, buffer)
        return buffer#.value
        
    def GetMessage(self):
        messages = []
        for shader in self._shaders:
            log = shader.GetInfoLog()
            if log:
                messages.append(log)
        log = self.GetInfoLog()
        if log:
            messages.append(log)
        return "\n".join(messages)
    
    def Compile(self):
        self._id = glCreateProgram()
        
        for shader in self._shaders:
            shader.Compile()
            glAttachShader(self._id, shader._id)
            
        glLinkProgram(self._id)
        
        message = self.GetMessage()
        if not self.GetLinkStatus():
            raise LinkError(message)
        else:
            self._ConfigureProperties()
        
        return message
    
    # This is a stub for child classes
    def _ConfigureProperties(self):
        pass
    
    # This is called by the Shader Manager at the start of a Frame
    # This is a stub for child classes     
    def OnFrameStart(self):
        pass
    
    def Use(self):
        glUseProgram(self._id)
        
    def Disable(self):
        glUseProgram(0)