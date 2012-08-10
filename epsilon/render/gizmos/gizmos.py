import math
from OpenGL.GL import *

from epsilon.core.input import Input

from epsilon.geometry.euclid import Vector3
from epsilon.scene.node import Node
from epsilon.render.colour import Preset

class WireSphere(Node):
    def __init__(self, position=Vector3(0,0,0), radius=1.0):
        Node.__init__(self)
        self.transform.position = position
        print "Wire Sphere position: %s" % self.transform.position
        self._radius = radius
        
        #self.transform.position.y -= self._radius
        
        
    def draw(self):
        
        self.renderer._setup_draw()
        
        glBegin(GL_LINE_LOOP)
        
        # On x-axis
        for i in range(0, 50):
            vt = self.transform.position.copy()
            vt.x += math.cos((2*math.pi/50)*i) * self._radius
            vt.y += math.sin((2*math.pi/50)*i) * self._radius
            vt.z += 0
            glVertex3f(vt.x,vt.y,vt.z)
        glEnd()
        
        glBegin(GL_LINE_LOOP)
        
        # On z-axis
        for i in range(0, 50):
            vt = self.transform.position.copy()
            vt.x += 0
            vt.z += math.cos((2*math.pi/50)*i) * self._radius
            vt.y += math.sin((2*math.pi/50)*i) * self._radius
            glVertex3f(vt.x,vt.y,vt.z)
        glEnd()
        
        self.renderer._teardown_draw()
        
class Line(Node):
    def __init__(self, position=Vector3(0,0,0), direction=Vector3(0,0,0), length=1.0):
        Node.__init__(self)
        self.transform.position = position
        self._direction = direction.normalized()
        self._length = length
        self._start_colour = Preset.white
        self._end_colour = Preset.red
        
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, new_dir):
        self._direction = new_dir
        
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, new_length):
        self._length = new_length
        
    @property
    def start_colour(self):
        return self._start_colour
    
    @start_colour.setter
    def start_colour(self, new_s_c):
        self._start_colour = new_s_c
        
    @property
    def end_colour(self):
        return self._end_colour
    
    @end_colour.setter
    def end_colour(self, new_e_c):
        self._end_colour = new_e_c
        
    def line_to(self, to_pos):
        if isinstance(to_pos, Vector3):
            dir = to_pos - self.transform.position
            length = dir.magnitude()
            dir = dir.normalized()
            self._direction = dir
            self._length = length
        
    def draw(self):
        
        self.renderer._setup_draw()
        
        ve = self._direction * self._length
        
        glBegin(GL_LINES)
        glColor3f(self._start_colour.r, self._start_colour.g, self._start_colour.b)
        glVertex3f(0, 0, 0)
        glColor3f(self._end_colour.r, self._end_colour.g, self._end_colour.b)
        glVertex3f(ve.x,ve.y,ve.z)
        glEnd()
        
        glColor3f(1.0, 1.0, 1.0)

        self.renderer._teardown_draw()
                
