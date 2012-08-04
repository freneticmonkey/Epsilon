
from OpenGL.GL import *

# This renderer is attached to node objects in order to render meshes.
from epsilon.render.meshfactory import *
from epsilon.render.material import GLMaterial

from epsilon.scene.nodecomponent import NodeComponent

matrix_type = GLfloat * 16
matrix_typed = GLdouble * 16

class Renderer(NodeComponent):
    
    def __init__(self, mesh=None, material=None):
        NodeComponent.__init__(self)
        self._mesh = mesh
        self._material = material
        self._visible = True
        self._culled = False
    
    @property
    def material(self):
        return self._material
    
    @material.setter
    def material(self, new_mat):
        self._material = new_mat
    
    @property
    def mesh(self):
        return self._mesh
    
    @mesh.setter
    def mesh(self, new_mesh):
        self._mesh = new_mesh
        
        # If a mesh has been set 
        # Set a default material
        if not self._mesh is None:
            if self._material is None:
                self._material = GLMaterial()
    
    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, vis):
        self._visible = vis
#        for child in self._children:
#            child.visible = vis

    @property
    def culled(self):
        return self._culled
    
    @culled.setter
    def culled(self, set_culled):
        self._culled = set_culled
        
    # Draw
    def draw(self):
        
        if self._visible and not self._culled:
        
            self._setup_draw()
            
            # Draw bounds
#            if self._material:
#                self.node_parent.transform.bounds.colour = self._material.diffuse
#            self.node_parent.transform.bounds.debug_draw()
            
            # Set Material
            # Every node _must_ have a material from now on.
            # The renderer is moving to entirely Shader based rendering and
            # as such all meshes cannot be rendered without a material 
            # definition
            if self._mesh and self._material:
                self._material.draw(self._mesh.glmesh)
                
            # If there is a mesh defined and the bounds needs to be drawn
#            if not self._mesh is None and self._mesh.bounds.get_draw_bounds():
#                self._mesh.bounds.gizmo.draw(transform.position)
            
            
            self._teardown_draw()
            
    def _setup_draw(self):
        glPushMatrix()
        
        # Translate    
        glTranslate(*self.node_parent.transform.position)
        
        # Rotate
        glMultMatrixf(matrix_type(*self.node_parent.transform.rotation.get_matrix()))
        
        # Scale
        glScalef(*self.node_parent.transform._local_scale)
        
        
    def _teardown_draw(self):
        # Pop the Transform stack
        glPopMatrix()
    