#from Core.EpsilonManager import EpsilonManager

import sys, traceback
import os

import cProfile

# Add the epsilon path to the python path
epsilon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(epsilon_path)
from epsilon.core.epsilonmanager import EpsilonManager
    
def main():
    core = None
    try:
            core = EpsilonManager()
            core.set_scene()
            core.run()
    except Exception, e:
            print "EpsilonCore: ERROR"
            print e.args
            traceback.print_exc(file=sys.stdout)
    if core:
        del core

if __name__ == "__main__":
    #cProfile.run("main()")
    main()
            

'''

TODO List

* Write a ScriptManager and Script class.
  Ideally ScriptManager can break scripts out into multiple threads
  
Script class:
functions:
    _init
    _start
    _before_render
    _update
    _after_render
    
    _physics_event
    _custom_event - ?
    
    _routes / _slots ? - easy ability to add events between two script objects
                         This function would be called first before any other
                         
Predefined Script Classes:
TransformScript
LightScript
PhysicsScript
AudioScript
AnimationScript - This is a Sub-set of the TransformScript

These classes are for specific node components and expose the component's 
properties to script manipulation.


* Write a Physics Layer
  Use PyODE and integrate it into node objects using a rigidbody property for Node objects
  
* Add Materials
  Use the materials property of the Node objects to allow materials to be used
  
* Add Audio Layer

* Networking.
  Don't really know what to do here.  I only really have an interest to integrate verse.


'''
