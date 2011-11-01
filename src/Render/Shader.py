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

from Scene.SceneManager import *

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
        
        self._id = compileShader(self._shader_source, self._shader_type)
        
#        num, src = self.ShaderSourceToArray()
#        for source in src:
##            source = src[0]
##            glShaderSource(self._id, num, src, None)
##            self._id = glShaderSource(source, self._shader_type)
#            
#            self._id = compileShader(source, self._shader_type)
            
#            glCompileShader(self._id)
            
        if not self.GetCompileStatus():
            raise CompileError(self.GetInfoLog())
        

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
        glGetProgramInfoLog(self._id, length, None, buffer)
        return buffer.value
        
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
        
# This is a temporary class for complex lighting.
# The attributes need to be read from the compiled source files and added to the 
# class using setattr etc.  There isn't really any point in implementing this 
# functionality until there is some kind of editing interface

class PhongShader(ShaderProgram):
    
    MAX_LIGHTS = 3
    LIGHT_SIZE = 5
    
    def __init__(self):
        vs = os.path.join("Render","Shaders","comp_lighting.vert")
        fs = os.path.join("Render","Shaders","comp_lighting.frag")
        ShaderProgram.__init__(self, VertexShader(vs), FragmentShader(fs))
        
        # Uniform Values - Need to fix the Colour class first
        self._global_ambient = Colour(.05,.05,.05,1.0)
        self._material_ambient = Colour(.2,.2,.2,1.0)
        self._material_diffuse = Colour(.5,.5,.5,1.0)
        self._material_specular = Colour(.8,.8,.8,1.0)
        self._material_shininess = 2.0
        
        self._uniform_names = [ 'Global_ambient',
                                'material.ambient',
                                'material.diffuse',
                                'material.specular',
                                'material.shininess'
                              ]
        self._uniform_locations = {}
        self._vertex_position_attr_location = None
        self._vertex_normal_attr_location = None
        
        self._lights = []
        
    @property
    def global_ambient(self):
        return self._global_ambient
    
    ### And so on.
        
    def _ConfigureProperties(self):
        # Get the Memory locations of the Shader Uniforms
        for uniform_name in self._uniform_names:
            location = glGetUniformLocation(self._id, uniform_name)
            
            if not location in [None,-1]:
                self._uniform_locations[uniform_name] = location
            else:
                Logger.Log("Shader error: uniform not found: " + uniform_name)
            
        self._uniform_locations['lights'] = glGetUniformLocation(self._id, 'lights')
        
        # Get the Memory locations of the Shader Attributes
        location = glGetAttribLocation(self._id, "Vertex_position")
        if not location in [None,-1]:
                self._vertex_position_attr_location = location
        else:
            Logger.Log("Shader error: uniform not found: vertex_position")
        
        location = glGetAttribLocation(self._id, "Vertex_normal")
        if not location in [None,-1]:
                self._vertex_normal_attr_location = location
        else:
            Logger.Log("Shader error: attribute not found: vertex_normal" )
        
    # This is called by the Shader Manager at the start of a Frame    
    def OnFrameStart(self):
         # Configure the scene lights
         
        lights = GetSceneManager().lights
        
        light_data = []
        
        # At this point I don't know enough about Shaders to know
        # what the behaviour of the Shader is if the light structure
        # isn't full in video memory
        
        # If there aren't enough lights in the scene to satisfy the shader
        # calculate how many 'empty' lights need to be created
        inc_count = self.MAX_LIGHTS
        inc_rm_count = 0
        if len(lights) < self.MAX_LIGHTS:
            inc_count = len(lights)
            inc_rm_count = self.MAX_LIGHTS - len(lights)
        
        # Set the scene's light properties inside the Shader
        for i in range(0, inc_count):
            light = lights[i]
            with light.ambient as am:
                light_data.append([am.r, am.g, am.b, am.a])
            with light.diffuse as dif:
                light_data.append([dif.r, dif.g, dif.b, dif.a])
            with light.specular as spec:
                light_data.append([spec.r, spec.g, spec.b, spec.a])
            with light.position as pos:
                light_data.append([pos.x, pos.y, pos.z, 1.0])
            light_data.append([light.attenuation, 0.0, 0.0, 1.0])
        
        # (If necessary) fill the video memory structure with empty lights 
        for i in range(0, inc_rm_count):
            light_data.append([0.0, 0.0, 0.0, 0.0])
            light_data.append([0.0, 0.0, 0.0, 0.0])
            light_data.append([0.0, 0.0, 0.0, 0.0])
            light_data.append([0.0, 0.0, 0.0, 0.0])
            light_data.append([0.0, 0.0, 0.0, 0.0])
            
        # create a numpy array for the data
        light_data_np = numpy.array(light_data, 'f')
        
        # Send the light data through to the Shader Video Memory
        self.Use()
        glUniform4fv(self._uniform_locations['lights'], (self.MAX_LIGHTS * self.LIGHT_SIZE), light_data_np)
        
        # Set the Global ambient value
        u_loc = self._uniform_locations['Global_ambient']
        if self._global_ambient not in [None, -1]:
            with self._global_ambient as ga:
                glUniform4f(u_loc,ga.r,ga.g,ga.b,ga.a)
        self.Disable()
            
    def Render(self, material, mesh):
        u_loc = self._uniform_locations['material.ambient']
        if u_loc not in [None, -1]:
            with material.ambient as ma:
                glUniform4f(u_loc,ma.r,ma.g,ma.b,ma.a)
        
        u_loc = self._uniform_locations['material.diffuse']
        if u_loc not in [None, -1]:
            with material.diffuse as md:
                glUniform4f(u_loc,md.r,md.g,md.b,md.a)
                
        u_loc = self._uniform_locations['material.specular']
        if u_loc not in [None, -1]:
            with material.specular as ms:
                glUniform4f(u_loc,ms.r,ms.g,ms.b,ms.a)
                
        u_loc = self._uniform_locations['material.shininess']
        if u_loc not in [None, -1]:
            glUniform1f(u_loc,material.shininess)
        
        glEnableVertexAttribArray(self._vertex_position_attr_location)
        glEnableVertexAttribArray(self._vertex_normal_attr_location)
        
        with mesh.vertex_buffer as vb:
            glVertexAttribPointer(self._vertex_position_attr_location, *vb.GetVertexAttribute())
            glVertexAttribPointer(self._vertex_normal_attr_location, *vb.GetNormalAttribute())
            
            glDrawElements(GL_TRIANGLES, vb.count, GL_UNSIGNED_SHORT, vb.indices)
            
            glDisableVertexAttribArray(self._vertex_position_attr_location)
            glDisableVertexAttribArray(self._vertex_normal_attr_location)
        
        
        
        
        
     

