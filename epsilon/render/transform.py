from epsilon.geometry.euclid import Vector3, Quaternion, Matrix4
from epsilon.render.bounds import Bounds

class Space:
    SELF = 0
    WORLD = 1
    PARENT = 2

class Transform(object):
    _next_id = 0
    
    @classmethod
    def get_id(cls):
        cls._next_id += 1
        return cls._next_id
    
    def __init__(self, node=None, pos=None, rot=None, scale=None, parent=None, scene=None):
        self._id = Transform.get_id()
        
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
            
        self._node = node
            
        # World positions
        self._world_position = pos
        self._world_rotation = rot
        self._world_scale = scale
        
        # Bounds of transform including children
        self._bounds = Bounds(world_centre=self.position)
        
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
    
    def __del__(self):
    # Detach any children
        for child in self._children:
            # TODO: HMMM - Re-attach the nodes to the scene Root rather than just leaving them dangling??
            child._parent = None
            
        self._children_to_update = []
        
    def __repr__(self):
        return "Node: %s Id: %d Pos: %s Rot: %s Scale: %s" % (self._node.name, self._id, self.position, self.rotation, self._local_scale)
        
    @property
    def tid(self):
        return self._id
        
    @property
    def node(self):
        return self._node
        
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
        
    # Transform properties
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, new_parent):
        new_parent.add_child(self)
    
    # Positions are all relative.  using a local_ prefix is redundant.
        
    # get local position
    @property
    def position(self):
        return self._world_position
        
    # set position relative to parent
    @position.setter
    def position(self, new_pos):
        # Calculate local position
        
        # convert world position to relative position
        if self._parent:
            new_pos -= self._parent.position
        else:
        	self._world_position = new_pos
        
        self._local_position = new_pos# - self._parent_matrix.get_translation()
        self._need_update()
        
    # get local position
    @property
    def local_position(self):
        return self._local_position
        
    # get local rotation
    @property
    def rotation(self):
        return self._world_rotation
    
    # set local rotation
    @rotation.setter
    def rotation(self, new_rot):
        self._local_rotation = new_rot
        self._need_update()
    
    # get local rotation        
    @property
    def local_rotation(self):
        return self._local_rotation
        
    # Get local scale
    @property
    def local_scale(self):
        return self._local_scale
    
    # Set local scale
    @local_scale.setter
    def local_scale(self, new_scale):
        self._local_scale = new_scale
        self._need_update()
    
