'''
Created on Dec 3, 2011

@author: scottporter
'''
import os

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.render.shader import ShaderProgram, VertexShader, FragmentShader#, GeometryShader
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
                                'material.shininess',
                                'diffuse_texture'
                              ]
        self._attribute_names = ['Vertex_position',
                                 'Vertex_normal',
                                 'Vertex_texture_coordinate']
        
    def on_frame_start(self):
        # Send the light data through to the Shader Video Memory
        self.use()

        # Set the Global ambient value
        self.set_uniform_data('Global_ambient', self._global_ambient)
        
        self.disable()
    
    def render(self, material, mesh):
        self.set_uniform_data('material.ambient', material.ambient)
        self.set_uniform_data('material.diffuse', material.diffuse)
        self.set_uniform_data('material.specular', material.specular)
        self.set_uniform_data('material.shininess', material.shininess)

        if self.attributes_valid():
            self.enable_attribute_arrays()
        
        if mesh.vertex_buffer.is_setup:
            with mesh.vertex_buffer as vb:
                if self.attributes_valid():
                    glVertexAttribPointer(self.get_attribute_location("Vertex_position"), *vb.GetVertexAttribute())
                    glVertexAttribPointer(self.get_attribute_location("Vertex_normal"), *vb.GetNormalAttribute())
                    glVertexAttribPointer(self.get_attribute_location("Vertex_texture_coordinate"), *vb.GetTexCoordAttribute())
                
                glDrawElements(GL_TRIANGLES, vb.count, GL_UNSIGNED_SHORT, vb.indices)
        
        if self.attributes_valid():
            self.disable_attribute_arrays()