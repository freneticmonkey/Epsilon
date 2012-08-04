"""

	Note: The Transform code has been ported from OGRE www.ogre3d.org

"""

from OpenGL.GL import *
from OpenGL.GLU import *

from epsilon.scripting.scriptmanager import ScriptManager

#from epsilon.render.meshfactory import *
from epsilon.render.frustum import Frustum
from epsilon.render.renderer import Renderer
from epsilon.render.transform import Transform

from epsilon.scripting.scriptmanager import ScriptManager

class Node(object):
	
	_next_id = 0
	
	@classmethod
	def get_id(cls):
		cls._next_id += 1
		return cls._next_id
	
	def __init__(self, name=None, light=None, camera=None, renderer=None):
		
		# Node Properties
		self._id = Node.get_id()
		
		# Generate a name if one has not been supplied
		if not name:
			name = "Node_" + str(self._id)
		
		self._name = name
		
		# Nodes will _always_ have a transform
		self._transform = Transform(self)
		
		# This allows for Nodes to be initialised without a renderer component
		if renderer is None:
			renderer = Renderer()
		
		self._renderer = None
		if not renderer is None:
			self._renderer = self._set_component(self._renderer, renderer)
		
		self._light = None
		if not light is None:
			self._light = self._set_component(self._light, light)
			
		self._camera = None
		if not camera is None:
			self._camera = self._set_component(self._camera, camera)
		
		self._scripts = []
		
	# If deleted
	def __del__(self):
		# Kill any scripts
		for script in self._scripts:
			ScriptManager.get_instance().remove_script(script)
			
	def __repr__(self):
		return "Id: " + str(self._id) + " Name: " + self._name
	
	# Node Property access
	@property
	def node_id(self):
		return self._id
	
	@property
	def name(self):
		return self._name
	
	@name.setter
	def name(self, new_name):
		self._name = new_name
	
	@property
	def light(self):
		return self._light
	
	@light.setter
	def light(self, new_light):
		self._light = self._set_component(self._light, new_light)
		
	@property
	def camera(self):
		return self._camera
	
	@camera.setter
	def camera(self, new_cam):
		self._camera = self._set_component(self._camera, new_cam)
	
	@property
	def renderer(self):
		return self._renderer
	
	@property
	def transform(self):
		return self._transform
	
	def _set_component(self, local_var, new_value):
		if not local_var is None:
			local_var.node_parent = None
			local_var.on_remove()
		
		if not new_value is None:
			local_var = new_value
			local_var.node_parent = self
			local_var.on_add()
			
		return local_var
	
	def _components_on_add(self):
		if not self._renderer is None:
			self._renderer.on_add()
		if not self._light is None:
			self._light.on_add()
		if not self._camera is None:
			self._camera.on_add()
		
	def _components_on_remove(self):
		if not self._renderer is None:
			self._renderer.on_remove()
		if not self._light is None:
			self._light.on_remove()
		if not self._camera is None:
			self._camera.on_remove()
		
	# Script Handling
	def add_script(self, new_script):
		new_script.node = self
		self._scripts.append(new_script)
	
	def remove_script(self, name='', rm_script=None):
		if len(name) == 0:
			name = rm_script.name
		
		for script in self._scripts:
			if len(name) > 0 and script.name == name:
				script.node = None
				self._scripts.remove(script)
				break
			
	def cull(self, camera):
		self.renderer.culled = camera.bounds_inside(self.transform.bounds) == Frustum.OUTSIDE
			
		if not self.renderer.culled:
			for child in self.transform.children:
				child.node.cull(camera)
#		else:
#			print "Culled: " + self.name
		
	def draw(self):
		if not self.renderer.culled:
			
			# Draw this Node
			if not self.renderer is None:
				self.renderer.draw()
				
			# Draw Children    
			for child in self.transform.children:
			    if not child.node is None:
			    	child.node.draw()
		    	
	def on_add(self):
		self._components_on_add()
		
	def on_remove(self):
		self._components_on_remove()
    		
## Primitive Objects
#class Plane(Node):
#	def __init__(self, name=None):
#		Node.__init__(self, name=name)
#		self.renderer.mesh = MeshFactory.get_mesh(MeshTypes.PLANE_HI)
#		
#class Cube(Node):
#	def __init__(self, name=None):
#		Node.__init__(self, name=name)
#		self.renderer.mesh = MeshFactory.get_mesh(MeshTypes.CUBE)
#		
#class Sphere(Node):
#	def __init__(self, name=None):
#		Node.__init__(self, name=name)
#		self.renderer.mesh = MeshFactory.get_mesh(MeshTypes.SPHERE)
#		
#class Octo(Node):
#	def __init__(self, name=None):
#		Node.__init__(self, name=name)
#		self.renderer.mesh = MeshFactory.get_mesh(MeshTypes.OCTOHEDRON)
#		
#class Light(Node):
#	def __init__(self, name=None):
#		Node.__init__(self, name=name)
#		self.light = GLLight()




	