'''
Created on Nov 19, 2011

@author: scottporter
'''

import os
import numpy

from OpenGL.GL import *
from OpenGL.GLU import *

from Logging import Logger

from Render.Shader import ShaderProgram, VertexShader, FragmentShader
from Render.Colour import Colour

from Scene.SceneManager import SceneManager

     
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
        self._global_ambient = Colour(.02,.02,.02,1.0)
        self._material_ambient = Colour(.2,.2,.2,1.0)
        self._material_diffuse = Colour(.5,.5,.5,1.0)
        self._material_specular = Colour(.2,.2,.2,1.0)
        self._material_shininess = 0.5
        
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
        
    def _configure_properties(self):
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
    def on_frame_start(self):
        # Configure the scene lights
        
        lights = SceneManager.get_instance().current_scene.lights
        
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
            with light.world_position as pos:
                light_data.append([pos.x, pos.y, pos.z, 1.0])
            #light_data.append([light.attenuation, 0.2, 0.5, 1.0])
            light_data.append([0.05, 0.02, 0.01, 0.0])
        
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
        self.use()
        glUniform4fv(self._uniform_locations['lights'], (self.MAX_LIGHTS * self.LIGHT_SIZE), light_data_np)
        
        # Set the Global ambient value
        u_loc = self._uniform_locations['Global_ambient']
        if self._global_ambient not in [None, -1]:
            with self._global_ambient as ga:
                glUniform4f(u_loc,ga.r,ga.g,ga.b,ga.a)
        self.disable()
            
    def render(self, material, mesh):
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
        
        
        
        
        
     

