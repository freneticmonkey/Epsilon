"""

	Note: The Transform code has been ported from OGRE www.ogre3d.org

"""
from Scripting.ScriptManager import ScriptManager

from Geometry.euclid import Vector3, Quaternion, Matrix4
from Scripting.ScriptManager import ScriptManager
from Render.MeshFactory import *
from Render.Material import GLMaterial

class Space:
	SELF = 0
	WORLD = 1
	PARENT = 2

class Node(object):
	
	_next_id = 0
	
	@classmethod
	def get_id(cls):
		cls._next_id += 1
		return cls._next_id
	
	def __init__(self, name=None, pos=None, rot=None, scale=None, parent=None, scene=None):
		
		# Node Properties
		self._id = Node.get_id()
		
		# Generate a name if one has not been supplied
		if not name:
			name = "Node_" + str(self._id)
		
		self._name = name
		self._mesh = None
		self._material = None
		self._light = None
		self._visible = True
		self._scripts = []
		
		# The scene that the node is in
		self._scene = scene
		
		# Transform Related properties
		self._children = []
		
		# Set default transform properties
		if not pos:
			pos = Vector3()
		if not rot:
			rot = Quaternion()
		if not scale:
			scale = Vector3(1,1,1)
			
		# World positions
		self._world_position = pos
		self._world_rotation = rot
		self._world_scale = scale
		
		# position relative to parent
		self._local_position = pos
		self._local_rotation = rot
		self._local_scale = scale
		
		self._inherit_rotation = True
		self._inherit_scale = True
		
		self._parent = parent
		# Properties to control hierarchy updates
		self._children_to_update = []
		self._need_parent_update = False
		self._need_child_update = False
		self._parent_notified = False
		self._force_parent_update = False		
		
		
		self._forward = Vector3(0,0,1)
		self._up = Vector3(0,1,0)
		self._right = Vector3(1,0,0)
				
		# Bounds?
		
		# Setup Default Material
