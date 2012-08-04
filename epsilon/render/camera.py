from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.events.eventbase import EventBase
from epsilon.geometry.euclid import Vector3
from epsilon.render.frustum import Frustum

from epsilon.scene.node import Node

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

class CameraBase(Frustum):
	def __init__(self):
		Frustum.__init__(self)

class CameraGL(CameraBase):
	def __init__(self):
		CameraBase.__init__(self)
		self._look_at_pos = Vector3()
		self._active = False
		
	def on_add(self):
		if not self.node_parent.transform.scene is None:
			print "adding camera"
			self.node_parent.transform.scene.add_camera(self)
		else:
			print "failed setting camera"
		# Send event notifying the SceneManager that a camera has been added to the scene
		#CameraAddedEvent(self).Send()
	
	def on_remove(self):
		if not self.node_parent.transform.scene is None:
			self.node_parent.transform.scene.remove_camera(self)
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
	def look_at_position(self):
		return self._look_at_pos
	
	@look_at_position.setter
	def look_at_position(self, new_la_pos):
		self._look_at_pos = new_la_pos
		
	def activate(self):
		self.set_perspective()
	
	def reset(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
	def look_at(self):
		self.reset()
		p = self.node_parent.transform.position
		self.reset()
		lookat = self._look_at_pos
		gluLookAt(p.x, p.y, p.z, lookat.x, lookat.y, lookat.z, 0, 1, 0 )
			
class Camera(Node):
	def __init__(self):
		Node.__init__(self, name="default_camera", camera=CameraGL(), renderer=None)
		
	