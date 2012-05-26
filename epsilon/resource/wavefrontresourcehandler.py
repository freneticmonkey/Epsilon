'''
Created on Mar 4, 2012

@author: scottporter
'''
import string

from epsilon.resource.resourcebase import ResourceType, ResourceBase
from epsilon.resource.resourcehandler import ResourceHandlerBase

from epsilon.render.mesh import Mesh

from epsilon.logging import Logger

# small utility function
def isspace(character):
    return character in string.whitespace

class WavefrontResourceHandler(ResourceHandlerBase):
    def __init__(self):
        ResourceHandlerBase.__init__(self)
        self._resource_type = ResourceType.MESH
        self._filetypes = ["obj"]
        
    def process_resource(self, filename):
        new_mesh = None
        
        try:
            vertices, uvs, faces = self.read_mesh_file(filename)
            
            # If data was able to be read from the file
            if len(vertices) and len(faces):
                
                new_mesh = Mesh(vertices, faces, tex_coords=uvs, filename=filename )
            
        except Exception, e:
            Logger.Log("ERROR: Parsing Wavefront object file: " + e.message)
        
        # Return the new Resource
        return new_mesh
        
    def remove_resource(self, resource):
        pass
        
    def read_mesh_file(self, filename):
        vlist = []
        uvlist = []
        flist = []
        
        with open(filename,"r") as mesh_file:
            
            for line in mesh_file.readlines():
                # ignore comment or empty line
                if line[0] == "#" or line[0] == "\n":
                    pass
        
                # add vertex
                elif line[0] == "v" and isspace(line[1]):
                    co = line.split()
                    vlist.append((float(co[1]), float(co[2]), float(co[3])))
        
                # add uv coord
                elif line[0:2] == "vt" and isspace(line[2]):
                    uvco = line.split()
                    uvlist.append((float(uvco[1]), float(uvco[2])))
                
                # add face
                elif line[0] == "f" and isspace(line[1]):
                    fdata = line.split()
                    # remove the f character
                    del fdata[0]
                    
                    if len(fdata) >= 3:
                        f = []
                        for vert in fdata:
                            ids = vert.split("/")
                            
                            # .obj id's start at 1
                            v_id = int(ids[0]) - 1
                            
                            # Currently discard the per vertex uvs
#                            if len(ids) >= 2: 
#                                uv_id = int(ids[1]) - 1
#                            else: 
#                                uv_id = -1
#                            
#                            f.append((v_id, uv_id))
                            f.append(v_id)
            
                        flist.append(f)
                        
        # Process any quads into triangles because the renderer doesn't yet
        # support quads :(
        processed_faces = []
        for face in flist:
            if len(face) == 4:
                # Face 1
                processed_faces.append([face[0], face[1], face[3]])
                processed_faces.append([face[3], face[1], face[2]])
            else:
                processed_faces.append(face)
         
    
        return vlist, uvlist, processed_faces
        
        
        
        