#		self._material = GLMaterial()
#		self._material.shader = "phong"
		
		# No default texture for now		
	
	# If deleted
	def __del__(self):
		# Kill any scripts
		for script in self._scripts:
			ScriptManager.get_instance().remove_script(script)
		
		# Detach any children
		for child in self._children:
			# TODO: HMMM - Re-attach the nodes to the scene Root rather than just leaving them dangling??
			child._parent = None
			
		self._children_to_update = []
			
	def __repr__(self):
		return "Id: " + str(self._id) + " Name: " + self._name
	
	# Node Property access
	
	@property
	def node_id(self):
		return self._id
	
	@property
	def name(self):
		return self._name
		
	@property
	def mesh(self):
		return self._mesh
	
	@mesh.setter
	def mesh(self, new_mesh):
		self._mesh = new_mesh
		# If a mesh has been set 
		# Set a default material
		if self._material is None:
			self._material = GLMaterial()
	
	@property
	def material(self):
		return self._material
	
	@material.setter
	def material(self, new_mat):
		self._material = new_mat
	
	@property
	def light(self):
		return self._light
	
	@light.setter
	def light(self, new_light):
		new_light.parent = self
		self._light = new_light
	
	@property
	def visible(self):
		return self._visible
	
	@visible.setter
	def visible(self, vis):
		self._visible = vis
		for child in self._children:
			child.visible = vis
	
	@property
	def children(self):
		return self._children
	
	@property
	def scene(self):
		return self._scene
	
	@property
	def need_update(self):
		if self._need_child_update or \
           self._need_parent_update or \
           len(self._children_to_update) > 0:
			return True
		else:
			return False
	
	# Node Functions
	
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
	
	# Child Node handling
	def add_child(self, child_node):
		if isinstance(child_node, Node):
			child_node._parent = self
			child_node._scene = self._scene
			self._children.append(child_node)
			# Allow the child to perform any post addition actions
			child_node.on_add()
			# Notify the parent that we have changed
			self._need_update(True)
		else:
			print "Error: child parameter is not a Node instance"
			
	def remove_child(self, child_node):
		if isinstance(child_node, Node):
			if child_node in self._children:
				child_node._parent = None
				self._children.remove(child_node)
				
				# Allow the former child to perform any post removal actions
				child_node.on_remove()
				
				# Notify the parent that we have changed
				self._need_update(True)
		else:
			print "Error: Child is not a Node instance"
	
	# In future this could be recursive			
	def get_child_with_id(self, id, recursive=False):
		ret_child = None
		for child in self._children:
			if child.node_id == id:
				ret_child = child
				break
		# Breadth first recursive search
		if recursive and not ret_child:
			for child in self._children:
				ret_child = child.get_child_with_id(id, recursive)
				if not ret_child is None:
					break
		return ret_child
	
	def get_child_with_name(self, name, recursive=False):
		ret_child = None
		for child in self._children:
			if child.name == name:
				ret_child = child
				break
		# Breadth first recursive search
		if recursive and not ret_child:
			for child in self._children:
				ret_child = child.get_child_with_name(name, recursive)
				if not ret_child is None:
					break
		return ret_child
	
	def get_child_with_type(self, class_type, recursive=False):
		ret_child = None
		for child in self._children:
			if child.__class__.__name__ == class_type:
				ret_child = child
				break
		# Breadth first recursive search
		if recursive and not ret_child:
			for child in self._children:
				ret_child = child.get_child_with_type(class_type, recursive)
				if not ret_child is None:
					break
		return ret_child
	
	# This function is called whenever the node is added as a child to another node
	def on_add(self):
		pass
	
	# This function is called whenever the node is removed as a child from another node
	def on_remove(self):
		pass
	
	# Update the Node and it's children's transforms
	def _update(self, update_children, parent_has_changed):
		
		# Always clear information about parent notification
		self._parent_notified = False
		
		# If there is no reason to continue updating stop.
		if not update_children and \
		   not self._need_parent_update and \
		   not self._need_child_update and \
		   not parent_has_changed:
			return
		
		# See if we should update the transform
		if self._need_parent_update or parent_has_changed:
			# Update transforms from parent
			self._update_from_parent()
		
		# Update the children of the node
		if self._need_child_update or parent_has_changed:
			for child_node in self._children:
				child_node._update(True,True)
			
			self._children_to_update = []
		else:
			# Update only the children that have requested updates
			for id in self._children_to_update:
				for child_node in self._children:
					if id == child_node.node_id:
						child_node._update(True,False)
						break
			self._children_to_update = []
		
		self._need_child_update = False
			
			
	# Called from parent node.  Updates transform properties and any child transform properties
	def _update_from_parent(self):
		
		if self._parent:
			# update rotation
			parent_rotation = self._parent.world_rotation
			if self._inherit_rotation:
				# Combine rotation with parent rotation
				self._world_rotation = parent_rotation * self._local_rotation
			else:
				self._world_rotation = self._local_rotation
			
			# update scale
			parent_scale = self._parent.world_scale
			if self._inherit_scale:
				# Scale own position by parent scale
				self._world_scale = parent_scale * self._local_scale
			else:
				self._world_scale = self._local_scale
			
			# Change position vector based on parent's rotation and scale
			self._world_position = parent_rotation * (parent_scale * self._local_position)
			
			# Add altered position vector to parent's position
			self._world_position += self._parent.world_position
		else:
			# This is the root node.
			self._world_position = self._local_position
			self._world_rotation = self._local_rotation
			self._world_scale    = self._local_scale
			
		self._need_parent_update = False
			
	# tell parent that this node needs an update
	def _need_update(self, force_parent_update=False):
		self._need_parent_update = True
		self._need_child_update  = True
		
		# if this not is not the root and the parent hasn't already been notified
		if self._parent and ( not self._parent_notified or self._force_parent_update):
			self._parent.request_update(self.node_id, force_parent_update)
			self._parent_notified = True
		
		# All children will be updated
		self._children_to_update = []
		
	# Request for the parent to update it's children
	def request_update(self, child_node_id, force_parent_update=False):
		# If we are already going to update everything then this doesn't matter
		if self._need_child_update:
			return
		
		self._children_to_update.append(child_node_id)
		# Request selective update of this node, if it hasn't already been done
		if self._parent and (not self._parent_notified or self._force_parent_update):
			self._parent.request_update(self.node_id, force_parent_update)
			self._parent_notified = True
			
	# Cancel an update for a child node
	def cancel_update(self, child_node_id):
		self._children_to_update.remove(child_node_id)
		
		# Propagate this up the hierarchy if we are done
		if len(self._children_to_update) == 0 and self._parent and not self._need_child_update:
			self._parent.cancel_update(self.node_id)
			self._parent_notified = True
	
	# Transform properties
	@property
	def parent(self):
		return self._parent
	
	# Positions are all relative.  using a local_ prefix is redundant.
		
	# get local position
	@property
	def position(self):
		return self._local_position
		
	# set position relative to parent
	@position.setter
	def position(self, new_pos):
		# Calculate local position
		self._local_position = new_pos# - self._parent_matrix.get_translation()
		self._need_update()
		
	# get world position
	@property
	def world_position(self):
		return self._world_position
	
		
	# get local rotation
	@property
	def rotation(self):
		return self._local_rotation
	
	# set local rotation
	@rotation.setter
	def rotation(self, new_rot):
		self._local_rotation = new_rot
		self._need_update()
	
	# get world rotation		
	@property
	def world_rotation(self):
		return self._world_rotation
		
	# Get local scale
	@property
	def local_scale(self):
		return self._local_scale
	
	# Set local scale
	@local_scale.setter
	def local_scale(self, new_scale):
		self._local_scale = new_scale
		self._need_update()
	
	# Get world scale
	@property
	def world_scale(self):
