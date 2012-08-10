import math
from datetime import datetime

from epsilon.ui.simplui import *
from epsilon.ui.uibasewindow import UIBaseWindow

from epsilon.render.gizmos.gizmomanager import GizmoManager

from epsilon.scene.node import Node#, Bounds
from epsilon.scene.scenemanager import SceneManager
from epsilon.geometry.euclid import Vector3

from epsilon.render.gizmos.gizmos import WireSphere, Line

from epsilon.environment.planet.cubespheremap import CubeSphereMap
from epsilon.environment.planet.spherequad import SphereQuad

class PlanetSphereDebugWindow(UIBaseWindow):
    def _setup_ui(self):
        self._dialog = Dialogue('Planet Sphere Debug',
                                x=700,
                                y=550,
                                content=
                                VLayout(hpadding=5, 
                                        children=
                                        [
                                         Checkbox('Track camera', action=self.track_camera_action, value=True),
                                         Label('x: 00.000 y: 00.000 z: 00.000', name='rel_camera_pos_label'),
                                         Label('face: UNKNOWN', name='face_name'),
                                         Label('x: 0.0000 y: 0.0000', name='camera_pos_label'),
                                         Label('x: 00.000 y: 00.000 z: 00.000', name='camera_real_pos_label'),
                                        ])
                                )
        self._frame.add(self._dialog)
        self._rel_camera_pos_label = self._frame.get_element_by_name('rel_camera_pos_label')
        self._face_name_label = self._frame.get_element_by_name('face_name')
        self._camera_pos_label = self._frame.get_element_by_name('camera_pos_label')
        self._camera_real_pos_label = self._frame.get_element_by_name('camera_real_pos_label')
        
        self._rel_camera_pos = Vector3(0,0,0)
        
        self._track_camera = True
    
    @property
    def rel_camera_pos(self):
        return self._rel_camera_pos
    
    @rel_camera_pos.setter
    def rel_camera_pos(self, new_cam_pos):
        self._rel_camera_pos = new_cam_pos
        
        self._rel_camera_pos_label.text = "x: %2.3f y: %2.3f z: %2.3f" % (new_cam_pos.x, new_cam_pos.y, new_cam_pos.z)
        
    @property
    def camera_pos(self):
        return self._camera_pos_label.text
    
    @camera_pos.setter
    def camera_pos(self, new_pos):
        
        face_name = "UNKNOWN"
        if new_pos.face == CubeSphereMap.TOP:
            face_name = 'TOP'
        elif new_pos.face == CubeSphereMap.BOTTOM:
            face_name = 'BOTTOM'
        elif new_pos.face == CubeSphereMap.LEFT:
            face_name = 'LEFT'
        elif new_pos.face == CubeSphereMap.RIGHT:
            face_name = 'RIGHT'
        elif new_pos.face == CubeSphereMap.FRONT:
            face_name = 'FRONT'
        elif new_pos.face == CubeSphereMap.BACK:
            face_name = 'BACK'
        
        self._face_name_label.text = "face: " + face_name
        
        self._camera_pos_label.text = "x: %1.4f y: %1.4f" % (new_pos.x, new_pos.y)
        
        # Convert the cubesphere coordinate back into world coordinates
        wc = CubeSphereMap.get_sphere_position(new_pos.x, new_pos.y, new_pos.face, 1.0)
        #wc = CubeSphereMap.get_sphere_vector(new_pos.x, new_pos.y, new_pos.face)
        self._camera_real_pos_label.text = "x: %3.2f y: %3.2f z: %3.2f" % (wc.x, wc.y, wc.z)
    
    @property
    def track_camera(self):
        return self._track_camera
        
    def track_camera_action(self, checkbox):
        self._track_camera = checkbox.value
        
class PlanetSphere(Node):
    def __init__(self, pos=Vector3(0,0,0), radius=10.0, density=4): #6.328
        Node.__init__(self)
        
        self.transform.position = pos
        print "Planet position: %s" % self.transform.position
        # The mesh density
        self._density = density
        
        # The camera position in sphere-space coordinates
        self._camera_pos = pos
        self._camera_pos_sc = None
        self._radius = radius
        self._horizon = 0.0
        
        self._max_depth = 8
        
        #self._camera_gizmo = WireSphere(radius=0.1)
        #self.transform.add_child(self._camera_gizmo.transform)
        
        self._camera_gizmo = GizmoManager.draw_sphere(Vector3(), radius=0.2)
        
        self._gen_faces()
        
        # The maximum height of the sphere surface (above the radius)
        self._max_height = (radius * 0.1)
        self._split_factor = 2.0  #16
        self._split_power = 1.1#1.25
        
        self._horizon = 0
        
#        self._ui = PlanetSphereDebugWindow()
        
        # Number splits this frame
        self._num_splits = 0
        # Max number of splits per frame
        self._max_splits = 8
        
#        pos = self.transform.position
#        pos.y += 0.1
#        self.transform.position.y = 1.0
#        self._line = Line(Vector3(0,1,0), Vector3(0, 0, 0), 5.0)
#        self.transform.add_child(self._line.transform)

        self._line = GizmoManager.draw_line(Vector3(-1,0,0), Vector3(0,0,0), 5.0)
        
