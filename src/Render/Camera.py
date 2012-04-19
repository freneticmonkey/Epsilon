from OpenGL.GL import *
from OpenGL.GLU import *

from Geometry.euclid import Vector3
from Scene.Node import Node
from Events.EventBase import EventBase

# Camera Events
class CameraAddedEvent(EventBase):
	def __init__(self, camera):
		EventBase.__init__(self, "CameraAdded", camera)
		
class CameraRemovedEvent(EventBase):
	def __init__(self, camera):
		EventBase.__init__(self, "CameraRemoved", camera)
		
class CameraSetActive(EventBase):
	def __init__(self, camera):
		EventBase.__init__(self, "SetActiveCamera", camera)

class CameraBase(Node):
	def __init__(self):
		Node.__init__(self)

class CameraGL(CameraBase):
	def __init__(self):
		CameraBase.__init__(self)
		self._name = "camera"
		self._look_at_pos = Vector3()
		self._active = False
		
	def on_add(self):
		if not self._scene is None:
			self._scene.add_camera(self)
		# Send event notifying the SceneManager that a camera has been added to the scene
		#CameraAddedEvent(self).Send()
	
	def on_remove(self):
		if not self._scene is None:
			self._scene.remove_camera(self)
		# Send event notifying the SceneManager that a camera has been remove from the scene
		#CameraRemovedEvent(self).Send()
		
	@property
	def active(self):
		return self._active
	
	# Note this should only be called by the SceneManager
	@active.setter
	def active(self, active_state):
		self._active = active_state
		
	@property
	def look_at(self):
		return self._look_at_pos
	
	@look_at.setter
	def look_at(self, new_la_pos):
		self._look_at_pos = new_la_pos
	
	def Reset(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
	def LookAt(self):
		self.Reset()
		p = self.position
		self.Reset()
		lookat = self._look_at_pos
		gluLookAt(p.x, p.y, p.z, lookat.x, lookat.y, lookat.z, 0, 1, 0 )
			
		
		
	