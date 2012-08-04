'''
Created on Sep 17, 2011

@author: scottporter
'''
import math

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.core.settings import DisplaySettings
from epsilon.geometry.euclid import Plane, Point3
from epsilon.render.transform import Transform
from epsilon.scene.nodecomponent import NodeComponent

class Frustum(NodeComponent):
    # Intersection Constants
    INSIDE = 0
    OUTSIDE = 1
    INTERSECT = 2
    
    def __init__(self, width=DisplaySettings.resolution[0], 
                       height=DisplaySettings.resolution[1]):
        NodeComponent.__init__(self)
        
        self._width = width
        self._height = height
        
        self._near_dist = 0.1
        self._near_width = 0.0
        self._near_height = 0.0
        self._far_dist = 1000.0
        self._far_width = 0.0
        self._far_height = 0.0
        
        self._aspect = self._width / self._height
        self._fov = 45.0
        
        self._frustum_planes = []
        
        # Build Near/Far Planes
        self._calc_near_far()
        
        # Internal Stats
        self._num_inside = 0
        self._num_outside = 0
        self._num_intersect = 0
    
    @property
    def width(self):
        return self._width
    
    @property
    def width(self, new_width):
        self._width = new_width
        self._calc_near_far()
    
    @property
    def height(self):
        return self._height
    
    @property
    def height(self, new_height):
        self._height = new_height
        self._calc_near_far()
      
    @property
    def fov(self):
        return self._fov
    
    @fov.setter
    def fov(self, new_fov):
        self._fov = new_fov
        self._calc_near_far()
                
    def resize(self, width, height):
        self._width = width
        self._height = height
        glViewport(0, 0, width, height)
        
    def set_perspective(self):
        self.calc_frustum()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self._fov, self._aspect, self._near_dist, self._far_dist)
        
    def set_screen(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, (self._width - 1), 0, (self._height - 1) )
        
    def _calc_near_far(self):
        tang = float(math.tan((math.pi/180) * self._fov * 0.5))
        
        self._near_height = self._near_dist * tang
        self._near_width = self._near_height * (self._width/self._height)
        
        self._far_height = self._far_dist * tang
        self._far_width = self._far_height * tang
        
    def calc_frustum(self):
        
        # Update frustrum planes
        self._frustum_planes = []
        
        # calc centres of near/far planes
        near_centre = self._transform.position + self._transform.forward * self._near_dist
        far_centre = self._transform.position + self._transform.forward * self._far_dist
        
        # Calc Top plane
        aux = (near_centre + self._transform.up * self._near_height) - self._transform.position
        aux.normalize()
        normal = aux.cross(self._transform.right)
        pp = near_centre + self._transform.up * self._near_height
        self._frustum_planes.append(Plane(Point3(pp.x, pp.y, pp.z), normal))
        
        # Calc Bottom plane
        aux = (near_centre - self._transform.up * self._near_height) - self._transform.position
        aux.normalize()
        normal = self._transform.right.cross(aux)
        pp = near_centre - self._transform.up * self._near_height
        self._frustum_planes.append(Plane(Point3(pp.x, pp.y, pp.z), normal))
        
        # Calc Left plane
        aux = (near_centre - self._transform.right * self._near_width) - self._transform.position
        aux.normalize()
        normal = aux.cross(self._transform.up)
        pp = near_centre - self._transform.right * self._near_width
        self._frustum_planes.append(Plane(Point3(pp.x, pp.y, pp.z), normal))
        
        
        # Calc Right plane
        aux = (near_centre + self._transform.right * self._near_width) - self._transform.position
        aux.normalize()
        normal = self._transform.up.cross(aux)
        pp = near_centre + self._transform.right * self._near_width
        self._frustum_planes.append(Plane(Point3(pp.x, pp.y, pp.z), normal))
        
        # Reset stats for this frame
        self._num_inside = 0
        self._num_outside = 0
        self._num_intersect = 0
        
    def point_inside(self, point):
        
        result = self.INSIDE
        
        for plane in self._frustum_planes:
            if plane.distance(point) < 0:
                result = self.OUTSIDE
                break
            
        return result
    
    def sphere_inside(self, point, radius):
        
        result = self.INSIDE
        
        for plane in self._frustum_planes:
            distance = plane.distance(point)
            
            if distance < -radius:
                result = self.OUTSIDE
                
            elif distance < radius:
                result = self.INTERSECT
        
        if result == self.OUTSIDE:
            self._num_outside += 1
        elif result == self.INSIDE:
            self._num_inside += 1
        elif result == self.INTERSECT:
            self._num_intersect += 1
        
        return result
    
    # The bounds is a Axis Aligned Cube
    def bounds_inside(self, bounds):
        
        corners = bounds.get_corners()
        
        result = self.INSIDE
        
        for plane in self._frustum_planes:
            in_corners = 0
            out_corners = 0
            
            # Check each corner against this plane
            for corner in corners:
                
                if plane.distance(corner) < 0:
                    out_corners += 1
                else:
                    in_corners += 1
            
                # if all corners are out
                if in_corners == 0:
                    result = self.OUTSIDE
                elif out_corners > 0:
                    result = self.INTERSECT
        
        if result == self.OUTSIDE:
            self._num_outside += 1
        elif result == self.INSIDE:
            self._num_inside += 1
        elif result == self.INTERSECT:
            self._num_intersect += 1
        
        return result
        