import math

from OpenGL.GL import *
from OpenGL.GLU import *
matrix_type = GLfloat * 16
matrix_typed = GLdouble * 16

from epsilon.scene.node import Node
from epsilon.render.material import GLMaterial

from epsilon.render.colour import Preset

from epsilon.environment.planet.cubespheremap import CubeSphereMap
from epsilon.environment.planet.spheresurface import SphereSurface

from epsilon.render.material import GLMaterial
from epsilon.render.renderer import Renderer

class QuadName:
    TL = 0
    TR = 1
    BR = 2
    BL = 3
    @staticmethod
    def quad_string(quad):
        if quad == QuadName.TL:
            return "TL"
        elif quad == QuadName.TR:
            return "TR"
        elif quad == QuadName.BR:
            return "BR"
        elif quad == QuadName.BL:
            return "BL"
        
class SphereQuadRenderer(Renderer):
    def __init__(self,mesh=None, material=None):
        Renderer.__init__(self, mesh, material)
        
    def _setup_draw(self):
        glPushMatrix()
            
        # Translate    
        glTranslate(*self.node_parent.transform.position)
        
        # Rotate
        glMultMatrixf(matrix_type(*self.node_parent.transform.rotation.get_matrix()))
        
        # ignore scale when rendering children
        

class SphereQuad(Node):
    SPLIT_DISTANCE = 1.5 # Size Multiplier
    MAX_DEPTH = 2
    
    def __init__(self, sphere_parent,
                       planet_root, 
#                       split_distance=1.0, 
                       radius=1.0,
                       root=True, 
                       level=-1,
                       density=10,
                       face=CubeSphereMap.TOP,
                       quad=QuadName.TL):
        
        # Override the default renderer
        Node.__init__(self, renderer=SphereQuadRenderer())
        
        self._sphere_parent = sphere_parent
        
        # Planet Root - for global controls
        self._planet_root = planet_root
        
        self._face = face
        self._quad = quad
        #self.local_scale = Vector3(size, size, size)
        
        self._root = root
        
        self._is_split = False
        self._level = level
        
        # The Mesh density
        self._density = density
        
        self._radius = radius
#        self._split_dist = split_distance * self.SPLIT_DISTANCE 
        
        self._corners = None
        self._quad_centres = None
        
        self._centre_coords = None
        
        self._sorted_quads = None
        
        
        #self._mesh = MeshFactory.get_mesh(MeshTypes.PLANE_HI)
        
        self._material = GLMaterial()
        if quad == QuadName.TL:
            self._material.diffuse = Preset.blue
        elif quad == QuadName.TR:
            self._material.diffuse = Preset.green
        elif quad == QuadName.BR:
            self._material.diffuse = Preset.yellow
        elif quad == QuadName.BL:
            self._material.diffuse = Preset.purple
        
#        # FIXME: This is a hack and needs to be fixed by a proper Bounds implementation
#        self._size = split_distance
#        
#        # Determine Bounds
#        h_size = self._size / 2.0
#        top = Vector3(h_size, h_size, h_size)
#        bottom = Vector3(-h_size, -h_size, -h_size)
#        self._bounds = Bounds(top, bottom)
        
    @property
    def face(self):
        return self._face

    @property
    def corners(self):
        return self._corners
    
    def _init_quad(self):
        self._calc_corners()
        
        # build the mesh for the quad
#        bound_min_x= (self._corners[0] * 2.0) - 1.0 
#        bound_max_x= (self._corners[2] * 2.0) - 1.0 
#        bound_min_z= (self._corners[1] * 2.0) - 1.0
#        bound_max_z= (self._corners[3] * 2.0) - 1.0
        bound_min_x= self._corners[0] 
        bound_max_x= self._corners[2] 
        bound_min_z= self._corners[1]
        bound_max_z= self._corners[3]