class WireCube(Node):
    
    # width, height, depth, max, and min are all relative to the object.
    # you cannot specify world coordinates for min max
    def __init__(self, 
                 position=Vector3(0,0,0), 
                 width=None, 
                 height=None, 
                 depth=None, 
                 max=Vector3(0.5, 0.5, 0.5), 
                 min=Vector3(-0.5,-0.5,-0.5) ):
        
        Node.__init__(self, name="WireCube")
        
        self.transform.position = position
        
        self._width = width     # X
        self._height = height   # Y
        self._depth = depth     # Z
        
        self._min = min
        self._max = max
        
        # Gen min/max - Will override explictly defined min/max - so pick one or the other!
        if not width is None and not height is None and not depth is None:
            hw = width / 2.0
            hh = height / 2.0
            hd = depth / 2.0
            
            self._min = Vector3(-hw, -hh, -hd) + position
            self._max = Vector3(hw, hh, hd) + position
        
        self.gen_coords()

        self._colour = Preset.white
        
    @property
    def min(self):
        return self._min
    
    @min.setter
    def min(self, new_min):
        self._min = new_min
        self.gen_coords()
        
    @property
    def max(self):
        return self._max
        
    @max.setter
    def max(self, new_max):
        self._max = new_max
        self.gen_coords()

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, new_colour):
        self._colour = new_colour
        
    def gen_coords(self):
        self._coords = []
        
        # Transform coords local
        max = self._max# + self.transform.local_position
        min = self._min# + self.transform.local_position
        
        #top
        self._coords.append(max)
        self._coords.append(Vector3(min.x, max.y, max.z ))
        self._coords.append(Vector3(min.x, max.y, min.z ))
        self._coords.append(Vector3(max.x, max.y, min.z ))
        
        #bottom
        self._coords.append(min)
        self._coords.append(Vector3(max.x, min.y, min.z ))
        self._coords.append(Vector3(max.x, min.y, max.z ))
        self._coords.append(Vector3(min.x, min.y, max.z ))
    
    def draw(self):
        
        self.gen_coords()
        
        self.renderer._setup_draw()
        
        glColor4f(self._colour.r, self._colour.g, self._colour.b, 0.5)

        # Fill the sides
        glBegin(GL_TRIANGLES)

        # Top
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)

        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)
        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)
        
        # Bottom
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)
        glVertex3f(self._coords[5].x, self._coords[5].y, self._coords[5].z)
        glVertex3f(self._coords[6].x, self._coords[6].y, self._coords[6].z)

        glVertex3f(self._coords[7].x, self._coords[7].y, self._coords[7].z)
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)
        glVertex3f(self._coords[6].x, self._coords[6].y, self._coords[6].z)

        # Sides
        glVertex3f(self._coords[6].x, self._coords[6].y, self._coords[6].z)
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)

        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)
        glVertex3f(self._coords[5].x, self._coords[5].y, self._coords[5].z)
        glVertex3f(self._coords[6].x, self._coords[6].y, self._coords[6].z)

        # back
        glVertex3f(self._coords[7].x, self._coords[7].y, self._coords[7].z)
        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)

        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[6].x, self._coords[6].y, self._coords[6].z)
        glVertex3f(self._coords[7].x, self._coords[7].y, self._coords[7].z)

        # right
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)
        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)

        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)
        glVertex3f(self._coords[7].x, self._coords[7].y, self._coords[7].z)
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)


        # front
        glVertex3f(self._coords[5].x, self._coords[5].y, self._coords[5].z)
        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)

        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)
        glVertex3f(self._coords[5].x, self._coords[5].y, self._coords[5].z)

        glEnd()

        glColor4f(self._colour.r, self._colour.g, self._colour.b, 1.0)
        
        # Top
        glBegin(GL_LINE_LOOP)
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)
        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glEnd()
        
        # Bottom
        glBegin(GL_LINE_LOOP)
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)
        glVertex3f(self._coords[5].x, self._coords[5].y, self._coords[5].z)
        glVertex3f(self._coords[6].x, self._coords[6].y, self._coords[6].z)
        glVertex3f(self._coords[7].x, self._coords[7].y, self._coords[7].z)
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)
        glEnd()
        
        #Sides
        glBegin(GL_LINES)
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[6].x, self._coords[6].y, self._coords[6].z)
        
        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)
        glVertex3f(self._coords[7].x, self._coords[7].y, self._coords[7].z)
        
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)
        
        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)
        glVertex3f(self._coords[5].x, self._coords[5].y, self._coords[5].z)
        glEnd()
        
        self.renderer._teardown_draw()
        
class WirePlane(Node):
    
    def __init__(self, pos, normal=Vector3.UP(), size=1.0):
        
        Node.__init__(self, name="WirePlane")
        
        self.transform.position = pos
        self._normal = normal.normalized()
        self._size = size
        self._colour = Preset.white
        self._gen_offset_coords()
        
    @property
    def normal(self):
        return self._normal
    
    @normal.setter
    def normal(self, new_normal):
        self._normal = new_normal
        self._gen_offset_coords()
    
    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, new_colour):
        self._colour = new_colour

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, new_size):
        self._size = new_size
        self._gen_offset_coords()
        
    def _gen_offset_coords(self):
        
        perp_z = Vector3.RIGHT()

        # gen perpendicular vector
        if not self._normal == Vector3.RIGHT():
            perp_z = self._normal.cross(Vector3.RIGHT())
        elif not self._normal == Vector3.UP():
            perp_z = self._normal.cross(Vector3.UP())
        
        perp_x = self._normal.cross(perp_z)
        
        perp_x *= self._size
        perp_z *= self._size
        
        tl = -perp_x + perp_z
        tr = perp_x + perp_z
        bl = -perp_x + -perp_z
        br = perp_x + -perp_z
        
        self._offset_coords = [tl, tr, br, bl]
        
    def _gen_coords(self):
        self._coords = []
        
        for coord in self._offset_coords:
            self._coords.append(coord)
        self._coords.append(Vector3())
        self._coords.append((self._normal * self._size) )
        
    def draw(self):
        
        self._gen_coords()
        
        self.renderer._setup_draw()
        
        #glColor3f(self.material.diffuse.r, self.material.diffuse.g, self.material.diffuse.b)
        glColor4f(self._colour.r, self._colour.g, self._colour.b, 0.5)
        
        # Plane triangles
        glBegin(GL_TRIANGLES)
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)

        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)
        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)
        
        glEnd()

        glColor4f(self._colour.r, self._colour.g, self._colour.b, 1.0)

        # Plane outer
        glBegin(GL_LINE_LOOP)
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)
        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glEnd()
        
        glBegin(GL_LINES)
        glVertex3f(self._coords[1].x, self._coords[1].y, self._coords[1].z)
        glVertex3f(self._coords[3].x, self._coords[3].y, self._coords[3].z)
        
        glVertex3f(self._coords[0].x, self._coords[0].y, self._coords[0].z)
        glVertex3f(self._coords[2].x, self._coords[2].y, self._coords[2].z)
        
        # Normal
        glVertex3f(self._coords[4].x, self._coords[4].y, self._coords[4].z)
        glVertex3f(self._coords[5].x, self._coords[5].y, self._coords[5].z)
        glEnd()
        
        self.renderer._teardown_draw()
        
    