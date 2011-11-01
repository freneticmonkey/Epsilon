'''
Created on Sep 18, 2011

@author: scottporter
'''

from Render.Mesh import *
from Render.Colour import *
from math import sqrt, pi, sin, cos
import itertools




# This class generates the necessary data for a specific mesh object
# and returns an instance of the Mesh class containing the mesh data.
# This class from: http://prideout.net/blog/?p=44
# Courtesy of Philip Rideout

class Polyhedra(object):
    
    @staticmethod
    def icosahedron():
        """Construct a 20-sided polyhedron"""
        faces = [ \
            (0,1,2),
            (0,2,3),
            (0,3,4),
            (0,4,5),
            (0,5,1),
            (11,6,7),
            (11,7,8),
            (11,8,9),
            (11,9,10),
            (11,10,6),
            (1,2,6),
            (2,3,7),
            (3,4,8),
            (4,5,9),
            (5,1,10),
            (6,7,2),
            (7,8,3),
            (8,9,4),
            (9,10,5),
            (10,6,1) ]
        verts = [ \
            ( 0.000,  0.000,  1.000 ),
            ( 0.894,  0.000,  0.447 ),
            ( 0.276,  0.851,  0.447 ),
            (-0.724,  0.526,  0.447 ),
            (-0.724, -0.526,  0.447 ),
            ( 0.276, -0.851,  0.447 ),
            ( 0.724,  0.526, -0.447 ),
            (-0.276,  0.851, -0.447 ),
            (-0.894,  0.000, -0.447 ),
            (-0.276, -0.851, -0.447 ),
            ( 0.724, -0.526, -0.447 ),
            ( 0.000,  0.000, -1.000 ) ]
        return verts, faces

    @staticmethod
    def octohedron(size=2.0):
        """Construct an eight-sided polyhedron"""
        f = sqrt(size) / size
        verts = [ \
            ( 0, -1,  0),
            (-f,  0,  f),
            ( f,  0,  f),
            ( f,  0, -f),
            (-f,  0, -f),
            ( 0,  1,  0) ]
        faces = [ \
            (0, 2, 1),
            (0, 3, 2),
            (0, 4, 3),
            (0, 1, 4),
            (5, 1, 2),
            (5, 2, 3),
            (5, 3, 4),
            (5, 4, 1) ]
        return verts, faces
    
    @staticmethod
    def plane(size=1.0):
        verts = [ \
                 ( size, 0, size),
                 ( size, 0,-size),
                 (-size, 0,-size),
                 (-size, 0, size)
                ]
        faces = [ \
                 (0, 1, 3),
                 (3, 2, 1)
#                 (2, 1, 0),
#                 (0, 3, 2)
                ]
        tex_coords = [ \
                      [1.0,1.0],
                      [1.0,0.0],
                      [0.0,0.0],
                      [0.0,1.0]
                     ]
        
        return verts, faces, tex_coords
    
    @staticmethod
    def cube(size=1.0):
        e2 = size / 2
        verts = list(itertools.product(*repeat([-e2, +e2], 3)))
        faces = [
            [0, 1, 3, 2], # left
            [4, 6, 7, 5], # right
            [7, 3, 1, 5], # front
            [0, 2, 6, 4], # back
            [3, 7, 6, 2], # top
            [1, 0, 4, 5], # bottom
        ]
        return verts, faces
    
    @staticmethod
    def subdivide(verts, faces):
        """Subdivide each triangle into four triangles, pushing verts to the unit sphere"""
        triangles = len(faces)
        for faceIndex in xrange(triangles):
        
            # Create three new verts at the midpoints of each edge:
            face = faces[faceIndex]
            a,b,c = (Vector3(*verts[vertIndex]) for vertIndex in face)
            verts.append((a + b).normalized()[:])
            verts.append((b + c).normalized()[:])
            verts.append((a + c).normalized()[:])
    
            # Split the current triangle into four smaller triangles:
            i = len(verts) - 3
            j, k = i+1, i+2
            faces.append((i, j, k))
            faces.append((face[0], i, k))
            faces.append((i, face[1], j))
            faces[faceIndex] = (k, j, face[2])
    
        return verts, faces
        
class Parametric:
    
    @staticmethod
    def sphere(slices, stacks):
        verts, faces = Parametric.surface(slices, stacks, Parametric.spherefunc)
        return verts, faces
    
    @staticmethod
    def plane(columns, rows):
        verts, faces, tex_coords = Parametric.plane_surface(columns, rows, Parametric.planefunc)
        return verts, faces, tex_coords
    
    @staticmethod
    def spherefunc(u, v):
        x = sin(u) * cos(v)
        y = cos(u)
        z = -sin(u) * sin(v)
        return x, y, z
    
    @staticmethod
    def planefunc(u, v):
        x = -0.5 + u
        y = 0
        z = -0.5 + v
        return x, y, z
    
    @staticmethod
    def plane_surface(columns, rows, func):
        verts = []
        for i in xrange(columns + 1):
            c = i * (1.0 / columns)
            for j in xrange(rows + 1):
                r = j * ( 1.0 / rows )
                p = func(c, r)
                verts.append(p)
        faces = []
        v = 0
        for c in xrange(columns):
            for r in xrange(rows):
                bl = v + c + r
                tl = bl + 1
                tr = tl + rows + 1
                br = tr - 1
                faces.append((bl, tl, tr))
                faces.append((bl, tr, br))
            v = v + rows
        
        tex_coords = []
        for i in xrange(columns + 1):
            c = i * (1.0 / columns)
            for j in xrange(rows + 1):
                r = j * ( 1.0 / rows )
                y = j/rows
                p = [c,r] 
                tex_coords.append(p)
            
        return verts, faces, tex_coords
    
    @staticmethod
    def surface(slices, stacks, func):
        verts = []
        for i in xrange(slices + 1):
            theta = i * pi / slices
            for j in xrange(stacks):
                phi = j * 2.0 * pi / stacks
                p = func(theta, phi)
                verts.append(p)
    
        faces = []
        v = 0
        for i in xrange(slices):
            for j in xrange(stacks):
                next = (j + 1) % stacks
#                faces.append((v + j, v + next, v + j + stacks))
#                faces.append((v + next, v + next + stacks, v + j + stacks))
                faces.append((v + j + stacks, v + next,  v + j))
                faces.append((v + j + stacks, v + next + stacks, v + next))
            v = v + stacks
    
        return verts, faces
        
class MeshTypes:
    PLANE = 0
    OCTOHEDRON = 1 
    ICOHEDRON = 2
    SPHERE = 3
    CUBE = 4
    PLANE_HI = 5

class MeshFactory(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def GetMesh(type):
        if type == MeshTypes.PLANE:
            verts, faces, tex_cs = Polyhedra.plane()
            return Mesh(verts, faces, Preset.yellow, tex_coords=tex_cs)
        elif type == MeshTypes.OCTOHEDRON:
            verts, faces = Polyhedra.octohedron()
        elif type == MeshTypes.ICOHEDRON:
            verts, faces = Polyhedra.icosahedron()
        elif type == MeshTypes.CUBE:
            verts, faces = Polyhedra.cube()
        elif type == MeshTypes.SPHERE:
            verts, faces = Parametric.sphere(16,16)
        elif type == MeshTypes.PLANE_HI:
            verts, faces, tex_cs = Parametric.plane(16,16)
            return Mesh(verts, faces, Preset.yellow, tex_coords=tex_cs)
        
        return Mesh(verts, faces, Preset.yellow)
    
    