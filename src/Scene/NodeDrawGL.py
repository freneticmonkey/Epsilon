'''
Created on Sep 18, 2011

@author: scottporter
'''

from OpenGL.GL import *
#from OpenGL.GLU import *

from Geometry.euclid import Matrix4, Vector3, Quaternion

matrix_type = GLfloat * 16

matrix_typed = GLdouble * 16

def DrawNode(node):
    
    if node.visible:
        
        glPushMatrix()
            
        # Translate    
        glTranslate(*node.local_position)
        
        # Rotate
        glMultMatrixf(matrix_type(*node.local_rotation.get_matrix()))
        
        # Scale
        glScalef(*node.local_scale)
        
            
        # Draw Light
#        if node.light:
#            node.light.Draw()
            
        # Set Material
        # Every node _must_ have a material from now on.
        # The renderer is moving to entirely Shader based rendering and
        # as such all meshes cannot be rendered without a material 
        # definition
        
        if node.mesh and node.material:
            node.material.Draw(node.mesh.glmesh)
#        if node.material:
#            node.material.SetupMaterial()
#        
#        # Draw Mesh
#        if node.mesh:
#            if node.mesh.glmesh:
#                node.mesh.glmesh.Draw()
#                
#        if node.material:
#            node.material.UnsetMaterial()
        
        # Draw Children    
        for child in node.children:
            DrawNode(child)
    
        # Pop the Transform stack
        glPopMatrix()
        