#        print "Generating Quad: %s with bounds: minx: %3.2f maxx: %3.2f minz: %3.2f maxz: %3.2f" % (QuadName.quad_string(self._quad),
#                                                                                                    bound_min_x,
#                                                                                                    bound_max_x,
#                                                                                                    bound_min_z,
#                                                                                                    bound_max_z,)
        self._surface = SphereSurface(bound_min_x=bound_min_x,
                                      bound_max_x=bound_max_x,
                                      bound_min_z=bound_min_z,
                                      bound_max_z=bound_max_z,
                                      increments=self._density,
                                      radius=self._radius,
                                      face=self._face)
        
        self.renderer.mesh = self._surface.mesh
        
        
    def _calc_corners(self):
        # Calculate the Cubic coordinates of this quad
        self._corners = []
        
        if self._root:
            self._corners.append(0.0) #tl x
            self._corners.append(0.0) #tl y
            self._corners.append(1.0) #br x
            self._corners.append(1.0) #br y
        else:
            parent_corners = self.transform.parent.node.corners
            
            if self._quad == QuadName.TL:
                self._corners.append(parent_corners[0])
                self._corners.append(parent_corners[1])
                self._corners.append(parent_corners[0] + (parent_corners[2] - parent_corners[0]) * 0.5 )
                self._corners.append(parent_corners[1] + (parent_corners[3] - parent_corners[1]) * 0.5 )
                
            elif self._quad == QuadName.TR:
                self._corners.append(parent_corners[0] + (parent_corners[2] - parent_corners[0]) * 0.5)
                self._corners.append(parent_corners[1])
                self._corners.append(parent_corners[2])
                self._corners.append(parent_corners[1] + (parent_corners[3] - parent_corners[1]) * 0.5 )
                
            elif self._quad == QuadName.BL:
                self._corners.append(parent_corners[0])
                self._corners.append(parent_corners[1] + (parent_corners[3] - parent_corners[1]) * 0.5)
                self._corners.append(parent_corners[0] + (parent_corners[2] - parent_corners[0]) * 0.5)
                self._corners.append(parent_corners[3])
                
            
            elif self._quad == QuadName.BR:
                self._corners.append(parent_corners[0] + (parent_corners[2] - parent_corners[0]) * 0.5)
                self._corners.append(parent_corners[1] + (parent_corners[3] - parent_corners[1]) * 0.5)
                self._corners.append(parent_corners[2])
                self._corners.append(parent_corners[3])
                
                
        mid_x = (self._corners[2] - self._corners[0]) / 2
        mid_y = (self._corners[3] - self._corners[1]) / 2
        
        self._centre_coords = [(self._corners[0] + mid_x), (self._corners[1] + mid_y)]
        
        self._quad_centres = [ [self._corners[0] + (mid_x/2), self._corners[1] + (mid_y/2)], #TL
                               [self._corners[2] - (mid_x/2), self._corners[1] + (mid_y/2)], #TR
                               [self._corners[2] - (mid_x/2), self._corners[3] - (mid_y/2)], #BR
                               [self._corners[0] + (mid_x/2), self._corners[3] - (mid_y/2)]  #BL
                             ]
        
    def _get_centre_position(self):
        return CubeSphereMap.get_sphere_position(self._centre_coords[0], 
                                                 self._centre_coords[1], 
                                                 self._face,
                                                 self._sphere_parent.radius)

    def update_surface(self):
        
        pos = self._sphere_parent.camera.node_parent.transform.position
        
        # Get world positions for centres of child quads
        child_pos = [CubeSphereMap.get_sphere_position(self._quad_centres[QuadName.TL][0],
                                                       self._quad_centres[QuadName.TL][1],
                                                       self._face,
                                                       self._sphere_parent.radius),
                     CubeSphereMap.get_sphere_position(self._quad_centres[QuadName.TR][0],
                                                       self._quad_centres[QuadName.TR][1],
                                                       self._face,
                                                       self._sphere_parent.radius),
                     CubeSphereMap.get_sphere_position(self._quad_centres[QuadName.BR][0],
                                                       self._quad_centres[QuadName.BR][1],
                                                       self._face,
                                                       self._sphere_parent.radius),
                     CubeSphereMap.get_sphere_position(self._quad_centres[QuadName.BL][0],
                                                       self._quad_centres[QuadName.BL][1],
                                                       self._face,
                                                       self._sphere_parent.radius),
                     ]
        
        # Get the distances of the camera from the quads
        distances = [pos.distance(child_pos[QuadName.TL]),
                     pos.distance(child_pos[QuadName.TR]),
                     pos.distance(child_pos[QuadName.BR]),
                     pos.distance(child_pos[QuadName.BL]),
                    ]
        
        # Sort the quads by distance from the camera for updating and rendering.
        # Not using actual distances to avoid precision errors
        coord = CubeSphereMap.get_cube_coord(*pos)
        self._sorted_quads = []
        
        if coord.x < self._centre_coords[0]:
            # In top left
            if coord.y < self._centre_coords[1]:
                #print "TL"
                self._sorted_quads.append(0)
                self._sorted_quads.append(1)
                self._sorted_quads.append(2)
                self._sorted_quads.append(3)
            
            # In bottom left
            else:
                #print "BL"
                self._sorted_quads.append(2)
                self._sorted_quads.append(0)
                self._sorted_quads.append(3)
                self._sorted_quads.append(1)
                
