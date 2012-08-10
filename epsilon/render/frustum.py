'''
Created on Sep 17, 2011

@author: scottporter
'''
import math
from itertools import chain

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.core.input import Input

from epsilon.core.settings import DisplaySettings
from epsilon.geometry.euclid import Plane, Point3, Vector3, Matrix4
from epsilon.render.colour import Preset
from epsilon.render.transform import Transform
from epsilon.scene.nodecomponent import NodeComponent

from epsilon.render.gizmos.gizmomanager import GizmoManager

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
        self._fov = 75.0
        
        self._frustum_planes = []
        
        # Build Near/Far Planes
        self._calc_near_far()
        
        # Internal Stats
        self._num_inside = 0
        self._num_outside = 0
        self._num_intersect = 0
        
        # Debug
        self._update_frustum = True
        
        # Frustum Plane Gizmos
        self._topg = GizmoManager.draw_plane(Vector3(), size=15.0)
        self._topg.colour = Preset.blue
        self._bottomg = GizmoManager.draw_plane(Vector3(), size=15.0)
        self._bottomg.colour = Preset.red
        self._leftg = GizmoManager.draw_plane(Vector3(), size=15.0)
        self._leftg.colour = Preset.orange
        self._rightg = GizmoManager.draw_plane(Vector3(), size=15.0)
        self._rightg.colour = Preset.purple

        # Lines
        self._tl = GizmoManager.draw_line(Vector3())
        self._tl.start_colour = Preset.red
        self._tr = GizmoManager.draw_line(Vector3())
        self._tr.start_colour = Preset.red
        self._bl = GizmoManager.draw_line(Vector3())
        self._bl.start_colour = Preset.red
        self._br = GizmoManager.draw_line(Vector3())
        self._br.start_colour = Preset.red
        
        self._forward = GizmoManager.draw_line(Vector3())
        self._forward.start_colour = Preset.green
        self._forward.end_colour = Preset.green
        

        self._cam_pos = GizmoManager.draw_cube(Vector3(), 1.0, 1.0, 1.0)
    
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
        
        if Input.get_key(Input.KEY_1):
            if not self._update_frustum:
                self._update_frustum = True#not self._update_frustum
                print "Frustum update enabled"
                print "cam pos: %s" % self._transform.position

        if Input.get_key(Input.KEY_2):
            if self._update_frustum:
                self._update_frustum = False
                print "Frustum update disabled"
                print "@ cam pos: %s" % self._transform.position

        if Input.get_key(Input.KEY_3):
            print "Camera pos: %s" % self._transform.position
            print "marker pos: %s" % self._cam_pos.transform.position
        
        if self._update_frustum:
            self.calc_frustum()
            
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self._fov, self._aspect, self._near_dist, self._far_dist)
        
    def set_screen(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, (self._width - 1), 0, (self._height - 1) )
        
    def _calc_near_far(self):
#        tang = float(math.tan((math.pi/180) * self._fov * 0.5))
        fov_r = (math.pi/180) * self._fov * 0.5 
        tang = 2.0 * math.tan(fov_r)
        
