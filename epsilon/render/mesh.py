'''
Created on Sep 17, 2011

These classes define a Mesh object and a GLMesh object for use with the GLRenderer.
The majority of the code has been taken directly from:
http://code.google.com/p/flyinghigh-opengl-from-python
Thanks to Jonathan Hartley.

@author: scottporter
'''

from datetime import datetime

from itertools import chain, repeat, izip
import math
using_pypy = False
import sys
if '__pypy__' in sys.builtin_module_names:
    using_pypy = False

if using_pypy:
    import array
else:
    import numpy

from OpenGL.GL import *
# Vertex Buffer Setup
from OpenGL.raw import GL
from OpenGL.arrays import ArrayDatatype as ADT
from OpenGL.arrays import vbo

from epsilon.logging.logger import Logger
from epsilon.geometry.euclid import Vector3
from epsilon.render.bounds import Bounds
from epsilon.render.colour import Colour, Preset
from epsilon.render.glutilities import *

from epsilon.resource.resourcebase import ResourceBase, ResourceType

#from epsilon.render.mesh_utilities import MeshUtilities as MU
#from epsilon.render.mesh_utilities import _gen_normals

from epsilon.utilities.timer import Timer

class TextureMappingConstants:
    PLANAR = 1
    CUBIC = 2
    SPHERICAL = 3
    CYLINDRICAL = 4

class OpenGLConstants:
    vertex_components = 3
    color_components  = 4
    normal_components = 3
    
    type_to_enum = {
        GLubyte: GL_UNSIGNED_BYTE,
        GLushort: GL_UNSIGNED_SHORT,
        GLuint: GL_UNSIGNED_INT,
    }

# This Class is a general mesh container that holds the shape data for
# a Mesh.
class Mesh(ResourceBase):
    
    def __init__(self, vertices, faces, face_colours=None, tex_coords=None, filename=""):
        ResourceBase.__init__(self, filename=filename)
        self._type = ResourceType.MESH
        
        # Create Vertices
        # If they are not already in Vector3 format create the necessary 
        # Vector3 objects
        if len(vertices) > 0 and not isinstance(vertices[0], Vector3):
            vertices = [Vector3(*v) for v in vertices]
        self._vertices = vertices
        
        # Currently only Triangles are supported
        for face in faces:
            # Check if the faces reference more than 3 vertices
            assert len(face) >= 3
            
            # Check that each vertex referenced in the face
            # is valid
            for index in face:
                assert 0 <= index < len(vertices)
        
        self._faces = faces
        
        if face_colours is None:
            face_colours = Preset.white 
        # If a single Colour has been specified for all of the faces,
        # replicate it for all of the faces in the Mesh
        if isinstance(face_colours, Colour):
            face_colours = list(repeat(face_colours, len(self.faces)) )
                        
        self._face_colours = face_colours
        
        # If tex coords haven't been specified give the mesh a bunch of
        # zero'd texture coordinates
        if tex_coords is None:
            tex_coords = []
#            tex_coords = list(repeat(Vector3(), len(self._vertices)))
        
        self._tex_coords = tex_coords
        
        # calculate the min and max vertices for bounds
        min = Vector3()
        max = Vector3()
        
        for vec in self._vertices:
            if min.x > vec.x:
                min.x = vec.x
            if min.y > vec.y:
                min.y = vec.y
            if min.z > vec.z:
                min.z = vec.z
                
            if max.x < vec.x:
                max.x = vec.x
            if max.y < vec.y:
                max.y = vec.y
            if max.z < vec.z:
                max.z = vec.z
        
        self._bounds = Bounds(min, max)
            
        # Create a Open GL Mesh Object
        self._glmesh = GLMesh(self)
        
    @property 
    def vertices(self):
        return self._vertices
    
    @property
    def faces(self):
        return self._faces
    
    @property
    def face_colours(self):
        return self._face_colours
    
    @property
    def glmesh(self):
        return self._glmesh;
    
    @property
    def tex_coords(self):
        return self._tex_coords
    
    @property
    def bounds(self):
        return self._bounds
    
    
