'''
Created on Mar 11, 2012

@author: scottporter
'''

# Used to store UI properties when visualising the Shader
class ShaderUICoord(object):
    __slots__ = ["x","y"]
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ShaderUIProperty(object):
    __slots__ = ["coord","width","height"]
    def __init__(self, coord, width, height):
        self.coord = coord
        self.width = width
        self.height = height
    
class ShaderUILine(object):
    __slots__ = ["start", "end", "segments"]
    def __init__(self, start, end, segments):
        self.start = start
        self.end = end
        self.segments = segments

class ShaderDataType:
    INTEGER = 1
    FLOAT = 2
    VECTOR4 = 3
    VECTOR3 = 4
    VECTOR2 = 5
    STRING = 6
    BOOL = 7
    IMAGE_BUFFER = 8
    
class ShaderVariable(object):
    def __init__(self, name, datatype, value, tree):
        self._name = name
        self._datatype = datatype
        self._value = value
        self._tree = tree
        
        if not tree is None:
            self._name = self._tree.get_unique_variable_name(self._name)
    
    @property
    def name(self):
        return self._name
    
    @property
    def datatype(self):
        return self._datatype
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value
        
class ShaderProperty(ShaderVariable):
    
    @classmethod
    def create(cls, shader_node_parent, name, default, placeholder, datatype):
        shader_node_parent.add_input(ShaderProperty(name, default, placeholder, datatype, shader_node_parent))
               
    def __init__(self, name, default, placeholder_name, datatype, parent, clamp=False, clamp_min=None, clamp_max=None):
        ShaderVariable.__init__(self, name, datatype, default, parent.tree)
        self._placeholder_name = placeholder_name
        self._datatype = datatype
        self._clamp = clamp
        self._clamp_min = clamp_min
        self._clamp_max = clamp_max
        self._parent = parent
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def placeholder_name(self):
        return self._placeholder_name
    
    @property
    def clamp(self):
        return self._clamp
    
    @property
    def clamp_min(self):
        return self._clamp_min
    
    @property
    def clamp_max(self):
        return self._clamp_max

# This class is kinda redundant for the time being as only 
# connections of single variables are currently handled
class ConnectionConnectivity:
    SINGLE = 1  # Single
    MULTI = 2   # arrays
    BOUNDED = 3 # length limited arrays

class ConnectionType:
    INPUT = 1
    OUTPUT = 2

class ConnectionSocket(ShaderProperty):
    
    @classmethod
    def create(cls, shader_node_parent, conn_type, name, default, placeholder, datatype, connectivity=ConnectionConnectivity.SINGLE):
        if conn_type == ConnectionType.INPUT:
            shader_node_parent.add_input(ConnectionSocket(name, default, placeholder, datatype, shader_node_parent))#connectivity))
        elif conn_type == ConnectionType.OUTPUT:
            shader_node_parent.add_output(ConnectionSocket(name, default, placeholder, datatype, shader_node_parent))#connectivity))
    
    def __init__(self, name, default, placeholder, datatype, parent):#connectivity):#, bound_length=1):
        ShaderProperty.__init__(self, name, default, placeholder, datatype, parent)
        self._connection = None
        self._operation_token = None
        #self._connections = []
        #self._bound_length = bound_length
        
    @property
    def connectivity(self):
        return self._connectivity
    
    @property
    def connected(self):
        return self._connection == None
    
    @property
    def connection(self):
        return self._connection
    
    # check if the incoming connection socket can be connected to this socket
    def add_connection(self, new_conn):
        # If not currently performing an operation - prevent infinite loop
        if self._operation_token is None:
            if new_conn.datatype == self.datatype:
                
                # Single Connection only at this point - disconnect existing
                if not self._connection is None:
                    self._connection.remove_connection()
                    
                self._connection = new_conn
                # indicate that the connection has been made on this end
                self._operation_token = True
                # Connect the other end of the connection
                new_conn.add_connection(self)
            # indicate that the connection process is complete
            self._operation_token = None
            
    def remove_connection(self):
        if self._operation_token is None:
            self._operation_token = True
            if not self._connection is None:
                # Disconnect on the other end
                self._connection.remove_connection()
            # Disconnect from this end
            self._connection = None
            self._operation_token = None
    
    # NOTE: This code was written with the idea of being able to specify
    # fixed length arrays as a connection type.  This doesn't seem to be 
    # necessary at the moment so I'll worry about it later.
    # New connections automatically replace existing connections
#    def add_connection(self, new_conn, bound_pos=0):
#        if new_conn.datatype == self.datatype:
#            if self.connectivity == ConnectionConnectivity.SINGLE:
#                self._connections[0] = new_conn
#            elif self.connectivity == ConnectionConnectivity.MULTI:
#                self._connections.append(new_conn)
#            elif self.connectivity == ConnectionConnectivity.BOUNDED:
#                if self._bound_length > bound_pos:
#                    self._connections[bound_pos] = new_conn
#                else:
#                    print "Attempted connection to invalid bound socket. %d" % bound_pos
#        else:
#            print "Connection types do not match"

class ShaderNodeBase(object):
    
    _tree = None
    
    _input_sockets = {}
    _output_sockets = {}
    _definition = None
    _call_format = ""
    
    def __init__(self, tree=None):
        self._tree = tree
        self._process_connections()
    
    @property
    def inputs(self):
        return self._input_sockets
    
    @property
    def outputs(self):
        return self._output_sockets
    
    # Adding/Removing Sockets
    def add_input(self, socket):
        if not socket.name in self._input_sockets:
            self._input_sockets[socket.name] = socket
            
    def add_output(self, socket):
        if not socket.name in self._output_sockets:
            self._output_sockets[socket.name] = socket
            
    # Getting Sockets
    def get_input(self, name):
        return_socket = None
        if name in self._input_sockets:
            return_socket = self._input_sockets[name]
        return return_socket
    
    def get_output(self, name):
        return_socket = None
        if name in self._output_sockets:
            return_socket = self._output_sockets[name]
        return return_socket
    
    # Connecting Sockets
    def add_input_connection(self, socket_name, incoming_connection):
        if socket_name in self._input_sockets:
            self._input_sockets[socket_name].add_connection(incoming_connection)
            
    def add_output_connection(self, socket_name, outgoing_connection):
        if socket_name in self._output_sockets:
            self._output_sockets[socket_name].add_connection(outgoing_connection)
            
    def remove_input_connection(self, socket_name):
        if socket_name in self._input_sockets:
            self._input_sockets[socket_name].remove_connection()
            
    def remove_output_connection(self, socket_name):
        if socket_name in self._output_sockets:
            self._output_sockets[socket_name].remove_connection()
    
    
    def connect(self, input_socket_name, to_node, output_socket_name):
        output_socket = to_node.get_output(output_socket_name)
        if not output_socket is None:
            self.add_input_connection(input_socket_name, output_socket)
            
    def disconnect(self, input_socket_name):
        self.remove_input_connection(input_socket_name)
         
            
    # Over-ridden in child classes
    def _process_connections(self):
        pass
    
    def output_definition(self):
        return self._definition
    
    def output_function_call(self):
        call_string = self._call_format
        
        for o_socket in self._output_sockets:
            call_string = call_string.replace(o_socket.placeholder, o_socket.name)
        
        return call_string
        
            
            
            
        
    
    
    