
import os

from Core.Window import Window

from OpenGL.GL import *
from OpenGL.GLU import *

from Logging import Logger
from Geometry.euclid import Vector3

from Render.Light import GLLight

from Render.Projection import Projection 
from Scene.SceneManager import SceneManager
from Scene import NodeDrawGL

from Render import Font
from Render.Shader import *
from Render.ShaderManager import ShaderManager

from UI.UIManager import UIManager

from Core import Time

matrix_type = GLfloat * 16
matrix_typed = GLdouble * 16

# This file will contain the renderer class and sub-classes for each renderer mode.
#

class RendererUninitialisedException(Exception): pass

class Renderer(Window):
	
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
	
class GLRenderer(Renderer):
	
	def __init__(self):
		Renderer.__init__(self)
		self._meshes = []
		
		self._has_initialised = False
		self._projection = None
		self._camera = None
		self._scene_root = None
		self._print_font = None
		self._shader_manager = None
		self._ui_manager = None
		
		# Render Settings
		self._wireframe = False
		self._grid = False
		
		# For FPS Calc
		self._last_time = 0.0
		
		self._fatal_error_displayed = False 
		
	def init(self, width, height, title):
		Renderer.init(self, width, height, title)
		
		#self._ui_manager = UIManager.get_instance()
		
		# Create projection object
		self._projection = Projection(width, height)
		
		# Create the ShaderManager
		self._shader_manager = ShaderManager.get_instance()
		
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
		
#		glEnable(GL_LIGHTING)
#		glEnable(GL_LIGHT0)
		
#		glEnable(GL_LIGHT1)
		glShadeModel(GL_SMOOTH)
		
		glCullFace(GL_BACK)
		glEnable(GL_CULL_FACE)
				
		# Clear to Light Blue
		glClearColor(180/255, 218/255, 1.0, 1.0)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		if self._wireframe:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		else:
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		
		# If the SceneManager instance hasn't been set
		if not SceneManager.get_instance().current_scene is None:
			# If there isn't a camera set get the active camera from the SceneManager
			if self._camera is None:
				self._camera = SceneManager.get_instance().current_scene.active_camera
			
			# Get the Scene Root
			if self._scene_root is None:	
				self._scene_root = SceneManager.get_instance().current_scene.root
		
		if self._camera is None:
			setup_ok = False
			Logger.Log("RENDER ERROR: Camera not found.")
		elif self._scene_root is None:
			setup_ok = False
			Logger.Log("RENDER ERROR: Scene Root not found.")
		else:
			setup_ok = True
		
		return setup_ok			
		
	def teardown_3d(self):
		glDisable(GL_CULL_FACE)
		
	def load_meshes(self, Nodes=[]):
		# Load the meshes from the Scene
		pass
		
	def draw_meshes(self):
		# Set 3D Drawing settings
		if self.setup_3d():
			
			#execute the camera's look at
			self._camera.LookAt()
			
			if self._grid:
				self.draw_grid()
			
	#		glLoadIdentity()
			
			# Draw the scene meshes here
			self.draw_node(self._scene_root)
			
			self.teardown_3d()
			#glEnd()
			
	def draw_node(self, node):
		
		if node.visible:
		
			glPushMatrix()
			
			# Translate    
			glTranslate(*node.position)
			
			# Rotate
			glMultMatrixf(matrix_type(*node.rotation.get_matrix()))
			
			# Scale
			glScalef(*node.local_scale)
			
			
			# Draw Light
			#        if node.light:
			#            node.light.Draw()
			
			# Set Material
			# Every node _must_ have a material from now on.
			# The renderer is moving to entirely Shader based rendering and
			# as such all meshes cannot be rendered without a material 
			# definition
			
			if node.mesh and node.material:
				node.material.draw(node.mesh.glmesh)
			
			if isinstance(node, GLLight):
				node.draw()
			#        if node.material:
			#            node.material.SetupMaterial()
			#        
			#        # Draw Mesh
			#        if node.mesh:
			#            if node.mesh.glmesh:
			#                node.mesh.glmesh.Draw()
			#                
			#        if node.material:
			#            node.material.UnsetMaterial()
			
			# Draw Children    
			for child in node.children:
				self.draw_node(child)
			
			# Pop the Transform stack
			glPopMatrix()
			
		
	def draw_gui(self):
		
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		
		# Draw the UI - Later
		self._projection.set_screen()
		self._camera.Reset()
		
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
		
#		self._ui_manager.draw()
		
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
		
		
	def draw(self):
		
		# Make another attempt at initialising the 3D now that all of the 
		# other Managers have initialised, and should have loaded their content
		if not self.setup_3d():
			if not self._fatal_error_displayed:
				message = "RENDER ERROR: Render hasn't been initialised"
				Logger.Log(message)
				self._fatal_error_displayed = True
				raise RendererUninitialisedException(message)
				
		# Set Projection
		self._projection.set_perspective(45)
		
		# Point the camera at the origin
		#self._camera.LookAt(Vector3())
		
		# Draw the Scene Meshes
		self.draw_meshes()
#		glFlush()
		
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
		