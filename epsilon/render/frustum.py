'''
Created on Sep 17, 2011

@author: scottporter
'''
import math
from itertools import chain

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.core.settings import Settings

from epsilon.core.input import Input
from epsilon.logging.logger import Logger

from epsilon.core.settings import Settings
from epsilon.geometry.euclid import Plane, Point3, Vector3, Matrix4
from epsilon.render.colour import Preset
from epsilon.render.transform import Transform
from epsilon.scene.nodecomponent import NodeComponent

from epsilon.render.rendersettings import RenderSettings

from epsilon.render.gizmos.gizmomanager import GizmoManager

from epsilon.events.eventbase import EventBase

class FrustumStatus(EventBase):
    def __init__(self, status):
        EventBase.__init__(self, 'FrustumStatus', status)

class Frustum(NodeComponent):
    # Intersection Constants
    INSIDE = 0
    OUTSIDE = 1
    INTERSECT = 2

    #near
    NTL = 0
    NBL = 1
    NTR = 2
    NBR = 3

    #far
    FTL = 0
    FBL = 1
    FTR = 2
    FBR = 3
    
    def __init__(self, width=None, 
                       height=None):
        NodeComponent.__init__(self)
        
        if width is None:
            width = Settings.get('DisplaySettings','resolution')[0]

        if height is None:
            height = Settings.get('DisplaySettings','resolution')[1]

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
        if Settings.has_option('RenderSettings','update_frustum'):
            self._update_frustum = Settings.get('RenderSettings','update_frustum')
        else:
            Settings.set('RenderSettings','update_frustum', self._update_frustum)
        
        self._top = None
        self._bottom = None
        self._left = None
        self._right = None

        self._verts = []

        self._gizmos = None

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
        
        self._update_frustum = Settings.get('RenderSettings','update_frustum')

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
            
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self._fov, self._aspect, self._near_dist, self._far_dist)
        
        if self._update_frustum:
            #self.calc_frustum()
            self.calc_frustum_lighthouse()
        
        # show the frustum visualisation
        self._vis_frustum(not self._update_frustum)
    
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

    def _calc_frustum_verts(self):
        
        # calc centres of near/far planes
        near_centre = self._transform.position + self._transform.forward * self._near_dist
        far_centre = self._transform.position + self._transform.forward * self._far_dist
        
        # Frustrum Area
        self._verts = []

        # NTL
        tl = near_centre.copy()
        tl += self._transform.right * self._near_width
        tl += self._transform.up * self._near_height
        self._verts.append(tl)
        
        # NBL
        bl = near_centre.copy()
        bl += self._transform.right * self._near_width
        bl += -self._transform.up * self._near_height
        self._verts.append(bl)

        # NTR
        tr = near_centre.copy()
        tr += -self._transform.right * self._near_width
        tr += self._transform.up * self._near_height
        self._verts.append(tr)

        # NBR
        br = near_centre.copy()
        br += -self._transform.right * self._near_width
        br += -self._transform.up * self._near_height
        self._verts.append(br)

        # FTL
        tlb = far_centre.copy()
        tlb += self._transform.right * self._far_width
        tlb += self._transform.up * self._far_height
        self._verts.append(tlb)

        # FBL
        blb = far_centre.copy()
        blb += self._transform.right * self._far_width
        blb += -self._transform.up * self._far_height
        self._verts.append(blb)

        # FTR
        trb = far_centre.copy()
        trb += -self._transform.right * self._far_width
        trb += self._transform.up * self._far_height
        self._verts.append(trb)

        # FBR
        brb = far_centre.copy()
        brb += -self._transform.right * self._far_width
        brb += -self._transform.up * self._far_height
        self._verts.append(brb)

    def _vis_frustum(self, show):

        if show:
            if self._gizmos is None:
                # Create gizmos
                # Frustum Plane Gizmos
                self._gizmos = []

                self._topg = GizmoManager.draw_plane(Vector3(), size=15.0, colour=Preset.blue)
                self._bottomg = GizmoManager.draw_plane(Vector3(), size=15.0, colour=Preset.red)
                self._leftg = GizmoManager.draw_plane(Vector3(), size=15.0, colour=Preset.orange)
                self._rightg = GizmoManager.draw_plane(Vector3(), size=15.0, colour=Preset.purple)

                self._gizmos.append(self._topg)
                self._gizmos.append(self._bottomg)
                self._gizmos.append(self._rightg)
                self._gizmos.append(self._leftg)

                # Lines
                self._tl = GizmoManager.draw_line(Vector3(), colour=Preset.red)
                self._tr = GizmoManager.draw_line(Vector3(), colour=Preset.red)
                self._bl = GizmoManager.draw_line(Vector3(), colour=Preset.red)
                self._br = GizmoManager.draw_line(Vector3(), colour=Preset.red)

                self._gizmos.append(self._tl)
                self._gizmos.append(self._tr)
                self._gizmos.append(self._bl)
                self._gizmos.append(self._br)
                
                self._oforward = GizmoManager.draw_line(Vector3(), colour=Preset.blue)
                self._oup = GizmoManager.draw_line(Vector3(), colour=Preset.green)
                self._oright = GizmoManager.draw_line(Vector3(), colour=Preset.red)
                self._gizmos.append(self._oforward)
                self._gizmos.append(self._oup)
                self._gizmos.append(self._oright)

                #self._cam_pos = GizmoManager.draw_cube(Vector3(), 1.0, 1.0, 1.0)
            
                self._tl.transform.position = self._verts[self.NTL]
                self._tl.line_to(self._verts[self.FTL])
                
                self._tr.transform.position = self._verts[self.NTR]
                self._tr.line_to(self._verts[self.FTR])
                
                self._bl.transform.position = self._verts[self.NBL]
                self._bl.line_to(self._verts[self.FBL])
                
                self._br.transform.position = self._verts[self.NBR]
                self._br.line_to(self._verts[self.FBR])

                # Transform orientation
                self._oforward.transform.position = self._transform.position.copy()
                self._oforward.direction = self._transform.forward
                self._oforward.length = 3.0
                
                self._oup.transform.position = self._transform.position.copy()
                self._oup.direction = self._transform.up
                self._oup.length = 3.0
                
                self._oright.transform.position = self._transform.position.copy()
                self._oright.direction = self._transform.right
                self._oright.length = 3.0

                # Frustum plane visualisation
                self._topg.transform.position = self._transform.position
                self._topg.normal = self._top.n

                self._bottomg.transform.position = self._transform.position
                self._bottomg.normal = self._bottom.n

                self._leftg.transform.position = self._transform.position
                self._leftg.normal = self._left.n

                self._rightg.transform.position = self._transform.position
                self._rightg.normal = self._right.n
        else:
            if not self._gizmos is None:
                for giz in self._gizmos:
                    GizmoManager.remove_gizmo(giz)
                self._gizmos = None
        
        
    def calc_frustum(self):
        
        # Using vector manipulation

        # Update frustrum planes
        self._frustum_planes = []

        # calc centres of near/far planes
        near_centre = self._transform.position + self._transform.forward * self._near_dist
        #far_centre = self._transform.position + self._transform.forward * self._far_dist
        
        # Calc Top plane
        # ------------------------------
        
        aux = (near_centre + self._transform.up * self._near_height) - self._transform.position
        aux.normalize()
        normal = aux.cross(self._transform.right)
        #pp = near_centre + self._transform.up * self._near_height
        #self._top = Plane(Point3(pp.x, pp.y, pp.z), normal)
        self._top = Plane(self._transform.position, normal)
        self._top.name = "top"
        self._frustum_planes.append(self._top)
        
        # -------------------------------

        # Calc Bottom plane

        # -------------------------------

        aux = (near_centre - self._transform.up * self._near_height) - self._transform.position
        aux.normalize()
        normal = self._transform.right.cross(aux)
        # pp = near_centre - self._transform.up * self._near_height
        # self._bottom = Plane(Point3(pp.x, pp.y, pp.z), normal)
        self._bottom = Plane(self._transform.position, normal)
        self._bottom.name = "bottom"
        self._frustum_planes.append(self._bottom)
        
        # -------------------------------

        # Calc Right plane

        # -------------------------------
        
        aux = (near_centre - self._transform.right * self._near_width) - self._transform.position
        aux.normalize()
        normal = aux.cross(self._transform.up)
        # pp = near_centre - self._transform.right * self._near_width
        # self._right = Plane(Point3(pp.x, pp.y, pp.z), normal)
        self._right = Plane(self._transform.position, normal)
        self._right.name = "right"
        self._frustum_planes.append(self._right)

        # -------------------------------

        # Calc Left plane

        # -------------------------------

        aux = (near_centre + self._transform.right * self._near_width) - self._transform.position
        aux.normalize()
        normal = self._transform.up.cross(aux)
        # pp = near_centre + self._transform.right * self._near_width
        # self._left = Plane(Point3(pp.x, pp.y, pp.z), normal)
        self._left = Plane(self._transform.position, normal)
        self._left.name = "left"
        self._frustum_planes.append(self._left)
        
        # Update the frustum visualisation
        self._calc_frustum_verts()
        self._vis_frustum()

        # Reset stats for this frame
        self._num_inside = 0
        self._num_outside = 0
        self._num_intersect = 0

    def calc_frustum_lighthouse(self):

        self._calc_frustum_verts()

        # Update frustrum planes
        self._frustum_planes = []

        verts = []
        for v in self._verts:
            verts.append(Point3(v.x, v.y, v.z))

        cp = Point3(self._transform.position.x,self._transform.position.y,self._transform.position.z)

        self._top = Plane(verts[self.FTR],verts[self.FTL],cp)
        self._top.name = "top"
        self._frustum_planes.append(self._top)
        
        # -------------------------------
        # Calc Bottom plane
        # -------------------------------

        self._bottom = Plane(verts[self.FBL],verts[self.FBR],cp)
        self._bottom.name = "bottom"
        self._frustum_planes.append(self._bottom)
        
        # -------------------------------
        # Calc Right plane
        # -------------------------------
        
        self._right = Plane(verts[self.FBR],verts[self.FTR],cp)
        self._right.name = "right"
        self._frustum_planes.append(self._right)

        # -------------------------------
        # Calc Left plane
        # -------------------------------

        self._left = Plane(verts[self.FTL],verts[self.FBL],cp)
        self._left.name = "left"
        self._frustum_planes.append(self._left)
        
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
        
        # data = [True,True,True,True]

        for i in range(0, len(self._frustum_planes)):
            plane = self._frustum_planes[i]
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
                # data[i]=False
            elif out_corners > 0:
                result = self.INTERSECT
        
        # FrustumStatus(data).send()

        if result == self.OUTSIDE:
            self._num_outside += 1
        elif result == self.INSIDE:
            self._num_inside += 1
        elif result == self.INTERSECT:
            self._num_intersect += 1
        
        return result
        