
import os

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.core.settings import Settings

from epsilon.core.window import Window
from epsilon.logging.logger import Logger
from epsilon.geometry.euclid import Vector3

#from epsilon.render.projection import Projection 
from epsilon.scene.scenemanager import SceneManager

from epsilon.render.frustum import Frustum

from epsilon.render.gizmos.gizmomanager import GizmoManager

#from epsilon.render import Font
from epsilon.render.shader import *
from epsilon.render.shadermanager import ShaderManager

from epsilon.render.colour import Preset

from epsilon.render.renderevents import RenderListener
from epsilon.render.rendersettings import RenderSettings

from epsilon.ui.uimanager import UIManager

# This file will contain the renderer class and sub-classes for each renderer mode.
#

class RendererUninitialisedException(Exception): pass

class WindowRenderer(Window):
    
    def __init__(self):
        Window.__init__(self)
        
        self._camera = None
        self._projection = None
    
    @property
    def camera(self):
        return self._camera
            
    @camera.setter
    def camera(self, new_cam):
        self._camera = new_cam
        
    @property
    def projection(self):
        return self._projection
    
    @projection.setter
    def projection(self, new_proj):
        self._projection = new_proj
    
class GLWindowRenderer(WindowRenderer):
    
    def __init__(self):
        WindowRenderer.__init__(self)
        self._meshes = []
        
        self._has_initialised = False
        self._camera = None
        self._scene_root = None
        self._print_font = None
        self._shader_manager = None
        self._ui_manager = None
        
        # Render Settings
        self._rendersettings = RenderSettings.get_instance()

        if not Settings.has_option('RenderSettings','wireframe'):
            Settings.set('RenderSettings','wireframe', False)

        if not Settings.has_option('RenderSettings','grid'):
            Settings.set('RenderSettings','grid', False)

        if not Settings.has_option('RenderSettings','draw_bounds'):
            Settings.set('RenderSettings','draw_bounds', False)
        
        # Render Listener to allow access to settings
        self._listener = RenderListener(self)
        
        # For FPS Calc
        self._last_time = 0.0
        
        self._fatal_error_displayed = False
        
        # Back Colour
        self._back_colour = Preset.lightgrey

        # Nodes queued for rendering.
        self._render_queue = []
        
    def init(self, width, height, title):
        WindowRenderer.init(self, width, height, title)
        
        self._ui_manager = UIManager.get_instance()
        
        # Create the ShaderManager
        self._shader_manager = ShaderManager.get_instance()
        
        # Get the GizmoManager
        self._gizmo_manager = GizmoManager.get_instance()
        
        # Initialise OpenGL Display and set the indicator for initialisation completion
        self._has_initialised = self.setup_3d()
    
    def setup_3d(self):
        
        setup_ok = False
        
        # Configure OpenGL Settings for drawing 3D
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        
        glShadeModel(GL_SMOOTH)
        
        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)
                
        glClearColor(*self._back_colour.get_gl_colour())
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        if Settings.get('RenderSettings','wireframe'):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # If the SceneManager instance hasn't been set
        if self._camera is None and self._scene_root is None:
            if not SceneManager.get_current_scene() is None:
                # If there isn't a camera set, get the active camera from the SceneManager
                if self._camera is None:
                    self._camera = SceneManager.get_current_scene().active_camera
                
                # Get the Scene Root
                if self._scene_root is None:    
                    self._scene_root = SceneManager.get_current_scene().root
        
        setup_ok = False
        if self._camera is None:
            Logger.Log("RENDER ERROR: Camera not found.")
        elif self._scene_root is None:
            Logger.Log("RENDER ERROR: Scene Root not found.")
        else:
            setup_ok = True
            
            # Activate the camera for rendering
            # set_projection, etc
            self._camera.activate()
        
        return setup_ok            
        
    def teardown_3d(self):
        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
                
    def draw_nodes(self):
            
        #execute the camera's look at
        self._camera.look_at()
        
        # Draw the nodes in the render queue
        for node in self._render_queue:

            # if the node has a custom draw function
            if 'draw' in dir(node):
                node.draw()

            # otherwise use the default daw function
            else:
                self._perform_draw(node)

        # Clear the render queue
        self._render_queue = []
            
    def _perform_draw(self, node):
        if not node.renderer.culled:
            
            # Draw this Node
            if not node.renderer is None:
                node.renderer.draw()
        
    def draw_gui(self):
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # Draw the UI - Later
        self._camera.set_screen()
        self._camera.reset()
        
        self._ui_manager.draw()
        
    def draw_gizmos(self):
        
        if Settings.get('RenderSettings','grid'):
            self.draw_grid()

        # Gizmos are always on top
        glDisable(GL_DEPTH_TEST)

        gizmos = self._gizmo_manager.get_gizmo_root().transform.children
        for gizmo in gizmos:
            self._perform_draw_gizmos(gizmo.node)

        glEnable(GL_DEPTH_TEST)

    def _perform_draw_gizmos(self, gizmo):
        
        # Draw this Node
        if not gizmo.renderer is None:
            gizmo.renderer.draw()
    
    def draw_grid(self):
        # Simple Grid for the time being
        columns = 50
        rows = 50
        
        glBegin(GL_LINES)
        
        # Horizontal lines.
        glColor3f(0.0,0.0,0.0)
        for i in range((-rows/2), (rows/2)):
            if i == 0.0:
                glColor3f(1.0,0.0,0.0)
            glVertex3f(-(columns/2), 0, i)
            glVertex3f((columns/2), 0, i)
            if i == 0.0:
                glColor3f(0.0,0.0,0.0)
        
        # Vertical lines.
        for i in range((-columns/2), (columns/2)):
            if i == 0.0:
                glColor3f(0.0,0.0,1.0)
            
            glVertex3f(i, 0, -(rows/2))
            glVertex3f(i, 0, (rows/2))
            
            if i == 0.0:
                glColor3f(0.0,0.0,0.0)
        glEnd()
        glColor3f(1.0,1.0,1.0)
        
        
    def draw(self):
        
        # Make another attempt at initialising the 3D now that all of the 
        # other Managers have initialised, and should have loaded their content
        if not self.setup_3d():
            if not self._fatal_error_displayed:
                message = "RENDER ERROR: Render hasn't been initialised"
                Logger.Log(message)
                self._fatal_error_displayed = True
                raise RendererUninitialisedException(message)
        
        # Draw the Scene Meshes
        self.draw_nodes()
        self.draw_gizmos()
        self.teardown_3d()
        
        self.draw_gui()

    # Perform culling on scene
    def cull(self):
        if self._scene_root is not None:
            self._perform_cull(self._scene_root)

    def _perform_cull(self, node):
                        
        # Check if the node has a custom culling function let it cull itself
        if 'cull' in dir(node):
            self._render_queue += node.cull(self._camera)

        # Else check if the node is within the camera frustum.
        elif not node.transform.bounds.is_empty:
            node.renderer.culled = self._camera.bounds_inside(node.transform.bounds) == Frustum.OUTSIDE
            
            # If this node isn't culled
            if not node.renderer.culled:

                # Add this node to the render queue.
                self._render_queue.append(node)

                for child in node.transform.children:
                    self._perform_cull(child.node)

    @property
    def wireframe(self):
        return self._wireframe
    
    @wireframe.setter
    def wireframe(self, set_wire):
        self._wireframe = set_wire
        
    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self, new_grid):
        self._grid = new_grid
        