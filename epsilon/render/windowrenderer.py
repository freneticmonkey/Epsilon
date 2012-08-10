
import os

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.core.window import Window
from epsilon.logging.logger import Logger
from epsilon.geometry.euclid import Vector3

#from epsilon.render.light import GLLight

#from epsilon.render.projection import Projection 
from epsilon.scene.scenemanager import SceneManager

from epsilon.render.gizmos.gizmomanager import GizmoManager

#from epsilon.render import Font
from epsilon.render.shader import *
from epsilon.render.shadermanager import ShaderManager

from epsilon.render.colour import Preset

from epsilon.render.renderevents import RenderListener

from epsilon.ui.uimanager import UIManager

#from epsilon.core.time import Time

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
		#self._projection = None
		self._camera = None
		self._scene_root = None
		self._print_font = None
		self._shader_manager = None
		self._ui_manager = None
		
		# Render Settings
		self._wireframe = False
		self._grid = True
		
		# Render Listener to allow access to settings
		self._listener = RenderListener(self)
		
		# For FPS Calc
		self._last_time = 0.0
		
		self._fatal_error_displayed = False
		
		# Back Colour
		self._back_colour = Preset.grey
		
	def init(self, width, height, title):
		WindowRenderer.init(self, width, height, title)
		
		self._ui_manager = UIManager.get_instance()
		
		# Create projection object
		#self._projection = Projection(width, height)
		
		# Create the ShaderManager
		self._shader_manager = ShaderManager.get_instance()
		
		# Get the GizmoManager
		self._gizmo_manager = GizmoManager.get_instance()
		
		#self._print_font = Font.font_data("/Library/Fonts/Arial.ttf", 16)
		
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
		
		if self._wireframe:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		else:
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		
		# If the SceneManager instance hasn't been set
		if not SceneManager.get_instance().current_scene is None:
			# If there isn't a camera set, get the active camera from the SceneManager
			if self._camera is None:
				self._camera = SceneManager.get_instance().current_scene.active_camera
			
			# Get the Scene Root
			if self._scene_root is None:	
				self._scene_root = SceneManager.get_instance().current_scene.root
		
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
		
	def load_meshes(self, Nodes=[]):
		# Load the meshes from the Scene
		pass
		
	def draw_meshes(self):
		# Set 3D Drawing settings
		if self.setup_3d():
			
			#execute the camera's look at
			self._camera.look_at()
			
			if self._grid:
				self.draw_grid()
			
			# Draw the scene meshes here
			self.draw_node(self._scene_root)
			
			self._gizmo_manager.draw()

			self.teardown_3d()
			#glEnd()
			
	def draw_node(self, node):
		
		#glDisable(GL_DEPTH_TEST)
		
		node.draw()
			
		
	def draw_gui(self):
		
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		
		# Draw the UI - Later
		self._camera.set_screen()
		self._camera.reset()
		
#		glColor3f(1.0,1.0,1.0)
#		self._print_font.glPrint(5, 50, "Camera:")
#		self._print_font.glPrint(5, 35, "Pos: %s" % str(self._camera.position))
#		self._print_font.glPrint(5, 20, "Ori: %s" % str(self._camera.rotation))
##		fps = ((1/Time.deltaTime))
#		fps = 1 / (Time.delta_time * 0.9) + (self._last_time * 0.1)
#		self._last_time = Time.delta_time
#		
#		#self._print_font.glPrint(5, 5, "FPS: %.2f" % fps) 
#		self._print_font.glPrint(5, 5, "FPS: %.2f" % Time.Time.get_instance().get_fps())
		
		self._ui_manager.draw()
		
	def draw_gizmos(self):
		pass
		self._gizmo_manager.draw()
	
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
		
		# Point the camera at the origin
		#self._camera.LookAt(Vector3())
		
		# Draw the Scene Meshes
		self.draw_meshes()
#		glFlush()
		
		self.draw_gizmos()
		
		self.draw_gui()
				
		#self._flip()
		
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
		