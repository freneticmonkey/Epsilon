#!/usr/bin/python
# print_names.py: print node id and name of all nodes on the server
import verse as v

def cb_connect_accept(v_avatar, address, host_id):
	# construct a mask to receive all node types
	# for example, mask = 1 << v.GEOMETRY means: list all geometry nodes
	print "accepted"
	mask = 0
	for i in range(0, v.NUM_TYPES):
		mask |= 1 << i

	v.send_node_index_subscribe(mask)

def cb_node_create(node_id, type, owner_id):
	# subscribe to this node, so we get node_name_set callbacks
	print "create"

	v.send_o_transform_subscribe(node_id, v.FORMAT_REAL32)
	v.send_node_subscribe(node_id)

	q = v.Quat32()
	q.x = 3.1415
	q.y = 2*3.1415
	q.z = 3*3.1415
	q.w = 4*3.1415
	z = (1, 2, 3, 4)
	
	v.send_o_transform_rot_real32(node_id, 0, 0, q, z, z, z, 0)

def cb_node_rot(node_id, time_s, time_f, rot, speed, acc, dragn, drag):
	print "rot:", rot.x, rot.y, rot.z, rot.w

def cb_node_name_set(node_id, name):
	# print the node id and name
	print "name set"
	print str(node_id) + ": " + name

def main():
	# set callback functions
	v.callback_set(v.SEND_CONNECT_ACCEPT, cb_connect_accept)
	v.callback_set(v.SEND_NODE_CREATE, cb_node_create)
	v.callback_set(v.SEND_NODE_NAME_SET, cb_node_name_set)
	v.callback_set(v.SEND_O_TRANSFORM_ROT_REAL32, cb_node_rot)

	# connect and set active session
	#session = v.send_connect("uname", "pass", "localhost", 0)
	session = v.send_connect("uname", "pass", "10.1.1.14", 0)
	v.session_set(session)

	# wait for callbacks for a reasonable amount of time
	for i in range(0, 10000):
		v.callback_update(10000)
	
	# terminate the connection, some more callbacks are needed to make sure
	# the message reaches the server
	v.send_connect_terminate("", "adios!")
	for i in range(0, 5):
		v.callback_update(10000)
	v.session_destroy(session)

main()