# This class converts the data held by the Mesh class into a format that
# can be processed using OpenGL
class GLMesh(object):
    
    def __init__(self, mesh=None):
        
        if not Mesh is None and isinstance(mesh, Mesh):
            vertices = list(mesh.vertices)
            faces = list(mesh.faces)
            tex_coords = list(mesh.tex_coords)
            
            self._vertex_buffer = VertexBuffer()
            
            self._vertices = None
            self._indices = None
            self._colours = None
            self._normals = None
            self._tex_coords = None
            
            self._get_glvertices(vertices, faces)
            self._get_glindices(faces)
            self._get_glcolours(faces, mesh.face_colours)
            self._get_glnormals(vertices, faces)
            self._v_len = len(self._vertices)
            self._gen_texture_coords(tex_coords)
            
            # Configure Vertex Buffer object
            self._vertex_buffer.setup(self._vertices, self._indices, self._normals, self._colours, self._tex_coords)
            
        else:
            self._num_glvertices = None
            self._glvertices = None
            self._glindex_type = None
            self._glindices = None
            self._glcolours = None
            self._glnormals = None
            
    @property
    def vertex_buffer(self):
        return self._vertex_buffer
            
    @property
    def glvertices(self):
        return self._glvertices
    
    @property
    def glindex_type(self):
        return self._glindex_type
    
    @property
    def glindices(self):
        return self._glindices
    
    @property
    def glcolours(self):
        return self._glcolours
    
    @property
    def glnormals(self):
        return self._glnormals
    
    # Get the number of vertices    
    def _get_num_glvertices(self, faces):
        return len(list(chain(*faces)))
    
    # Create a list of GLfloat vertices
    def _get_glvertices(self, vertices, faces):
                
        self._vertices = []
        self._vert_index = []
        
        for face in faces:
            for index in face:
                self._vertices.append(vertices[index])
                self._vert_index.append(index)
        
        glverts = chain.from_iterable(
                                      vertices[index]
                                      for face in faces
                                      for index in face                                      
                                     )
        
        self._num_glvertices = self._get_num_glvertices(faces)
        # return CreateGLArray(GLfloat, glverts, (self._num_glvertices * OpenGLConstants.vertex_components) )
    
    def _get_glindex_type(self):
        # The type of glindices depends on how many vertices there are
        
        # NOTE: I'm not too sure about this calculation.  self.num_vertices appears to
        #       hold the number of FACES in the mesh rather than the number of vertices.
        #       This needs to be tested out.  -- Hmmm it looks like this code supports faces
        #       with more than 3 vertices.
        if self._num_glvertices < 256:
            index_type = GLubyte
        elif self._num_glvertices < 65536:
            index_type = GLushort
        else:
            index_type = GLuint
        return index_type
    
    # Create the GL Indices
    def _get_glindices(self, faces):
        glindices = []
        
        face_offset = 0
        for face in faces:
            indices = xrange(face_offset, face_offset + len(face))
            glindices.extend(chain(*MeshUtilities.tesselate_face(indices)))
            face_offset += len(face)
        self._indices = glindices
        self._glindex_type = self._get_glindex_type()
        # return CreateGLArray(self._glindex_type, glindices, len(glindices))
    
    def _get_glcolours(self, faces, face_colours):
        
        self._colours = []
        for face, colour in izip(faces, face_colours):
            for i in range(len(face)):
                self._colours.append(colour)
        
        glcolours = chain.from_iterable( 
                                        repeat(colour, len(face))
                                        for face, colour in izip(faces, face_colours)                                        
                                       )
        
        #return CreateGLArray(GLubyte, chain(*glcolours), (self._num_glvertices * OpenGLConstants.color_components) )
    
    def _get_glnormals(self, vertices, faces):
        self._normals = []

        normals = list( MeshUtilities.face_normal(vertices, face) for face in faces )

        # Calculate the normals once for each unique vertex and after calcs done, 
        # rebuild the vertex list
        vertex_normals = []
        
        # for each vertex
        for v_inc in range(len(vertices)):
            face_normals = []
            vert_norm = Vector3()
            
            # for each face
            for f_inc in range(len(faces)):
                
                # if the face contains the current vertex
                if v_inc in faces[f_inc]:
                    # and the faces normal isn't already stored i.e. ignore co-planar face normals
                    if normals[f_inc] not in face_normals:
                        # Store it
                        face_normals.append(normals[f_inc])
            
            # Calculate the average for all of the face normals found
         
            for f_norm in face_normals:
                vert_norm += f_norm
            vert_norm.normalize()
            
            vertex_normals.append(vert_norm)
        
        for vi in range(len(self._vert_index)):
            v_ind = self._vert_index[vi]
            self._normals.append(vertex_normals[v_ind])
        
    def _gen_texture_coords(self, tex_coords=None, mapping_type=TextureMappingConstants.SPHERICAL):
        
        if len(tex_coords) == 0 :
            tex_coords = []
            fast = False
            
            if mapping_type == TextureMappingConstants.SPHERICAL:
                
                if fast:
                    for norm in self._normals:
                        u = norm.x / 2 + 0.5
                        v = norm.z / 2 + 0.5
                        tex_coords.append([u,v])
                else:
                    for norm in self._normals:
                        u = math.asin(norm.x)/math.pi + 0.5
                        v = math.asin(norm.z)/math.pi + 0.5
                        tex_coords.append([u,v])
        
        else:
            # Expand the texture coordinates array to match the format of the transformed vertex array
            new_tex_coords = []
            
            for vi in range(len(self._vert_index)):
                
                v_ind = self._vert_index[vi]
                new_tex_coords.append(tex_coords[v_ind])
            
            tex_coords = new_tex_coords
                    
        self._tex_coords = tex_coords
        
