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
    def get_param(self, param_id):
        outvalue = c_int(0)
        glGetShaderiv(self._id, param_id, byref(outvalue))
        value = outvalue.value
        if value in ShaderConstants.shader_errors.keys():
            msg = '%s from glGetShader(%s, %s, &value)'
            raise ValueError(msg % (ShaderConstants.shader_errors[value], self._id, param_id))
        return value
    
    # Get the compile status of the Shader
    def get_compile_status(self):
        return bool(self.get_param(GL_COMPILE_STATUS))
    
    # Get the length of the Shader info log
    def get_info_log_length(self):
        return self.get_param(GL_INFO_LOG_LENGTH)
    
    # Get the Info Log of the shader
    def get_info_log(self):
        length = self.get_info_log_length()
        if length == 0:
            return ""
        buffer = create_string_buffer(length)
        glGetShaderInfoLog(self._id, length, None, buffer)
        return buffer.value
    
    def shader_source_to_array(self):
        num = len(self._shader_source)
        all_source = (c_char_p * num)(*self._shader_source)
        return num, cast(pointer(all_source), POINTER(POINTER(c_char)))
    
    # Read the contents of a file
    def load_source(self, fname):
        with open(fname) as fp:
            src = fp.read()
        return src
    
    # Load the source for all of the Shader source files
    def load_shader_source(self):
        return [self.load_source(fname) for fname in self._files]
    
    # Compile the Shader
    def compile(self):
        self._id = glCreateShader(self._shader_type)
        self._shader_source = self.load_shader_source()
        
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
            
        if not self.get_compile_status():
            info = self.get_info_log()
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
        self.use()
        return self
        
    def __exit__(self, type, value, traceback):
        self.disable()
        
    def get_param(self, param_id):
        outvalue = c_int(0)
        glGetProgramiv(self._id, param_id, byref(outvalue))
        value = outvalue.value
        if value in ShaderConstants.shader_errors.keys():
            msg = "%s from glGetProgram(%s, %s, &value)"
            raise ValueError(msg % (ShaderConstants.shader_errors[value], self._id, param_id))
        return value
    
    def get_link_status(self):
        return bool(self.get_param(GL_LINK_STATUS))
    
    # Get the length of the Shader info log
    def get_info_log_length(self):
        return self.get_param(GL_INFO_LOG_LENGTH)
    
    # Get the Info Log of the shader
    def get_info_log(self):
        length = self.get_info_log_length()
        if length == 0:
            return ""
        buffer = create_string_buffer(length)
        buffer = glGetProgramInfoLog(self._id)#, buffer)#length, None, buffer)
        return buffer#.value
        
    def get_message(self):
        messages = []
        for shader in self._shaders:
            log = shader.get_info_log()
            if log:
                messages.append(log)
        log = self.get_info_log()
        if log:
            messages.append(log)
        return "\n".join(messages)
    
    def compile(self):
        self._id = glCreateProgram()
        
        for shader in self._shaders:
            shader.compile()
            glAttachShader(self._id, shader._id)
            
        glLinkProgram(self._id)
        
        message = self.get_message()
        if not self.get_link_status():
            raise LinkError(message)
        else:
            self._configure_properties()
        
        return message
    
    # This is a stub for child classes
    def _configure_properties(self):
        pass
    
    # This is called by the Shader Manager at the start of a Frame
    # This is a stub for child classes     
    def on_frame_start(self):
        pass
    
    def use(self):
        glUseProgram(self._id)
        
    def disable(self):
        glUseProgram(0)