'''
Created on Dec 3, 2011

@author: scottporter
'''
import os

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.logging import Logger

from epsilon.render.shader import ShaderProgram, VertexShader, FragmentShader
from epsilon.render.colour import Colour

class PhongSimple(ShaderProgram):
    
    def __init__(self):
        
        shader_source_dir = os.path.dirname(__file__)
        vs = os.path.join(shader_source_dir,"phong.vert")
        fs = os.path.join(shader_source_dir,"phong.frag")
        ShaderProgram.__init__(self, VertexShader(vs), FragmentShader(fs))
        self._global_ambient = Colour(.02,.02,.02,1.0)
        
        self._uniform_names = [ 'Global_ambient',
                                'material.ambient',
                                'material.diffuse',
                                'material.specular',
                                'material.shininess'
                              ]
        self._uniform_locations = {}
        
        self._vertex_position_attr_location = None
        self._vertex_normal_attr_location = None
        
    def _configure_properties(self):
        # Get the Memory locations of the Shader Uniforms
        for uniform_name in self._uniform_names:
            location = glGetUniformLocation(self._id, uniform_name)
            
            if not location in [None,-1]:
                self._uniform_locations[uniform_name] = location
            else:
                Logger.Log("Shader error: uniform not found: " + uniform_name)
        
        # Get the Memory locations of the Shader Attributes
        location = glGetAttribLocation(self._id, "Vertex_position")
        if not location in [None,-1]:
                self._vertex_position_attr_location = location
        else:
            Logger.Log("Shader error: attribute not found: Vertex_position")
        
        location = glGetAttribLocation(self._id, "Vertex_normal")
        if not location in [None,-1]:
                self._vertex_normal_attr_location = location
        else:
            Logger.Log("Shader error: attribute not found: Vertex_normal" )
    
    def on_frame_start(self):
        # Send the light data through to the Shader Video Memory
        self.use()
        
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
        
        if not self._vertex_position_attr_location is None and not self._vertex_normal_attr_location is None:
            glEnableVertexAttribArray(self._vertex_position_attr_location)
            glEnableVertexAttribArray(self._vertex_normal_attr_location)
        
        with mesh.vertex_buffer as vb:
            if not self._vertex_position_attr_location is None and not self._vertex_normal_attr_location is None:
                glVertexAttribPointer(self._vertex_position_attr_location, *vb.GetVertexAttribute())
                glVertexAttribPointer(self._vertex_normal_attr_location, *vb.GetNormalAttribute())
            
            glDrawElements(GL_TRIANGLES, vb.count, GL_UNSIGNED_SHORT, vb.indices)
            
            if not self._vertex_position_attr_location is None and not self._vertex_normal_attr_location is None:
                glDisableVertexAttribArray(self._vertex_position_attr_location)
                glDisableVertexAttribArray(self._vertex_normal_attr_location)