class MeshUtilities:
    
    @staticmethod
    def face_normal(vertices, face):
        # Return the unit normal vector of the face
        # The direction of the normal will be reversed if
        # the faces winding is reversed.
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[2]]
        a = v0 - v1
        b = v2 - v1
        normal = b.cross(a).normalize()
        return normal
    
    '''
    Return the given face broken into a list of triangles, wound in the
    same direction as the original poly. Does not work for concave faces.
    e.g. [0, 1, 2, 3, 4] -> [[0, 1, 2], [0, 2, 3], [0, 3, 4]]
    '''
    @staticmethod
    def tesselate_face(face):
        return ( [face[0], face[index], face[index + 1]]
                 for index in xrange(1, len(face) - 1)
               )

# This class receives a collection of vertex data, formats it into a VertexBufferObject
# and allows easy use of the VBO
class VertexBuffer(object):
    
    FLOAT_WIDTH = 4 # bytes
    
    def __init__(self):
        self._vbo = None
        self._num_vertices = 0
        self._indices_vbo = None
        self._has_normals = False
        self._has_colours = False
        self._has_tex_coords = False
        self._num_tex_coords = 0
        
        # offsets
        self._normal_offset = 0
        self._colour_offset = 0
        self._tex_coord_offset = 0
        
        self._stride = 0
        self._is_setup = False
        
    def __del__(self):
        if not self._vbo is None:
            self._vbo.delete()
        
    def __enter__(self):
        self.bind()
        return self
        
    def __exit__(self, type, value, traceback):
        self.unbind()
        
    def setup(self, vertices,
                    indices,
                    normals = None,
                    colours = None,
                    texture_coords = None,
                    num_texture_coords = 0):
        
        self._num_vertices = len(vertices)
        
        if self._num_vertices == 0:
            Logger.Log("VertexBuffer ERROR: empty vertices")
            return
        
        # Add code to handle varying length lists of colour values.
        
        has_normals = (not normals is None and isinstance(normals, list))
        has_colours = (not colours is None and isinstance(colours, list))
        
        has_tex_coords = (not texture_coords is None and isinstance(texture_coords, list))
        
        has_colours = False
