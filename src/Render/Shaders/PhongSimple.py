'''
Created on Dec 3, 2011

@author: scottporter
'''
import os

from OpenGL.GL import *
from OpenGL.GLU import *

from Render.Shader import ShaderProgram, VertexShader, FragmentShader

class PhongSimple(ShaderProgram):
    
    def __init__(self):
        vs = os.path.join("Render","Shaders","phong.vert")
        fs = os.path.join("Render","Shaders","phong.frag")
        ShaderProgram.__init__(self, VertexShader(vs), FragmentShader(fs))
        
    def _ConfigureProperties(self):
        pass
    
    def OnFrameStart(self):
        pass
    
    def Render(self, material, mesh):
        
        glEnableVertexAttribArray(self._vertex_position_attr_location)
        glEnableVertexAttribArray(self._vertex_normal_attr_location)
        
        with mesh.vertex_buffer as vb:
            glVertexAttribPointer(self._vertex_position_attr_location, *vb.GetVertexAttribute())
            glVertexAttribPointer(self._vertex_normal_attr_location, *vb.GetNormalAttribute())
            
            glDrawElements(GL_TRIANGLES, vb.count, GL_UNSIGNED_SHORT, vb.indices)
            
            glDisableVertexAttribArray(self._vertex_position_attr_location)
            glDisableVertexAttribArray(self._vertex_normal_attr_location)