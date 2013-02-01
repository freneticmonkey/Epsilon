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

from epsilon.environment.planet.spheresurface import SphereSurface

#from epsilon.geometry.cperlin import Perlin, FractalNoise
from epsilon.geometry.cperlin import Perlin, FractalNoise

from noise import pnoise3, snoise3

from epsilon.render.colour import Preset


from epsilon.render.texture import GeneratedTexture
from epsilon.render.meshfactory import Parametric
from pyglet.gl import *
from pyglet.image import ImageData
import numpy
from epsilon.render.renderer import Renderer

from epsilon.render.texturemanager import TextureManager

class PlanetSphereDebugWindow(UIBaseWindow):
    def _setup_ui(self):
        self._dialog = Dialogue('Planet Sphere Debug',
                                x=800,
                                y=550,
                                content=
                                VLayout(hpadding=5, 
                                        children=
                                        [
                                         Checkbox('Planet camera', action=self.planet_camera_action, value=False),
                                         Checkbox('Track camera', action=self.track_camera_action, value=True),
                                        ])
                                )
        self._frame.add(self._dialog)
        
        self._track_camera = True

        self._planet_camera = False
    
    @property
    def planet_camera(self):
        return self._planet_camera
        
    def planet_camera_action(self, checkbox):
        self._planet_camera = checkbox.value

    @property
    def track_camera(self):
        return self._track_camera
        
    def track_camera_action(self, checkbox):
        self._track_camera = checkbox.value
        
class PlanetSphere(Node):
    def __init__(self, pos=Vector3(0,0,0), radius=150.0, density=16): #6.328
        Node.__init__(self)
        
        self._name = "planet_root"

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
        
        # The maximum height of the sphere surface (above the radius)
        self._max_height = (radius * 0.05) #0.02
        self._split_factor = 1.1  #16
        self._split_power = 1.1 #1.25
        
        self._horizon = 0
        
        self._ui = PlanetSphereDebugWindow()
        
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
        
        self._generator = SphereSurface(self._density, self._radius, self._max_height)

        # Create the faces of the planet
        self._gen_faces()

        # Generate a texture for the plane
        root_trans = SceneManager.get_instance().current_scene.root.transform
        test_plane = root_trans.get_child_with_name("test_plane", True).node
        test_plane.renderer.material.texture = self._generator.get_texture("B", 128)

        # test_plane = root_trans.get_child_with_name("test_plane_right", True).node
        # test_plane.renderer.material.texture = self._generator.get_texture("R", 128)

        # test_plane = root_trans.get_child_with_name("test_plane_left", True).node
        # test_plane.renderer.material.texture = self._generator.get_texture("L", 128)

        # test_plane = root_trans.get_child_with_name("test_plane_front", True).node
        # test_plane.renderer.material.texture = self._generator.get_texture("F", 128)

    @property
    def name(self):
        return self._name

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

    @property
    def generator(self):
        return self._generator
    
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
        self._top =     SphereQuad('T', self, self, radius=self._radius, density=self._density, face=CubeSphereMap.TOP)
        self._bottom =  SphereQuad('U', self, self, radius=self._radius, density=self._density, face=CubeSphereMap.BOTTOM)
        self._front =   SphereQuad('F', self, self, radius=self._radius, density=self._density, face=CubeSphereMap.FRONT)
        self._back =    SphereQuad('B', self, self, radius=self._radius, density=self._density, face=CubeSphereMap.BACK)
        self._left =    SphereQuad('L', self, self, radius=self._radius, density=self._density, face=CubeSphereMap.LEFT)
        self._right =   SphereQuad('R', self, self, radius=self._radius, density=self._density, face=CubeSphereMap.RIGHT)
        
        self.transform.add_child(self._top.transform)
        self.transform.add_child(self._bottom.transform)
        self.transform.add_child(self._front.transform)
        self.transform.add_child(self._back.transform)
        self.transform.add_child(self._left.transform)
        self.transform.add_child(self._right.transform)
        
        self._top._init_quad()
        self._bottom._init_quad()
        self._front._init_quad()
        self._back._init_quad()
        self._left._init_quad()
        self._right._init_quad()

    def update_sphere(self):
        
#        start = datetime.now()
        
        if (datetime.now() - self._last_time).total_seconds() > 0.1:
        
            if self._ui.track_camera:
            
                if self._camera is None:
                    self._camera = SceneManager.get_instance().current_scene.active_camera

                # Store the camera pos for access by the quad children
                self._camera_pos = self._camera.node_parent.transform.position - self.transform.position

                self._camera_pos_sc = CubeSphereMap.get_cube_coord(self._camera_pos.x, self._camera_pos.y, self._camera_pos.z) 
                
                self._line.line_to(self._camera_pos)


                if self._ui.planet_camera:
                    # Check if the camera has intersected the planet.
                    if self._camera_pos.magnitude() < (self._radius + self._max_height):
                        u = self._camera_pos_sc.x
                        v = self._camera_pos_sc.y
                        face = self._camera_pos_sc.face
                        self._camera.node_parent.transform.position = CubeSphereMap.get_sphere_position(u, v, face, (self._radius + self._max_height))

                
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
                
                if True:
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

        # debug draw - gen texture

        # self._planet_texture._pyglet_image.blit(256, 256)
        
#        el = datetime.now() - start
#        print "Draw Elapsed: %4.2f ms " % (el.microseconds / 1000) 
    