#        self._cube_pos = Line(self.transform.position, Vector3(0, 0, 0), 5.0)
#        self.transform.add_child(self._cube_pos.transform)
        
        self._camera = None
        self._last_camera_pos = None
        self._last_time = datetime.now()
        
    @property
    def radius(self):
        return self._radius
    
    @property
    def max_height(self):
        return self._max_height
        
    @property
    def camera_pos(self):
        return self._camera_pos
    
    @property
    def camera_pos_sc(self):
        return self._camera_pos_sc
    
    @property
    def split_factor(self):
        return self._split_factor
    
    @property
    def split_power(self):
        return self._split_power
    
    @property
    def horizon(self):
        return self._horizon
    
    @property
    def ui(self):
        return self._ui
    
    @property
    def camera(self):
        return self._camera
    
    def can_split(self):
        split = False
        
#        print "Requesting split: # %d Max # %d" % (self._num_splits, self._max_splits )
        if self._num_splits < self._max_splits:
            split = True
            self._num_splits += 1
#            print "Granted"
#        else:
#            print "Rejected"
        
        return split
        
        
    def _gen_faces(self):
#        self._top =     SphereQuad(self, self, radius=self._radius, density=self._density, face=CubeSphereMap.TOP)
#        self._bottom =  SphereQuad(self, self, radius=self._radius, density=self._density, face=CubeSphereMap.BOTTOM)
#        self._front =   SphereQuad(self, self, radius=self._radius, density=self._density, face=CubeSphereMap.FRONT)
        self._back =    SphereQuad(self, self, radius=self._radius, density=self._density, face=CubeSphereMap.BACK)
#        self._left =    SphereQuad(self, self, radius=self._radius, density=self._density, face=CubeSphereMap.LEFT)
#        self._right =   SphereQuad(self, self, radius=self._radius, density=self._density, face=CubeSphereMap.RIGHT)
        
#        self.transform.add_child(self._top.transform)
#        self.transform.add_child(self._bottom.transform)
#        self.transform.add_child(self._front.transform)
        self.transform.add_child(self._back.transform)
#        self.transform.add_child(self._left.transform)
#        self.transform.add_child(self._right.transform)
        
#        self._top._init_quad()
#        self._bottom._init_quad()
#        self._front._init_quad()
        self._back._init_quad()
#        self._left._init_quad()
#        self._right._init_quad()
        
    def update_sphere(self):
        
#        start = datetime.now()
        
        if (datetime.now() - self._last_time).total_seconds() > 1.0:
        
#            if self._ui.track_camera:
        
            self._camera = SceneManager.get_instance().current_scene.active_camera
            
            # Store the camera pos for access by the quad children
            self._camera_pos = self._camera.node_parent.transform.position - self.transform.position
            self._camera_pos_sc = CubeSphereMap.get_cube_coord(self._camera_pos.x, self._camera_pos.y, self._camera_pos.z) 
            
            self._line.line_to(self._camera_pos)
            
            # Reset the number of splits
            self._num_splits = 0
            #print "Resetting splits"
            
            # If the camera has moved a sufficient distance to warrant an update
#            if self._last_camera_pos is None:
#                self._last_camera_pos = self._camera_pos
#            dist = self._last_camera_pos - self._camera_pos 
#            if dist.magnitude() > 1.0:
                
            # Calc the horizon
            altitude = self._camera_pos.magnitude()
            horizon_altitude = max([altitude-self.radius, self.max_height])
            self._horizon = math.sqrt(horizon_altitude * horizon_altitude + 2.0 * horizon_altitude * self._radius)
            
            # Update all of the sides of the cube/sphere
            for child in self.transform.children:
                if isinstance(child.node, SphereQuad):
                    child.node.update_surface()
                    
            self._last_camera_pos = self._camera_pos
                    
            self._last_time = datetime.now()
            
            # Update the UI with the camera pos
#            self._ui.rel_camera_pos = self._camera_pos
#            self._ui.camera_pos = self._camera_pos_sc

            if not self._camera_pos_sc is None:
                pos = CubeSphereMap.get_sphere_vector(self._camera_pos_sc.x, self._camera_pos_sc.y, self._camera_pos_sc.face)
                pos.normalize()
                pos *= (self._radius / 1.9)
                self._camera_gizmo.transform.position = pos
            
#        el = datetime.now() - start
#        print "Update Elapsed: %4.2f ms " % (el.microseconds / 1000)
            
    def cull(self, camera):
        # Override culling so that it doesn't interfere with the planet
        pass
            
    def draw(self):
        
#        start = datetime.now()
        
        self.renderer._setup_draw()
        
        for child in self.transform.children:
            if child.node:
                child.node.draw()
            
        self.renderer._teardown_draw()
        
#        el = datetime.now() - start
#        print "Draw Elapsed: %4.2f ms " % (el.microseconds / 1000) 
    
