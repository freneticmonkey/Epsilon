'''
Created on Dec 3, 2011

@author: scottporter
'''
import os

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.render.shader import ShaderProgram, VertexShader, FragmentShader#, GeometryShader
from epsilon.render.colour import Colour

from epsilon.scene.scenemanager import SceneManager
from epsilon.render.texturemanager import TextureManager

from epsilon.core.coreevents import QuitEvent

class Phong3(ShaderProgram):
    
    def __init__(self):
        
        shader_source_dir = os.path.dirname(__file__)
        vs = os.path.join(shader_source_dir,"phong3.vert")
        fs = os.path.join(shader_source_dir,"phong3.frag")
        ShaderProgram.__init__(self, VertexShader(vs), FragmentShader(fs))
        
        self._uniform_names = [ 'model',
                                'view',
                                'proj',
                                'lightPosition',
                                'diffuse_texture'
                                # 'material.diffuse',
                                # 'material.specular',
                                # 'material.shininess',
                                # 'diffuse_texture'
                              ]
        self._attribute_names = ['position',
                                 'normal',
                                 'colour',
                                 'texture_coordinate'
                                ]
        
    def on_frame_start(self):
        # Set the proj matrix
        projection = SceneManager.get_current_scene().active_camera.projection_matrix
        camera_pos = SceneManager.get_current_scene().active_camera.node_parent.transform.world_matrix
        if projection:
            #projection.inverse()
            self.set_uniform_data('proj', projection)
        if camera_pos:
            #camera_pos.transpose()
            self.set_uniform_data('view', camera_pos)

        lights = SceneManager.get_current_scene().lights
        if len(lights) > 0:
            light_pos = lights[0].transform.position
            self.set_uniform_data('lightPosition', light_pos)
    
    def render(self, material, mesh, transform):
        # self.set_uniform_data('material.ambient', material.ambient)
        # self.set_uniform_data('material.diffuse', material.diffuse)
        # self.set_uniform_data('material.specular', material.specular)
        # self.set_uniform_data('material.shininess', material.shininess)

        # this is a kind of roundabout of accessing this
        world_mat = transform.world_matrix
        #world_mat.transpose()
        self.set_uniform_data('model', world_mat)

        texture = TextureManager.get_instance().get_texture_by_name( material.texture )
        if texture is not None:
            self.set_uniform_data('diffuse_texture', texture)

        if self.attributes_valid():
            self.enable_attribute_arrays()
        
        if mesh.vertex_buffer.is_setup:
            with mesh.vertex_buffer as vb:
                if self.attributes_valid():
                    glVertexAttribPointer(self.get_attribute_location("position"), *vb.GetVertexAttribute())
                    glVertexAttribPointer(self.get_attribute_location("normal"), *vb.GetNormalAttribute())
                    glVertexAttribPointer(self.get_attribute_location("colour"), *vb.GetColourAttribute())
                    glVertexAttribPointer(self.get_attribute_location("texture_coordinate"), *vb.GetTexCoordAttribute())
                
                glDrawElements(GL_TRIANGLES, vb.count, GL_UNSIGNED_SHORT, vb.indices)
        
        if self.attributes_valid():
            self.disable_attribute_arrays()

        #QuitEvent().send()