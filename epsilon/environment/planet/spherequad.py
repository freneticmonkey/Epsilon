import math

from OpenGL.GL import *
from OpenGL.GLU import *
matrix_type = GLfloat * 16
matrix_typed = GLdouble * 16

from epsilon.logging.logger import Logger

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
    
    def __init__(self, name,
                       sphere_parent,
                       planet_root, 
                       split_distance=1.0, 
                       radius=1.0,
                       root=True, 
                       level=-1,
                       density=10,
                       face=CubeSphereMap.TOP,
                       quad=QuadName.TL):
        
        # Override the default renderer
        Node.__init__(self, renderer=SphereQuadRenderer())
        
        self._name = name

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
        
        # The Quads
        self._tl = None
        self._tr = None
        self._bl = None
        self._br = None
        
        
        #self._mesh = MeshFactory.get_mesh(MeshTypes.PLANE_HI)
        
        # self._material = GLMaterial()
        # if quad == QuadName.TL:
        #     self._material.diffuse = Preset.blue
        # elif quad == QuadName.TR:
        #     self._material.diffuse = Preset.green
        # elif quad == QuadName.BR:
        #     self._material.diffuse = Preset.yellow
        # elif quad == QuadName.BL:
        #     self._material.diffuse = Preset.purple

        
#        # FIXME: This is a hack and needs to be fixed by a proper Bounds implementation
#        self._size = split_distance
#        
#        # Determine Bounds
#        h_size = self._size / 2.0
#        top = Vector3(h_size, h_size, h_size)
#        bottom = Vector3(-h_size, -h_size, -h_size)
#        self._bounds = Bounds(top, bottom)
    @property
    def name(self):
        return self._name

    @property
    def face(self):
        return self._face

    @property
    def corners(self):
        return self._corners
    
    def _init_quad(self):
        self._calc_corners()
        
        #Logger.Log("Created Quad: name: %s" % ( self.name ) )
        
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
        # self._surface = SphereSurface(bound_min_x=bound_min_x,
        #                               bound_max_x=bound_max_x,
        #                               bound_min_z=bound_min_z,
        #                               bound_max_z=bound_max_z,
        #                               increments=self._density,
        #                               radius=self._radius,
        #                               face=self._face,
        #                               planet_root=self._planet_root)
        
        # self.renderer.mesh = self._planet_root.generator.gen_mesh(bound_min_x=bound_min_x,
        #                                                           bound_max_x=bound_max_x,
        #                                                           bound_min_z=bound_min_z,
        #                                                           bound_max_z=bound_max_z,
        #                                                           face=self._face)

        self.renderer.mesh = self._planet_root.generator.gen_mesh(self._name)

        # Set PLANET texture
        self.renderer.material.texture = self._planet_root.generator.get_texture(self._name)
        self.renderer.material.shininess = 0.1

        
    def _get_quad(self, quadrant):
        found_quad = None
        if quadrant == QuadName.TL:
            found_quad = self._tl
        elif quadrant == QuadName.TR:
            found_quad = self._tr
        elif quadrant == QuadName.BL:
            found_quad = self._bl
        elif quadrant == QuadName.BR:
            found_quad = self._br
        else:
            print "Invalid Quadrant? %d" % quadrant
            
        return found_quad
        
    def _calc_corners(self):
        # Calculate the Cubic coordinates of this quad
        x0, y0, x1, y1, face = CubeSphereMap.get_address_bounds(self._name)

        self._corners = [x0, y0, x1, y1]
        self._centre_coords = CubeSphereMap.get_address_centre(self._name)
        self._quad_centres = [
                                CubeSphereMap.get_address_centre(self._name+'A'),
                                CubeSphereMap.get_address_centre(self._name+'B'),
                                CubeSphereMap.get_address_centre(self._name+'D'),
                                CubeSphereMap.get_address_centre(self._name+'C')
                             ]

        # if self._root:
        #     self._corners.append(0.0) #tl x
        #     self._corners.append(0.0) #tl y
        #     self._corners.append(1.0) #br x
        #     self._corners.append(1.0) #br y
        # else:
        #     parent_corners = self.transform.parent.node.corners
            
        #     if self._quad == QuadName.TL:
        #         self._corners.append(parent_corners[0])
        #         self._corners.append(parent_corners[1])
        #         self._corners.append(parent_corners[0] + (parent_corners[2] - parent_corners[0]) * 0.5 )
        #         self._corners.append(parent_corners[1] + (parent_corners[3] - parent_corners[1]) * 0.5 )
                
        #     elif self._quad == QuadName.TR:
        #         self._corners.append(parent_corners[0] + (parent_corners[2] - parent_corners[0]) * 0.5)
        #         self._corners.append(parent_corners[1])
        #         self._corners.append(parent_corners[2])
        #         self._corners.append(parent_corners[1] + (parent_corners[3] - parent_corners[1]) * 0.5 )
                
        #     elif self._quad == QuadName.BL:
        #         self._corners.append(parent_corners[0])
        #         self._corners.append(parent_corners[1] + (parent_corners[3] - parent_corners[1]) * 0.5)
        #         self._corners.append(parent_corners[0] + (parent_corners[2] - parent_corners[0]) * 0.5)
        #         self._corners.append(parent_corners[3])
                
            
        #     elif self._quad == QuadName.BR:
        #         self._corners.append(parent_corners[0] + (parent_corners[2] - parent_corners[0]) * 0.5)
        #         self._corners.append(parent_corners[1] + (parent_corners[3] - parent_corners[1]) * 0.5)
        #         self._corners.append(parent_corners[2])
        #         self._corners.append(parent_corners[3])
                
                
        # mid_x = (self._corners[2] - self._corners[0]) / 2
        # mid_y = (self._corners[3] - self._corners[1]) / 2
        
        # self._centre_coords = [(self._corners[0] + mid_x), (self._corners[1] + mid_y)]
        
        # self._quad_centres = [ [self._corners[0] + (mid_x/2), self._corners[1] + (mid_y/2)], #TL
        #                        [self._corners[2] - (mid_x/2), self._corners[1] + (mid_y/2)], #TR
        #                        [self._corners[2] - (mid_x/2), self._corners[3] - (mid_y/2)], #BR
        #                        [self._corners[0] + (mid_x/2), self._corners[3] - (mid_y/2)]  #BL
        #                      ]
        
        # Get world positions for centres of child quads
        self._child_pos = [CubeSphereMap.get_sphere_position(self._quad_centres[QuadName.TL][0],
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

    def _get_centre_position(self):
        return CubeSphereMap.get_sphere_position(self._centre_coords[0], 
                                                 self._centre_coords[1], 
                                                 self._face,
                                                 self._sphere_parent.radius)

    def update_surface(self):
        
        pos = self._sphere_parent.camera.node_parent.transform.position
        
        # Get the distances of the camera from the quads
        # This needs to be updated in future to handle transform applied to the planet
        # i.e. rotation and position
        distances = [pos.distance(self._child_pos[QuadName.TL]),
                     pos.distance(self._child_pos[QuadName.TR]),
                     pos.distance(self._child_pos[QuadName.BR]),
                     pos.distance(self._child_pos[QuadName.BL]),
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
        quad_size = self._child_pos[QuadName.TL] - self._child_pos[QuadName.BR] * 1.0 #( radius / frustrum radius)....
        
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
                    
                # Check the quadrant against the horizon distance
                if self._sphere_parent.horizon > 0.0 and \
                   (distances[quad_inc] - radius) > self._sphere_parent.horizon:
                    if not self._get_quad(quad_inc) is None:
                        self._get_quad(quad_inc)._merge()
                        #print "Horizon"
                    continue
               
                # Check the quadrant against the view frustrum
                if not self._get_quad(quad_inc) is None and not self._get_quad(quad_inc)._is_split:
                    child_quad_size = quad_size / 2.0
                    inside = self._sphere_parent.camera.sphere_inside(self._child_pos[quad_inc], child_quad_size) 
                    if inside == 1:
                        quad = self._get_quad(quad_inc)
                        #Logger.Log("Culling Quad: sz: %f name: %s pos: %s" % ( child_quad_size, quad.name, str(child_pos[quad_inc]) ) )
                        quad._merge()
                        continue
            
            if distances[quad_inc] > priority:
                if not self._get_quad(quad_inc) is None:
                    #print "merging due to distance: " + QuadName.quad_string(quad_inc)
                    self._get_quad(quad_inc)._merge()
                    
#                if self._level == self._planet_root._max_depth:
#                    print "merging split level: %d" % self._level
#                    print priority
#                    print distances
                    
                #print "Distance"
                continue

            # If the quad is futher away than its size then dont split it
            if distances[quad_inc] > quad_size:
                continue

#             if self._level <= self._planet_root._max_depth:
# #                print priority
# #                print distances
# #                print "Split level: %d" % self._levelx 
#                 Logger.Log("Splitting Quad: name: %s" % ( self.name) )
#                 self._split(quad_inc)
                
                
            if self._is_split:
                self._get_quad(quad_inc).update_surface()
            elif self._level <= self._planet_root._max_depth:
                #Logger.Log("Splitting Quad: name: %s" % ( self.name) )
                self._split(quad_inc) 
    
    def _can_merge(self):
        
        # If this node has children
        if self._is_split:
            return False
        
        #TODO: Add check to prevent this node from being merged if it is bordering a leaf node
        #      at the same level
        
        return True
       
    def _merge(self):
        
        #    child_quad = self.children[quadrant]
        children_merged = True
        
        if self._is_split:
            self.transform.remove_children()
            self._tl = None
            self._tr = None
            self._bl = None
            self._br = None
            
            self._is_split = False
        return True
            
    # Quadrant is currently unused.
    def _split(self, quadrant=-1):
        
        if not self._is_split:
            if not self._planet_root.can_split():
                return
            
            h_size = 1.0
            next_level = self._level + 1
            
            # build top left
            self._tl = SphereQuad(self._name+'A', self._sphere_parent, self._planet_root, radius=self._radius, root=False, level=next_level, density=self._density, face=self._face, quad=QuadName.TL )
            self.transform.add_child( self._tl.transform )
            self._tl._init_quad()
            
            # top right
            self._tr = SphereQuad(self._name+'B', self._sphere_parent, self._planet_root, radius=self._radius, root=False, level=next_level, density=self._density, face=self._face, quad=QuadName.TR )
            self.transform.add_child( self._tr.transform )
            self._tr._init_quad()
            
            # bottom left
            self._bl = SphereQuad(self._name+'C', self._sphere_parent, self._planet_root, radius=self._radius, root=False, level=next_level, density=self._density, face=self._face, quad=QuadName.BL )
            self.transform.add_child( self._bl.transform )
            self._bl._init_quad()
            
            # bottom right
            self._br = SphereQuad(self._name+'D', self._sphere_parent, self._planet_root, radius=self._radius, root=False, level=next_level, density=self._density, face=self._face, quad=QuadName.BR )
            self.transform.add_child( self._br.transform )
            self._br._init_quad()
            
            self._is_split = True
            
    def hit_test(self, coord, quad=-1):
        if coord.face == self.face:
            if not quad == -1:
                mid_x = ((self._corners[0] + self._corners[2]) / 2.0)
                mid_y = ((self._corners[1] + self._corners[3]) / 2.0)
                
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
        if self._is_split:
            
            # Draw sorted children
            for quad_inc in self._sorted_quads:
                self._get_quad(quad_inc).draw()
            
        # If not split then draw self and don't draw children
        else:
            self.renderer.draw()
            
    