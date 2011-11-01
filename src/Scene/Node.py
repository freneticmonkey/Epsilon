"""

	Note: The Transform code has been ported from OGRE www.ogre3d.org

"""


from Geometry.euclid import Vector3, Quaternion, Matrix4
from Scripting.ScriptManager import ScriptManager
from Render.MeshFactory import *

_next_id = 0

class Space:
	SELF = 0
	WORLD = 1
	PARENT = 2

def GetId():
	global _next_id
	_next_id += 1
	return _next_id

class Node(object):
	
	def __init__(self, name=None, pos=None, rot=None, scale=None, parent=None):
		
		# Node Properties
		self._id = GetId()
		
		# Generate a name if one has not been supplied
		if not name:
			name = "Node_" + str(self._id)
		
		self._name = name
		self._mesh = None
		self._material = None
		self._light = None
		self._visible = True
		self._scripts = []
		
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
	
	# If deleted
	def __del__(self):
		# Kill any scripts
		for script in self._scripts:
			ScriptManager.GetInstance().RemoveScript(script)
		
		# Detach any children
		for child in self._children:
			# TODO: HMMM - Re-attach the nodes to the scene Root rather than just leaving them dangling??
			child._parent = None
			
		self._children_to_update = []
			
	def __repr__(self):
		return "Id: " + str(self._id) + " Name: " + self._name
	
	# Node Property access
	
	@property
	def id(self):
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
	
	# Node Functions
	
	# Script Handling
	def AddScript(self, new_script):
		new_script.node = self
		self._scripts.append(new_script)
	
	def RemoveScript(self, name='', rm_script=None):
		if len(name) == 0:
			name = rm_script.name
		
		for script in self._scripts:
			if len(name) > 0 and script.name == name:
				script.node = None
				self._scripts.remove(script)
				break
	
	# Child Node handling
	def AddChild(self, child_node):
		if isinstance(child_node, Node):
			child_node._parent = self
			self._children.append(child_node)
			# Allow the child to perform any post addition actions
			child_node.OnAdd()
			# Notify the parent that we have changed
			self._NeedUpdate(True)
		else:
			print "Error: child parameter is not a Node instance"
			
	def RemoveChild(self, child_node):
		if isinstance(child_node, Node):
			if child_node in self._children:
				child_node._parent = None
				self._children.remove(child_node)
				
				# Allow the former child to perform any post removal actions
				child_node.OnRemove()
				
				# Notify the parent that we have changed
				self._NeedUpdate(True)
		else:
			print "Error: Child is not a Node instance"
	
	# In future this could be recursive			
	def GetChildWithId(self, id):
		ret_child = None
		for child in self._children:
			if child.id == id:
				ret_child = child
				break
		return ret_child
	
	def GetChildWithName(self, name):
		ret_child = None
		for child in self._children:
			if child.name == name:
				ret_child = child
				break
		return ret_child
	
	# This function is called whenever the node is added as a child to another node
	def OnAdd(self):
		pass
	
	# This function is called whenever the node is removed as a child from another node
	def OnRemove(self):
		pass
	
	# Update the Node and it's children's transforms
	def _Update(self, update_children, parent_has_changed):
		
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
			self._UpdateFromParent()
		
		# Update the children of the node
		if self._need_child_update or parent_has_changed:
			for child_node in self._children:
				child_node._Update(True,True)
			
			self._children_to_update = []
		else:
			# Update only the children that have requested updates
			for id in self._children_to_update:
				for child_node in self._children:
					if id == child_node.id:
						child_node._Update(True,False)
						break
			self._children_to_update = []
		
		self._need_child_update = False
			
			
	# Called from parent node.  Updates transform properties and any child transform properties
	def _UpdateFromParent(self):
		
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
	def _NeedUpdate(self, force_parent_update=False):
		self._need_parent_update = True
		self._need_child_update  = True
		
		# if this not is not the root and the parent hasn't already been notified
		if self._parent and ( not self._parent_notified or self._force_parent_update):
			self._parent.RequestUpdate(self.id, force_parent_update)
			self._parent_notified = True
		
		# All children will be updated
		self._children_to_update = []
		
	# Request for the parent to update it's children
	def RequestUpdate(self, child_node_id, force_parent_update=False):
		# If we are already going to update everything then this doesn't matter
		if self._need_child_update:
			return
		
		self._children_to_update.append(child_node_id)
		# Request selective update of this node, if it hasn't already been done
		if self._parent and (not self._parent_notified or self._force_parent_update):
			self._parent.RequestUpdate(self.id, force_parent_update)
			self._parent_notified = True
			
	# Cancel an update for a child node
	def CancelUpdate(self, child_node_id):
		self._children_to_update.remove(child_node_id)
		
		# Propagate this up the hierarchy if we are done
		if len(self._children_to_update) == 0 and self._parent and not self._need_child_update:
			self._parent.CancelUpdate(self.id)
			self._parent_notified = True
	
	# Transform properties
	@property
	def parent(self):
		return self._parent
		
	# get local position
	@property
	def local_position(self):
		return self._local_position
		
	# set position relative to parent
	@local_position.setter
	def local_position(self, new_pos):
		# Calculate local position
		self._local_position = new_pos# - self._parent_matrix.get_translation()
		self._NeedUpdate()
		
	# get world position
	@property
	def world_position(self):
		return self._world_position
	
	# Another world position access
	@property
	def position(self):
		return self.world_position
		
	# get local rotation
	@property
	def local_rotation(self):
		return self._local_rotation
	
	# set local rotation
	@local_rotation.setter
	def local_rotation(self, new_rot):
		self._local_rotation = new_rot
		self._NeedUpdate()
	
	# get world rotation		
	@property
	def world_rotation(self):
		return self._world_rotation
	
	@property
	def rotation(self):
		return self.world_rotation
		
	# Get local scale
	@property
	def local_scale(self):
		return self._local_scale
	
	# Set local scale
	@local_scale.setter
	def local_scale(self, new_scale):
		self._local_scale = new_scale
		self._NeedUpdate()
	
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
		
		self._NeedUpdate()
		
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
		
		self._NeedUpdate()
	
	# Set Scale
	def scale(self, new_scale):
		self._local_scale = self._local_scale * new_scale
		self._NeedUpdate()
		
# Primitive Objects
class Plane(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.mesh = MeshFactory.GetMesh(MeshTypes.PLANE_HI)
		
class Cube(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.mesh = MeshFactory.GetMesh(MeshTypes.CUBE)
		
class Sphere(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.mesh = MeshFactory.GetMesh(MeshTypes.SPHERE)
		
class Octo(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.mesh = MeshFactory.GetMesh(MeshTypes.OCTOHEDRON)
		
class Light(Node):
	def __init__(self, name=None):
		Node.__init__(self, name=name)
		self.light = GLLight()




	