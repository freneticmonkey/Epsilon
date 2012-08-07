
from OpenGL.GL import *

from epsilon.geometry.euclid import Vector3
from epsilon.render.colour import Colour, Preset

class InvalidCoordinate(Exception): pass

# TODO: Bounds - Doesn't currently handle transformations.  
# For example, won't handle rotated bounding boxes. Thinking about it 
# I've basically implemented axis aligned bounding boxes.  But without support for scale.


class Bounds(object):
    draw_bounds = False
    @classmethod
    def set_draw_bounds(cls, draw):
        cls.draw_bounds = draw
    
    @classmethod
    def get_draw_bounds(cls):
        return cls.draw_bounds
    
    def __init__(self, bottom_bound=Vector3(0,0,0), 
                       top_bound=Vector3(0,0,0),
                       world_centre=Vector3(0,0,0)):
            
        self._world_centre = world_centre
        
        self._top_offset = top_bound
        self._bottom_offset = bottom_bound
        
        self._update()
        
        self._colour = Preset.white
        
    def _update(self):
        # Update world bounds
        self._world_top_bound = self._top_offset + self._world_centre
        self._world_bottom_bound = self._bottom_offset + self._world_centre
        
    @property
    def max(self):
        return self._world_top_bound
    
    @property
    def max_offset(self):
        return self._top_offset
    
    @property
    def min(self):
        return self._world_bottom_bound
    
    @property
    def min_offset(self):
        return self._bottom_offset
        
    @property
    def world_centre(self):
        return self._centre
    
    @world_centre.setter
    def world_centre(self, new_centre):
        self._world_centre = new_centre
        self._update()
    
    @property
    def height(self):
        return self._top_offset.y - self._bottom_offset.y
    
    @property
    def width(self):
        return self._top_offset.x - self._bottom_offset.x
    
    @property
    def depth(self):
        return self._top_offset.z - self._bottom_offset.z
    
    @property
    def is_empty(self):
        return self.height == 0 and self.width == 0 and self.depth == 0
    
    @property
    def colour(self):
        return self._colour
    
    @colour.setter
    def colour(self, new_colour):
        self._colour = new_colour
    
    def __repr__(self):
        return "World centre: %s Width: %4.2f Height: %4.2f Depth: %4.3f" % (self._world_centre, self.width, self.height, self.depth)
    
#    @property
#    def gizmo(self):
#        return self._wire_cube
    
    # Create a volume that encompasses both bounds objects
    def __add__(self, other):
        if isinstance(other, Bounds):
            
            # This is calculated in world bounds
            
            max_x = self.max.x
            if other.max.x > max_x:
                max_x = other.max.x
                
            max_y = self.max.y
            if other.max.y > max_y:
                max_y = other.max.y
            
            max_z = self.max.z
            if other.max.z > max_z:
                max_z = other.max.z
                
            min_x = self.min.x
            if other.min.x < min_x:
                min_x = other.min.x
                
            min_y = self.min.y
            if other.min.y < min_y:
                min_y = other.min.y
            
            min_z = self.min.z
            if other.min.z < min_z:
                min_z = other.min.z
                
        # Convert the world coordinates of the bounds to offsets
        max = Vector3(max_x, max_y, max_z) - self._world_centre
        min = Vector3(min_x, min_y, min_z) - self._world_centre
            
        return Bounds( min, max, self._world_centre ) 
            
#        raise ValueError("Parameter is not a Bounds object")
       
    # Added to help with frustum calcs
    def get_corners(self):
        coords = []
        #top
        coords.append(self._world_top_bound)
        coords.append(Vector3(self._world_top_bound.x,    self._world_top_bound.y, self._world_bottom_bound.z ))
        coords.append(Vector3(self._world_bottom_bound.x, self._world_top_bound.y, self._world_bottom_bound.z ))
        coords.append(Vector3(self._world_bottom_bound.x, self._world_top_bound.y, self._world_top_bound.z ))
        
        #bottom
        coords.append(self._world_bottom_bound)
        coords.append(Vector3(self._world_top_bound.x,    self._world_bottom_bound.y, self._world_bottom_bound.z ))
        coords.append(Vector3(self._world_top_bound.x,    self._world_bottom_bound.y, self._world_top_bound.z ))
        coords.append(Vector3(self._world_bottom_bound.x, self._world_bottom_bound.y, self._world_top_bound.z ))
        
        return coords
    
    # Get corners in local coordinates for wire cube drawing.
    def get_local_corners(self):
        coords = []
        #top
        coords.append(self._top_offset)
        coords.append(Vector3(self._top_offset.x,    self._top_offset.y, self._bottom_offset.z ))
        coords.append(Vector3(self._bottom_offset.x, self._top_offset.y, self._bottom_offset.z ))
        coords.append(Vector3(self._bottom_offset.x, self._top_offset.y,    self._top_offset.z ))
        
        #bottom
        coords.append(self._bottom_offset)
        coords.append(Vector3(self._top_offset.x,    self._bottom_offset.y, self._bottom_offset.z ))
        coords.append(Vector3(self._top_offset.x,    self._bottom_offset.y,    self._top_offset.z ))
        coords.append(Vector3(self._bottom_offset.x, self._bottom_offset.y,    self._top_offset.z ))
        
        return coords
      
    # if the point within the bounds
    def within(self, coord):
        within = False
        if isinstance(coord, Vector3):
            within =  (self._top_bound.x > coord.x) and (self._bottom_bound.x < coord.x) and \
                      (self._top_bound.y > coord.y) and (self._bottom_bound.y < coord.y) and \
                      (self._top_bound.z > coord.z) and (self._bottom_bound.z < coord.z)
        else:
            raise InvalidCoordinate()
        
        return within
    
    def debug_draw(self):
        corners = self.get_local_corners()
        
        glColor3f(self._colour.r, self._colour.g, self._colour.b)
        
        # Top
        glBegin(GL_LINE_LOOP)
        glVertex3f(corners[0].x, corners[0].y, corners[0].z)
        glVertex3f(corners[1].x, corners[1].y, corners[1].z)
        glVertex3f(corners[2].x, corners[2].y, corners[2].z)
        glVertex3f(corners[3].x, corners[3].y, corners[3].z)
        glVertex3f(corners[0].x, corners[0].y, corners[0].z)
        glEnd()
        
        # Bottom
        glBegin(GL_LINE_LOOP)
        glVertex3f(corners[4].x, corners[4].y, corners[4].z)
        glVertex3f(corners[5].x, corners[5].y, corners[5].z)
        glVertex3f(corners[6].x, corners[6].y, corners[6].z)
        glVertex3f(corners[7].x, corners[7].y, corners[7].z)
        glVertex3f(corners[4].x, corners[4].y, corners[4].z)
        glEnd()
        
        #Sides
        glBegin(GL_LINES)
        glVertex3f(corners[0].x, corners[0].y, corners[0].z)
        glVertex3f(corners[6].x, corners[6].y, corners[6].z)
        
        glVertex3f(corners[1].x, corners[1].y, corners[1].z)
        glVertex3f(corners[5].x, corners[5].y, corners[5].z)
        
        glVertex3f(corners[2].x, corners[2].y, corners[2].z)
        glVertex3f(corners[4].x, corners[4].y, corners[4].z)
        
        glVertex3f(corners[3].x, corners[3].y, corners[3].z)
        glVertex3f(corners[7].x, corners[7].y, corners[7].z)
        glEnd()
        