#    # Get world scale
#    @property
#    def world_scale(self):
##        return self._scale
#        return self._world_scale
    
    @property
    def forward(self):
        return self._local_rotation * Vector3.FORWARD()
    
    @property
    def up(self):
        return self._local_rotation * Vector3.UP()
    
    @property
    def right(self):
        return self._local_rotation * Vector3.RIGHT()
    
    @property
    def bounds(self):
        return self._bounds
    
    # set local/world position
    def translate(self, new_pos, relative_to=Space.SELF): # Add axis parameter?
        
        if relative_to == Space.SELF:
            self._local_position += self._local_rotation * new_pos
        elif relative_to == Space.WORLD:
            if self._parent:
                self._local_position += ( self._parent.position.conjugated() * new_pos) / self._parent.local_scale
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
    
    # Child Node handling
    def add_child(self, child_node_trans):
        if isinstance(child_node_trans, Transform):
            child_node_trans._parent = self
            child_node_trans._scene = self._scene
            self._children.append(child_node_trans)
            # Allow the child to perform any post addition actions
            child_node_trans.on_add()
            # Notify the parent that we have changed
            self._need_update(True)
        else:
            print "Error: child parameter is not a Transform instance"
            
    def remove_child(self, child_node_trans):
        if isinstance(child_node_trans, Transform):
            if child_node_trans in self._children:
                child_node_trans._parent = None
                child_node_trans._scene = None
                self._children.remove(child_node_trans)
                
                # Allow the former child to perform any post removal actions
                child_node_trans.on_remove()
                
                # Notify the parent that we have changed
                self._need_update(True)
        else:
            print "Error: Child is not a Transform instance"
            
    def remove_children(self):
        if self._children is None:
            print "?"
        else:
            for child in self._children:
                if child is None:
                    print "Null child...?"
                    
        # FIXME: This should be performed in reverse order? - Hell yes.
        for i in reversed(range(0, len(self._children))):
            child = self._children[i]
            self.remove_child(child)
    
    # This function is called whenever the node is added as a child to another node
    def on_add(self):
        #notify the parent node
        self.node.on_add()
        
        # Propogate the event to children, otherwise they will never know correct state
        # e.g attached to a new scene
        for child in self.children:
            child.on_add()
    
    # This function is called whenever the node is removed as a child from another node
    def on_remove(self):
        # notify the parent node
        self.node.on_remove()
        
        #Propogate to children
        for child in self.children:
            child.on_remove()
    
    # In future this could be recursive            
    def get_child_with_id(self, id, recursive=False):
        ret_child = None
        for child in self._children:
            if child._node.tid == id:
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
            if child._node.name == name:
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
            
            if isinstance(child, Transform):
                if child.__class__.__name__ == class_type:
                    ret_child = child
                    break
            else:
                if child._node.__class__.__name__ == class_type:
                    ret_child = child
                    break
        # Breadth first recursive search
        if recursive and not ret_child:
            for child in self._children:
                ret_child = child.get_child_with_type(class_type, recursive)
                if not ret_child is None:
                    break
        return ret_child
    
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
                    if id == child_node.tid:
                        child_node._update(True,False)
                        break
            self._children_to_update = []
        
        self._need_child_update = False
        
        # Now that the children's transforms have been updated, update
        # this transform's bounds
        self._update_bounds()
            
    # Called from parent node.  Updates transform properties and any child transform properties
    def _update_from_parent(self):
        
        if self._parent:
            
            # update rotation
            parent_rotation = self._parent.rotation
            if self._inherit_rotation:
                # Combine rotation with parent rotation
                self._world_rotation = parent_rotation * self._local_rotation
            else:
                self._world_rotation = self._local_rotation
            
            # update scale
            parent_scale = self._parent.local_scale
            if self._inherit_scale:
                # Scale own position by parent scale
                self._local_scale = parent_scale * self._local_scale
            else:
                self._local_scale = self._local_scale
            
            # Change position vector based on parent's rotation and scale
            self._world_position = parent_rotation * (parent_scale * self._local_position)
            
            # Add altered position vector to parent's position
            self._world_position += self._parent.position
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
            self._parent.request_update(self.tid, force_parent_update)
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
            self._parent.request_update(self.tid, force_parent_update)
            self._parent_notified = True
            
    # Cancel an update for a child node
    def cancel_update(self, child_node_id):
        self._children_to_update.remove(child_node_id)
        
        # Propagate this up the hierarchy if we are done
        if len(self._children_to_update) == 0 and self._parent and not self._need_child_update:
            self._parent.cancel_update(self.tid)
            self._parent_notified = True
            
            
    # Update the transform's bounds
    def _update_bounds(self):
        updated_bounds = None
        
        if len(self.children) > 0:
            
            for child in self.children:
                cb = None
                
                # If the child has a mesh get the mesh's bounds
#                if not child.node.renderer is None and not child.node.renderer.mesh is None:
#                    cb = child.node.renderer.mesh.bounds
                if not child.node is None:
                    cb = child.node.transform.bounds
                
                # If there is a bounds
                if not cb is None:
                    # if an updated bounds hasn't been created yet
                    if updated_bounds is None:
                        updated_bounds = Bounds(world_centre=self.position)
                    
                    # if the child bound is not empty
                    if not cb.is_empty:
                        updated_bounds += cb
        else:
            # If there isn't any children, but the node attached to this transform has a mesh.
            if not self.node.renderer is None and not self.node.renderer.mesh is None:
                # Get the mesh's bounds
                updated_bounds = self.node.renderer.mesh.bounds
                # centre it to this transform
                updated_bounds.world_centre = self.position
                
        # If a new bounds was generated
        if not updated_bounds is None:
            self._bounds = updated_bounds
        # If a new bounds wasn't generated, but the existing bounds has something in it 
        elif not self._bounds.is_empty:
            # set a empty bounds
            self._bounds = Bounds(world_centre=self.position)
        # else no new bounds was generated, and the existing bounds is already empty
        # so don't do anything.
            
                    
                
            
            
            