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
    print "Epsilon Engine Terminated.."

if __name__ == "__main__":
    main()