#		return self._scale
		return self._world_scale
	
	@property
	def forward(self):
		return self._local_rotation * Vector3.FORWARD()
	
	@property
	def up(self):
		return self._local_rotation * Vector3.UP()
	
	@property
	def right(self):
		return self._local_rotation * Vector3.RIGHT()
	
	# set local/world position
	def translate(self, new_pos, relative_to=Space.SELF): # Add axis parameter?
		
		if relative_to == Space.SELF:
			self._local_position += self._local_rotation * new_pos
		elif relative_to == Space.WORLD:
			if self._parent:
				self._local_position += ( self._parent.world_position.conjugated() * new_pos) / self._parent.world_scale
			else:
				self._local_position += new_pos
		elif relative_to == Space.PARENT:
			self._local_position += new_pos
		
		self._need_update()
		
	# set world rotation
	def rotate(self, new_rot, relative_to=Space.SELF):
		
		qnorm = new_rot.copy()
		qnorm.normalize()
				
		if relative_to == Space.SELF:
			self._local_rotation = self._local_rotation * qnorm
		elif relative_to == Space.PARENT:
			self._local_rotation = qnorm * self._local_rotation
		elif relative_to == Space.WORLD:
			self._local_rotation = self._local_rotation * self._world_rotation.conjugated() * qnorm * self._world_rotation
		
		self._need_update()
	
	# Set Scale
	def scale(self, new_scale):
		self._local_scale = self._local_scale * new_scale
		self._need_update()
		
# Primitive Objects
class Plane(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.mesh = MeshFactory.get_mesh(MeshTypes.PLANE_HI)
		
class Cube(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.mesh = MeshFactory.get_mesh(MeshTypes.CUBE)
		
class Sphere(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.mesh = MeshFactory.get_mesh(MeshTypes.SPHERE)
		
class Octo(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.mesh = MeshFactory.get_mesh(MeshTypes.OCTOHEDRON)
		
class Light(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.light = GLLight()




	