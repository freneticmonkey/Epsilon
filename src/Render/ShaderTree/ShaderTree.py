'''
Created on Mar 11, 2012

@author: scottporter
'''

from ShaderNodes import *

class ShaderTree(object):
    
    def __init__(self, name=""):
        self._name = name
        self._variable_table = []
        self._nodes = []
        self._data = []
        self._source = ""
        
        # Generation Variables
        self._variables = []
        self._definitions = []
        
    @property
    def source(self):
        if self._source == "":
            self.process_tree()
        return self._source
        
    def add_node(self, new_node):
        self._nodes.append(new_node)
        
    def remove_node(self, del_node):
        self._nodes.remove(del_node)
        
    def add_data(self, data):
        self._data.append(data)
        
    def remove_data(self, data):
        self._data.remove(data)
    
    def get_unique_variable_name(self, variable):
        added_variable = None
        
        if not variable in self._variable_table:
            self._variable_table.append(variable)
            added_variable = variable
        else:
            # generate a new postfix for the variable
            # by appending an integer to the end of the
            # requested variable
            prefix = variable
            for ipostfix in range(1,100):
                gen_variable = prefix + str(ipostfix)
                if not gen_variable in self._variable_table:
                    self._variable_table.append(gen_variable)
                    added_variable = gen_variable
                    break
        
        return added_variable
    
    # Check that the tree can generate a valid shader
    def validate_tree(self):
        pass
    
    # Walk the tree and output the nodes as script
    def process_tree(self):
        # Find the/an output node within the tree
        output_node = None
        
        for node in self._nodes:
            if isinstance(node, ViewerOutputNode):
                output_node = node
            # elif other output nodes
            if not output_node is None:
                break
        
        # The way the tree is constructed it's essentially reversed where
        # the root node is the output and everything feeds into it.  So,
        # with that in mind, perform a standard breadth first walk through the
        # tree writing the functions as we go.
        self.process_connections(output_node)
        
    def process_connections(self, node):
        connections = []    
        for name, socket in node.inputs.iteritems():
            if socket.connected:
                pass
                
            
            
        
                
    
    
    
    
    
    
    