#        has_tex_coords = False
        
        if has_tex_coords and len(texture_coords) > 0:
            # If the first element of the first list in the list is a float
            if isinstance(texture_coords[0][0], float):
                # Then there is only a single set of texture coordinates
                num_texture_coords = 1
            # otherwise assume that it's a list, and count the number of lists to get the
            # number of texture coordinates
            else:
                num_texture_coords = len(texture_coords[0][0])
            
        # If the input data has enough data for each of the vertices
        #if len(normals) == len(vertices):
        buffer = []
        
        for i in range(0, len(vertices)):
            vert_data = []
            with vertices[i] as v:
                vert_data.append([v.x,v.y,v.z])
            if has_normals:
                with normals[i] as n:
                    vert_data.append([n.x,n.y,n.z])
            if has_colours:
                r, g, b, a = colours[i].GetFloatColour()
                vert_data.append([r, g, b, a])
            if has_tex_coords:
                if num_texture_coords > 1:
                    for t in range(0, num_texture_coords):
                        tc = texture_coords[i][t]
                        vert_data.append([tc[0],tc[1]])
                else:
                    vert_data.append(texture_coords[i])
            buffer.append(list(chain(*vert_data)))
        if using_pypy:
            try:
                buf_array = array.array('f', list(chain(*buffer)))
            except Exception, e:
                print buffer
                raise e
            
            self._vbo = vbo.VBO(buf_array)
        else:
            self._vbo = vbo.VBO(numpy.array(buffer, 'f'))
        
        self._has_colours = has_colours
        self._has_normals = has_normals
        self._has_tex_coords = has_tex_coords
        self._num_tex_coords = num_texture_coords
        
        
        self._stride = 3 * self.FLOAT_WIDTH
        if self._has_normals:
            self._normal_offset = self._stride
            self._stride += 3 * self.FLOAT_WIDTH
        if self._has_colours:
            self._colour_offset = self._stride
            self._stride += 4 * self.FLOAT_WIDTH
        if self._has_tex_coords:
            self._tex_coord_offset = self._stride
            self._stride += (2 * self.FLOAT_WIDTH) * num_texture_coords
            
        if using_pypy:
            ind_array = array('H')
            ind_array.fromlist(indices)
            self._indices_vbo = vbo.VBO(ind_array,target="GL_ELEMENT_ARRAY_BUFFER")
        else:
            self._indices_vbo = vbo.VBO(numpy.array(indices,dtype=numpy.ushort),target="GL_ELEMENT_ARRAY_BUFFER")
        self._is_setup = True    
        # else:
        #     Logger.Log("Vertex Buffer ERROR: vertex and normal data list lengths don't match. Len normals: %d: Len verts: %d" % (len(normals), len(vertices)))
        

    @property
    def is_setup(self):
        return self._is_setup
    
    @property
    def count(self):
        return self._num_vertices
    
    @property 
    def indices(self):
        return self._indices_vbo
    
    # Handles Binding and setting appropriate OpenGL Settings
    def bind(self):
        if not self._vbo is None and not self._indices_vbo is None: 
            self._vbo.bind()
            self._indices_vbo.bind()       
        
    def GetVertexAttribute(self):
        return 3, GL_FLOAT, False, self._stride, self._vbo
    
    def GetNormalAttribute(self):
        return 3, GL_FLOAT, False, self._stride, (self._vbo+self._normal_offset)
    
    def GetColourAttribute(self):
        return 4, GL_FLOAT, False, self._stride, self._vbo+self._colour_offset
    
    # For single texture coordinates only
    def GetTexCoordAttribute(self):
        return 2, GL_FLOAT, False, self._stride, self._vbo+self._tex_coord_offset        
        
    def unbind(self):
        if not self._vbo is None and not self._indices_vbo is None: 
            self._vbo.unbind()
            self._indices_vbo.unbind()
    
    