#                self._sorted_quads.append(2)
#                self._sorted_quads.append(0)
#                self._sorted_quads.append(3)
#                self._sorted_quads.append(1)
        else:
            # In top right
            if coord.y < self._centre_coords[1]:
                #print "TR"
                self._sorted_quads.append(1)
                self._sorted_quads.append(0)
                self._sorted_quads.append(3)
                self._sorted_quads.append(2)
            
            # In bottom right
            else:
                #print "BR"
                self._sorted_quads.append(2)
                self._sorted_quads.append(3)
                self._sorted_quads.append(0)
                self._sorted_quads.append(1)
        
        # Calculate the quadrant size using the length of the diagonal across the quadrant
        #TODO: Maybe this is used to adjust the frustrum on the fly when the camera gets close to the planet??
        quad_size = child_pos[QuadName.TL] - child_pos[QuadName.BR] * 1.0 #( radius / frustrum radius)....
        
        radius = self._sphere_parent.radius
        
        # Calculate split priority
        # Adjust the quadrant size because the quadrants become distorted near the corners of the cube
        # resulting in incorrect splitting/merging of quads.
        quad_size = (self._corners[2] - self._corners[0]) * radius
        priority = 0.0
        if quad_size > (self._sphere_parent.max_height * 0.001):
            priority = self._sphere_parent.split_factor * math.pow(quad_size, self._sphere_parent.split_power )
            
        for quad_inc in self._sorted_quads:
            
            # Check to see if the camera is within this quadrant
            if not self.hit_test(self._sphere_parent.camera_pos_sc, quad_inc):
                if len(self.transform.children) > quad_inc:
                    # Check the quadrant against the horizon distance
                    if self._sphere_parent.horizon > 0.0 and distances[quad_inc] - radius > self._sphere_parent.horizon:
                        self.transform.children[quad_inc].node._merge()
                        print "Horizon"
                        continue
                    
                    # Check the quadrant against the view frustrum
                    if not self._sphere_parent.camera.sphere_inside(self.transform.children[quad_inc].position, radius):
                        self.transform.children[quad_inc].node._merge()
                        #print "Culling"
                        continue
            
            if distances[quad_inc] > priority:
                if len(self.transform.children) > quad_inc:
                    self.transform.children[quad_inc].node._merge()
                    #print "Distance"
                    continue
            
            self._split(quad_inc)
            
            if self._is_split:
                if len(self.transform.children) > quad_inc:
                    if self.transform.children[quad_inc]:
                        self.transform.children[quad_inc].node.update_surface()
            
        
#    def update_surface_old(self):
#        
#        pos = self._sphere_parent.camera_pos
#        
#        # If this level can be split otherwise, ignore
#        if self._level < self.MAX_DEPTH:
#            
#            # Build the corner coordinates if necessary
#            if self._corners is None:
#                self._calc_corners()
#            
#            distance = pos - self.position
#            
#            if distance.magnitude() < self._split_dist:
#                if not self._is_split:
#                    # split
#                    self._split()
#                    
#                # else already split - hide this level and check if children
#                else:
#                    for child in self._children:
#                        child.update_surface()
#                     
#                #self._material.diffuse = Preset.green
#            else:
#                if self._is_split:
#                    self._is_split = False
#                
#                #self._material.diffuse = Preset.blue
#                # else not split - don't do anything
    
    def _can_merge(self):
        
        # If this node has children
        if self._is_split:
            return False
        
        #TODO: Add check to prevent this node from being merged if it is bordering a leaf node
        #      at the same level
        
        return True
       
    def _merge(self):
        #if self._is_split:
        
        #    child_quad = self.children[quadrant]
        children_merged = True
        
        if self._is_split:
#            print "merging"
#            if not self.children[QuadName.TL]._merge():
#                children_merged = False
#            if not self.children[QuadName.TR]._merge():
#                children_merged = False
#            if not self.children[QuadName.BR]._merge():
#                children_merged = False
#            if not self.children[QuadName.BL]._merge():
#                children_merged = False
#                
#            if not children_merged or not self._can_merge():
#                return False
            self.transform.remove_children()
#            for i in range(len(self.children)-1, 0, -1):
#            # child in self.children:
#                child = self.children[i]
#                self.remove_child(child)
            #self.children[quadrant].visible = False
            self._is_split = False
        return True
        
        #return False
            
    # Quadrant is currently unused.
    def _split(self, quadrant=-1):
        
        if not self._is_split:
            if not self._planet_root.can_split():
#                print "Ignoring split until next frame"
                return
            
#            print "splitting"
            h_size = 1.0#self._size / 2.0
            #p_size = self._size / 4.0
            next_level = self._level + 1
            
#            print "Splitting level: %d" % self._level
#            print "Quadrant: %s" % QuadName.quad_string(quadrant)
            # build top left
            #coord = Vector3(-p_size, 0, p_size)
            new_quad = SphereQuad(self._sphere_parent, self._planet_root, radius=self._radius, root=False, level=next_level, density=self._density, face=self._face, quad=QuadName.TL )
            self.transform.add_child( new_quad.transform )
            new_quad._init_quad()
            
            # top right
            #coord = Vector3(p_size, 0, p_size)
            new_quad = SphereQuad(self._sphere_parent, self._planet_root, radius=self._radius, root=False, level=next_level, density=self._density, face=self._face, quad=QuadName.TR )
            self.transform.add_child( new_quad.transform )
            new_quad._init_quad()
            
            # bottom left
            #coord = Vector3(-p_size, 0, -p_size )
            new_quad = SphereQuad(self._sphere_parent, self._planet_root, radius=self._radius, root=False, level=next_level, density=self._density, face=self._face, quad=QuadName.BL )
            self.transform.add_child( new_quad.transform )
            new_quad._init_quad()
            
            # bottom right
            #coord = Vector3(p_size, 0, -p_size )
            new_quad = SphereQuad(self._sphere_parent, self._planet_root, radius=self._radius, root=False, level=next_level, density=self._density, face=self._face, quad=QuadName.BR )
            self.transform.add_child( new_quad.transform )
            new_quad._init_quad()
            
            self._is_split = True
    
    def hit_test(self, coord, quad=-1):
        if coord.face == self.face:
            if not quad == -1:
                mid_x = ((self._corners[0] + self._corners[2]) / 2)
                mid_y = ((self._corners[1] + self._corners[3]) / 2)
                
                if quad == QuadName.TL:
                    return (coord.x >= self._corners[0] and coord.x <= mid_x and \
                            coord.y >= self._corners[1] and coord.y <= mid_y )
                elif quad == QuadName.TR:
                    return (coord.x >= mid_x and coord.x <= self._corners[2] and \
                            coord.y >= self._corners[1] and coord.y <= mid_y )
                elif quad == QuadName.BR:
                    return (coord.x >= self._corners[0] and coord.x <= mid_x and \
                            coord.y >= mid_y and coord.y <= self._corners[3])
                elif quad == QuadName.BL:
                    return (coord.x >= mid_x and coord.x <= self._corners[2] and \
                            coord.y >= mid_y and coord.y <= self._corners[3])
                else:
                    return False
                    
            else:
                return ( coord.x >= self._corner[0] and coord.x <= self._corner[2] and \
                         coord.y >= self._corner[1] and coord.y <= self._corner[3] )
        else:
            return False
    
    def draw(self):
        # If split then draw children
        if self._is_split and not self.transform.children == []:
            
            if not len(self.transform.children) == 4:
                print "missing children"
            
            # Draw sorted children
            for quad_inc in self._sorted_quads:
                self.transform.children[quad_inc].node.draw()
            
        # If not split then draw self and don't draw children
        else:
            self.renderer.draw()
            
    