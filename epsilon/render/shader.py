'''
Created on Sep 25, 2011

@author: scottporter
'''
import os

from ctypes import byref, c_char, c_char_p, c_int, cast, create_string_buffer, pointer, POINTER
from OpenGL.GL import *
from OpenGL.GL.shaders import *

from epsilon.geometry.euclid import Vector2, Vector3, Matrix3, Matrix4
from epsilon.render.colour import Colour
from epsilon.render.texture import Texture

from epsilon.logging.logger import Logger

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
        #glGetShaderInfoLog(self._id, length, None, buffer)
        buffer = glGetShaderInfoLog(self._id)
        return buffer#.value
    
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
            print "ERROR: Shader Compile Fail:\nErrors:"

            # Print compile errors
            for arg in e.args:
                if type(arg).__name__ == 'str':
                    print arg
                elif type(arg).__name__ == 'list':

                    #print source
                    for source in arg:
                        line_count = 1
                        for line in source.split('\n'):
                            print "%d : %s" % ( line_count, line )
                            line_count +=1
                        print ""
        
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
                print "No error info Log."#" for source:"
                #print "\n".join(self._shader_source)
            raise CompileError(info)
        

class VertexShader(Shader):
    _shader_type = GL_VERTEX_SHADER

class GeometryShader(Shader):
    _shader_type = GL_GEOMETRY_SHADER
    
class FragmentShader(Shader):
    _shader_type = GL_FRAGMENT_SHADER    

class ShaderProgram(object):
    
    def __init__(self, *shaders):
        self._shaders = list(shaders)
        self._id = None
        
        self._uniform_names = []
        self._attribute_names = []

        self._uniform_locations = {}
        self._attribute_locations = {}
        self._attribute_locations_valid = False
        self._name = self.__class__.__name__

    def __enter__(self):
        self.use()
        return self
        
    def __exit__(self, type, value, traceback):
        self.disable()

    @property
    def name(self):
        return self._name
        
    def get_param(self, param_id):
        outvalue = c_int(0)
        glGetProgramiv(self._id, param_id, byref(outvalue))
        value = outvalue.value
        if value in ShaderConstants.shader_errors.keys():
            msg = "%s from glGetProgram(%s, %s, &value)"
            raise ValueError(msg % (ShaderConstants.shader_errors[value], self._id, param_id))
        return value

    # Helper functions for handling repetitive Shader Code.
    def _configure_properties(self):

        problems_detected = False

        # Get the Memory locations of the Shader Uniforms
        for uniform_name in self._uniform_names:
            u_loc = self.get_gl_uniform_location(uniform_name)
            if u_loc is not None:
                self._uniform_locations[uniform_name] = u_loc
            else:
                problems_detected = True
                
        # Get the Memory locations of the Shader Attributes
        self._attribute_locations_valid = True
        for attribute_name in self._attribute_names:
            a_loc = self.get_gl_attribute_location(attribute_name)
            if a_loc is not None:
                self._attribute_locations[attribute_name] = a_loc                
            else:
                self._attribute_locations_valid = False
                problems_detected = True

        # If problems were detected during configure, display the shader
        # unforms and attributes
        if problems_detected:
            Logger.Log("WARNING: Problems were detected configuring shader: %s\n" % self._name)
        self.display_shader_inputs()
            
    def display_shader_inputs(self):
        info_text = "Shader Inputs for: %s\n" % self._name
        num_uniforms = self.get_param(GL_ACTIVE_UNIFORMS)
        if num_uniforms > 0:
            info_text += "Shader Uniforms\n"
            for i in range(num_uniforms):
                name, size, gltype = glGetActiveUniform(self._id, i)
                info_text += "u: %s\n" % name
        else:
            info_text += "No Shader Uniforms detected\n"

        num_attributes = self.get_param(GL_ACTIVE_ATTRIBUTES)
        if num_attributes > 0:
            info_text += "Shader Attributes\n"
            for i in range(num_attributes):
                name, size, gltype = glGetActiveAttrib(self._id, i)
                
                info_text += "a: %s\n" % name
        else:
            info_text += "No Shader Attributes detected\n"

        Logger.Log(info_text)

    def get_gl_uniform_location(self, name):
        # Get the Memory locations of the Shader Attributes
        uniform_location_request = glGetUniformLocation(self._id, name)
        uniform_location = None
        if not uniform_location_request in [None,-1]:
                uniform_location = uniform_location_request
        else:
            Logger.Log("Shader error: %s: uniform not found: %s" % (self._name, name) )
        return uniform_location

    def get_uniform_location(self, name):
        loc = None
        if name in self._uniform_locations:
            loc = self._uniform_locations[name]
        return loc

    def get_gl_attribute_location(self, name):
        # Get the Memory locations of the Shader Attributes
        attribute_location_request = glGetAttribLocation(self._id, name)
        attribute_location = None
        if not attribute_location_request in [None,-1]:
                attribute_location = attribute_location_request
        else:
            Logger.Log("Shader error: %s: attribute not found: %s" % (self._name, name) )
        return attribute_location

    def get_attribute_location(self, name):
        loc = None
        if name in self._attribute_locations:
            loc = self._attribute_locations[name]
        return loc

    def attributes_valid(self):
        return self._attribute_locations_valid

    def set_uniform_data(self, name, data):
        if name in self._uniform_locations:
            u_loc = self._uniform_locations[name]

            if type(data) == Colour:
                glUniform4f(u_loc, data.r, data.g, data.b, data.a)

            elif type(data) == Vector2:
                glUniform2f(u_loc, 1, GL_FALSE, data.x, data.y)

            elif type(data) == Vector3:
                glUniform3f(u_loc, 1, GL_FALSE, data.x, data.y, data.z)

            elif type(data) == Matrix3:
                glUniformMatrix3fv(u_loc, 1, GL_FALSE, data[:])

            elif type(data) == Matrix4:
                glUniformMatrix4fv(u_loc, 1, GL_FALSE, data[:])

            elif type(data) == Texture:
                glUniform1i(u_loc, 0)#data.opengl_id)

            elif type(data) == int:
                glUniform1i(u_loc, data)

            elif type(data) == float:
                glUniform1f(u_loc, data)
            
            # TODO: Add other data types here.

            else:
                Logger.Log("WARNING: Binding an unhanded data type to shader. Shader: %s\nuniform: %s\nDataType: %s \n" % ( self._name, name, type(data).__class__.__name__))
        # else:
        #     Logger.Log("WARNING: Unknown uniform on shader. Shader: %s\nuniform: %s\nDataType: %s \n" % ( self._name, name, type(data).__class__.__name__))

    # FIXME/TODO: This is hardcoded so that all attributes are treated as arrays.
    #             This is clearly not correct but for now only. Fix to check for types asap.
    def enable_attribute_arrays(self):
        for attribute in self._attribute_locations.values():
            glEnableVertexAttribArray(attribute)

    def disable_attribute_arrays(self):
        for attribute in self._attribute_locations.values():
            glDisableVertexAttribArray(attribute)
    
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
            log = None#shader.get_info_log()
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
    
    # This is called by the Shader Manager at the start of a Frame
    # This is a stub for child classes     
    def on_frame_start(self):
        pass
    
    def use(self):
        glUseProgram(self._id)
        
    def disable(self):
        glUseProgram(0)