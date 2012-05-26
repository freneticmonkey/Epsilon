'''
Created on Sep 28, 2011

@author: scottporter
'''

from epsilon.scene.node import *

def start_test():
    
    print "starting transform test"
    parent = Node(name='parent')
    child = Node(name='child')
    parent.AddChild(child)
    
    
    
    # Update child properties
    
    print "finished transform test"


if __name__ == "__main__":
    start_test()