
#PyOpenGL types
#from epsilon.render.meshfactory import *
from OpenGL.GL import *
from OpenGL.GLU import *

matrix_type = GLfloat * 16
matrix_typed = GLdouble * 16

from epsilon.render.mesh import Mesh
from epsilon.render.colour import Preset

from epsilon.environment.planet.cubespheremap import CubeSphereMap

class SphereSurface(object):
    
    # parameters are the bounds of the region in which the sphere surface needs to 
    # be generated 
    def __init__(self, bound_min_x=0.0, 
                       bound_max_x=1.0, 
                       bound_min_z=0.0, 
                       bound_max_z=1.0, 
                       increments=10,
                       radius=1.0, 
                       face=CubeSphereMap.TOP):
        
        # Ensure that the bounds can be used to generate a valid mesh
        if bound_min_x >= bound_max_x:
            err = "SphereSurface: X Bounds are invalid. min x: %3.2f, max x: %3.2f" % (bound_min_x, 
                                                                                       bound_max_x
                                                                                      )
            raise ValueError( err )
        
        if bound_min_z >= bound_max_z:
            err = "SphereSurface: Z Bounds are invalid. min z: %3.2f, max z: %3.2f" % (bound_min_z, 
                                                                                       bound_max_z)
            raise ValueError( err )
        
        self._increments = increments
        self._bound_min_x = bound_min_x
        self._bound_max_x = bound_max_x
        self._bound_min_z = bound_min_z
        self._bound_max_z = bound_max_z
        
        self._radius = radius
        
        self._face = face
        
        self._mesh = None
        self._gen_mesh()
        
    @property
    def mesh(self):
        return self._mesh
        
    def _gen_mesh(self):
        verts = []
        for i in xrange(self._increments + 1):
            #c = i * (1.0 / self._increments)
            c = (i * ( (self._bound_max_x - self._bound_min_x) / float(self._increments) ) ) + self._bound_min_x
            
            for j in xrange(self._increments + 1):
                #r = j * ( 1.0 / self._increments )
                r = (j * ( (self._bound_max_z - self._bound_min_z) / float(self._increments) ) ) + self._bound_min_z
                
                p = CubeSphereMap.get_sphere_vector(c, r, self._face) * self._radius
                verts.append((p.x, p.y, p.z))
                
        faces = []
        v = 0
        for c in xrange(self._increments):
            for r in xrange(self._increments):
                bl = v + c + r
                tl = bl + 1
                tr = tl + self._increments + 1
                br = tr - 1
                
                faces.append((bl, tl, tr))
                faces.append((bl, tr, br))
            v = v + self._increments
        
        tex_coords = []
        for i in xrange(self._increments + 1):
            c = i * (1.0 / self._increments)
            for j in xrange(self._increments + 1):
                r = j * ( 1.0 / self._increments )
                y = j/self._increments
                p = [c,r] 
                tex_coords.append(p)
            
        # Build a mesh
        self._mesh = Mesh(verts, faces, Preset.green, tex_coords=tex_coords)    
    
        
        