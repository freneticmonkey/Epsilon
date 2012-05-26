'''
Created on Sep 25, 2011

@author: scottporter
'''

#from Geometry.euclid import *
import math
        
def deg_to_rad(angle):
    return angle * (math.pi/180)

def rad_to_deg(angle):
    return angle * (180/math.pi)
        
def test_transform():
    
    # parent
    pos = Vector3(0,2,0)
    rot = Quaternion().new_rotate_axis(deg_to_rad(45), Vector3(0,1,0))
    scale = Vector3(1,1,1)
#    scale = Vector3(2,2,2)
    
    mat = Matrix4()
    mat.translate(*pos)
    mat *= rot.get_matrix()
    mat.scale(*scale)
    
    print "parent"
    print mat
     
    # child
    cpos = Vector3(0,3,0)
    crot = Quaternion().new_rotate_axis(deg_to_rad(30), Vector3(0,1,0))
    
    cmat = Matrix4().translate(*cpos)
    cmat *= crot.get_matrix()
    cmat.scale(1,1,1)
    
    print "child"
    print cmat
    
    wmat = mat * cmat
    
    print "world"
    print wmat
    
    g_pos = wmat.get_translation()
    g_scale = wmat.get_scale()
    
    g_rot = wmat.get_rotation()
    angle, axis = g_rot.get_angle_axis()
    
    deg_a = angle * (180/math.pi)
    
    print "pos: " + str(g_pos)
    
    print "scale: " + str(g_scale)
    
    print "rot: " + str(deg_a) + "," + str(axis)
    
    
    diffmat = wmat * mat.inverse()
    
    print "diff"
    a, ax = diffmat.get_rotation().get_angle_axis()
    a = a * (180/math.pi)
    print "pos: " + str(diffmat.get_translation())
    print "scale: " + str(diffmat.get_scale())
    print "rot: " + str(a) + "," + str(ax)
    
    rota = Quaternion().new_rotate_axis(deg_to_rad(45), Vector3(0,1,0))
    rotb = Quaternion().new_rotate_axis(deg_to_rad(20), Vector3(0,1,0))
    
    rotf = rota * rotb
    
    a, ax = rotf.get_angle_axis()
    a = a * (180/math.pi)
    print "comb"
    print "rot: " + str(a) + "," + str(ax)
    
    rotd = Quaternion().new_rotate_axis(deg_to_rad(10), Vector3(0,1,0))
    
    rotf *= rotd
    
    rotc = rotf * rota.conjugated()
    
    a, ax = rotc.get_angle_axis()
    a = a * (180/math.pi)
    print "conj"
    print "rot c: " + str(a) + "," + str(ax)     
    
if __name__ == "__main__":
    test_transform()
    
    