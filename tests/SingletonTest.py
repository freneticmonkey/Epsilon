#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
'''
Created on Nov 19, 2011

@author: scottporter
'''

class BaseSingleton(object):
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            
        return cls._instance
    
class Child(BaseSingleton):
    
    def __init__(self):
        print "Child class"
        
class ChildTwo(BaseSingleton):
    
    _test = ""
    
    def __init__(self):
        print "ChildTwo class"
        self._test = "initialised"
        
    @classmethod
    def access(cls):
        print cls._instance._test
        
def main():
    c = Child.get_instance()
    d = Child.get_instance()
    
    e = ChildTwo.get_instance()
    
    print "C: " + str(id(c))
    print "D: " + str(id(d))
    
    print "E: " + str(id(e))
    e.access()
        
if __name__ == "__main__":
    main()