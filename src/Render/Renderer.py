import pygame

from Core.Window import Window

from OpenGL.GL import *
from OpenGL.GLU import *

from Logging import Logger
from Geometry.euclid import Vector3

from Render.Projection import Projection 
from Scene.SceneManager import SceneManager
from Scene import NodeDrawGL

from Render.Font import *
from Render.Shader import *
from Render.ShaderManager import ShaderManager

from UI.UIManager import UIManager

import os

from Core import Time
# This file will contain the renderer class and sub-classes for each renderer mode.
#

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
		
	def Draw(self):
		pass
	
class GLRenderer(Renderer):
	
	def __init__(self):
		Renderer.__init__(self)
		self._meshes = []
		
		self._has_initialised = False
		self._projection = None
		self._camera = None
		self._print_font = None
		self._shader_manager = None
		self._ui_manager = None
		
		# Render Settings
		self._wireframe = False
		self._grid = False
		
		# For FPS Calc
		self._last_time = 0.0 
		
	def InitialiseDisplay(self, width, height, title):
		pygame.init()
		pygame.display.set_mode((width,height), pygame.OPENGL|pygame.DOUBLEBUF)
		pygame.display.set_caption(title)
		
		# If there isn't a camera set get the active camera from the SceneManager
		if self._camera is None:
			#self._camera = SceneManager.GetSceneManager().root.GetChildWithName('camera')
			self._camera = SceneManager.get_instance().active_camera
			
		self._ui_manager = UIManager.get_instance()
		
		# Create projection object
		self._projection = Projection(width, height)
		
		# Initialise OpenGL Display
		self.Setup3D()
		
		# Create the ShaderManager
		self._shader_manager = ShaderManager.get_instance()
		
		self._print_font = font_data("/Library/Fonts/Arial.ttf", 16)
		
		# Get the Scene Root
		self._scene_root = SceneManager.get_instance().root
		
		# Get the camera
		self._camera = self._scene_root.GetChildWithName("camera")
		
		# Indicate that the renderer has finished initialising
		self._has_initialised = True
	
	def Setup3D(self):
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
		
	def Teardown3D(self):
		glDisable(GL_CULL_FACE)
		
	def LoadMeshes(self, Nodes=[]):
		# Load the meshes from the Scene
		pass
		
	def DrawMeshes(self):
		# Set 3D Drawing settings
		self.Setup3D()
		
		#execute the camera's look at
		self._camera.LookAt()
		
		
		if self._grid:
			self.DrawGrid()
		
#		glLoadIdentity()
		
		# Draw the scene meshes here
		NodeDrawGL.DrawNode(self._scene_root)
		
		self.Teardown3D()
		#glEnd()
		
	def DrawGUI(self):
		
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		
		# Draw the UI - Later
		self._projection.SetScreen()
		self._camera.Reset()
		self._print_font.glPrint(5, 50, "Camera:")
		self._print_font.glPrint(5, 35, "Pos: %s" % str(self._camera.position))
		self._print_font.glPrint(5, 20, "Ori: %s" % str(self._camera.rotation))
#		fps = ((1/Time.deltaTime))
		fps = 1 / (Time.delta_time * 0.9) + (self._last_time * 0.1)
		self._last_time = Time.delta_time
		
		#self._print_font.glPrint(5, 5, "FPS: %.2f" % fps) 
		self._print_font.glPrint(5, 5, "FPS: %.2f" % Time.Time.get_instance().get_fps())
		
		self._ui_manager.draw()
		
	def DrawGrid(self):
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
		
		
	def Draw(self):
		
		if not self._has_initialised:
			Logger.Log("RENDER ERROR: Render hasn't been initialised")
			return
				
		# Set Projection
		self._projection.SetPerspective(45)
		
		# Point the camera at the origin
		#self._camera.LookAt(Vector3())
		
		# Draw the Scene Meshes
		self.DrawMeshes()
#		glFlush()
		
		self.DrawGUI()
				
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
		