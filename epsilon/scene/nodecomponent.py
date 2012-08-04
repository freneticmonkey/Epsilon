
class NodeComponent(object):
    def __init__(self, node=None):
        self.node_parent = node
        
    @property
    def node_parent(self):
        return self._node_parent
    
    @node_parent.setter
    def node_parent(self, set_node):
        self._node_parent = set_node
        self._transform = None
        
        if not self._node_parent is None:
            self._transform = self._node_parent.transform
    
    def on_add(self):
        pass
    
    def on_remove(self):
        pass