#        tang = 2.0 * math.tan(self._fov / 2.0)
        
        self._near_height = self._near_dist * tang
        self._near_width = self._near_height * (self._width/self._height)
        
        self._far_height = self._far_dist * tang
        self._far_width = self._far_height * tang
        
    def _vis_frustum(self):
        # calc centres of near/far planes
        near_centre = self._transform.position + self._transform.forward * self._near_dist
        far_centre = self._transform.position + self._transform.forward * self._far_dist
        
        # Camera pos
        self._cam_pos.transform.position = near_centre.copy()
        self._cam_pos.transform.rotation = self.node_parent.transform.rotation.copy()

        # Frustrum Area
        tl = near_centre.copy()
        tl += self._transform.right * self._near_width
        tl += self._transform.up * self._near_height
        
        tlb = far_centre.copy()
        tlb += self._transform.right * self._far_width
        tlb += self._transform.up * self._far_height
        self._tl.transform.position = tl
        self._tl.line_to(tlb)
        
        tr = near_centre.copy()
        tr += -self._transform.right * self._near_width
        tr += self._transform.up * self._near_height
        
        trb = far_centre.copy()
        trb += -self._transform.right * self._far_width
        trb += self._transform.up * self._far_height
        self._tr.transform.position = tr
        self._tr.line_to(trb)
        
        bl = near_centre.copy()
        bl += self._transform.right * self._near_width
        bl += -self._transform.up * self._near_height
        
        blb = far_centre.copy()
        blb += self._transform.right * self._far_width
        blb += -self._transform.up * self._far_height
        
        self._bl.transform.position = bl
        self._bl.line_to(blb)
        
        br = near_centre.copy()
        br += -self._transform.right * self._near_width
        br += -self._transform.up * self._near_height
        
        brb = far_centre.copy()
        brb += -self._transform.right * self._far_width
        brb += -self._transform.up * self._far_height
        self._br.transform.position = br
        self._br.line_to(brb)

        self._forward.transform.position = self._transform.position.copy()
        self._forward.line_to(self._transform.forward * 3.0)
        
    def calc_frustum(self):
        
        self._vis_frustum()
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
        p = Plane(Point3(pp.x, pp.y, pp.z), normal)
        p.name = "top"
        self._frustum_planes.append(p)
        
        self._topg.transform.position = pp + aux * 5.0
        self._topg.normal = normal
        
        # Calc Bottom plane
        aux = (near_centre - self._transform.up * self._near_height) - self._transform.position
        aux.normalize()
        normal = self._transform.right.cross(aux)
        pp = near_centre - self._transform.up * self._near_height
        p = Plane(Point3(pp.x, pp.y, pp.z), normal)
        p.name = "bottom"
        self._frustum_planes.append(p)
        
        self._bottomg.transform.position = pp  + aux * 5.0
        self._bottomg.normal = normal
        
        # Calc Left plane
        aux = (near_centre - self._transform.right * self._near_width) - self._transform.position
        aux.normalize()
        normal = aux.cross(self._transform.up)
        pp = near_centre - self._transform.right * self._near_width

        mat = glGetDoublev(GL_PROJECTION_MATRIX)
        mat = list(chain.from_iterable(mat))

        # The normal needs to be reflected, this is close but not quite.
        # I think need to read the matrix differently

        x = float(mat[3] + mat[0])
        y = float(mat[7] + mat[4])
        z = float(mat[11] + mat[8])
        # d = (mat[15] + mat[12])

        norm = Vector3(x,y,z)
        norm.normalize()    
        if norm.magnitude() > 0.0:
            normal = norm

        # n = ( x*x + y*y + z*z ) / 3.0
        # d /= n

        if Input.get_key(Input.KEY_4):
            print "Projection matrix:"

            # mm = glGetDoublev(GL_MODELVIEW_MATRIX)
            # mm = list(chain.from_iterable(mm))
            # print mm
            # model_mat = Matrix4()

            # pm = glGetDoublev(GL_PROJECTION_MATRIX)

            # proj_mat = Matrix4(list(chain.from_iterable(pm)))

            # print proj_mat

            
            print "Left: %s d: %3.2f" % (normal, d)

            print "plane: %s" % p

            #p = Plane(Point3(x,y,z),d)
        
        p = Plane(Point3(pp.x, pp.y, pp.z), normal)
        p.name = "left"
        self._leftg.transform.position = pp  + aux.normalize() * 5.0
        self._leftg.normal = normal


        self._frustum_planes.append(p)

        # Calc Right plane
        aux = (near_centre + self._transform.right * self._near_width) - self._transform.position
        aux.normalize()
        normal = self._transform.up.cross(aux)
        pp = near_centre + self._transform.right * self._near_width
        p = Plane(Point3(pp.x, pp.y, pp.z), normal)
        p.name = "right"
        self._frustum_planes.append(p)
        
        self._rightg.transform.position = pp  + aux.normalize() * 5.0
        self._rightg.normal = normal
        
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
                    print "Failing plane: " + plane.name
                elif out_corners > 0:
                    result = self.INTERSECT
        
        if result == self.OUTSIDE:
            self._num_outside += 1
        elif result == self.INSIDE:
            self._num_inside += 1
        elif result == self.INTERSECT:
            self._num_intersect += 1
        
        return result
        