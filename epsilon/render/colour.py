'''
Created on Sep 18, 2011

@author: scottporter
'''
from collections import namedtuple
from random import randint, uniform, random
from OpenGL.GL import GLfloat

from epsilon.render.glutilities import *

class Colour(object):

    @classmethod
    def from_string(cls,colour_string):
        rgba = colour_string.split(" ")
        if len(rgba) == 4:
            rgba = Colour(float(rgba[0]), float(rgba[1]),float(rgba[2]),float(rgba[3]))
            return rgba
        else:
            print "Colour: Invalid string parameter: " + colour_string
            return None

    def __init__(self, r=1.0, g=1.0, b=1.0, a=1.0):

        # Ensure internal storage is in artimetic format
        if (r+g+b+a) > 4.0:
            r /= 255.0
            g /= 255.0
            b /= 255.0
            a /= 255.0

        self._r = r
        self._g = g
        self._b = b
        self._a = a

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, new_value):
        if new_value > 1.0:
            new_value /= 255.0
        self._r = new_value

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, new_value):
        if new_value > 1.0:
            new_value /= 255.0
        self._g = new_value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, new_value):
        if new_value > 1.0:
            new_value /= 255.0
        self._b = new_value

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, new_value):
        if new_value > 1.0:
            new_value /= 255.0
        self._a = new_value
    
    def __repr__(self):
        return 'Colour(%f, %f, %f, %f)' % (self.r, self.g, self.b, self.a)
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    # Get a Colour object with a random colour
    @staticmethod
    def random():
        return Colour( random(), random(), random(), 1.0)
    
    def inverted(self):
        return Colour( 1.0 - self.r,
                       1.0 - self.g,
                       1.0 - self.b,
                       1.0
                     )
    
    def tinted(self, other=None, proportion=0.5):
        if other is None:
            other = Preset.white
        
        return Colour( self.r * (1 - proportion) + other.r * proportion,
                       self.g * (1 - proportion) + other.g * proportion,
                       self.b * (1 - proportion) + other.b * proportion,
                       self.a * (1 - proportion) + other.a * proportion                      
                     )
    # Returns the colour as an array in the range of 0 - 1.0
    def get_arithmetic(self):
        return (self.r, self.g, self.b, self.a)
    
    # Returns the colour as an array in the range 0 - 255
    def get_8bit(self):
        return ( self.r * 255, self.g * 255.0, self.b * 255.0, self.a * 255.0)
    
    # Get OpenGL Array representation of the Colour
    def get_gl_colour(self):
        return CreateGLArray(GLfloat, self.get_8bit(), 4)
    
    # Get a normalised array representation of the colour
    def get_shader_colour(self):
        #return ((self.r/255.0), (self.g/255.0), (self.b/255.0), self.a)
        return self.get_arithmetic()
    
class Preset:
    # Preset Colours
    red    = Colour(1.0,  0,  0 ,1.0)
    green  = Colour(  0,1.0,  0 ,1.0)
    blue   = Colour(  0,  0,1.0 ,1.0)
    yellow = Colour(1.0,1.0,  0 ,1.0)
    orange = Colour(1.0,0.5,  0 ,1.0)
    cyan   = Colour(  0,1.0,1.0 ,1.0)
    purple = Colour(1.0,  0,1.0 ,1.0)
    white  = Colour(1.0,1.0,1.0 ,1.0)
    grey   = Colour(0.5,0.5,0.5 ,1.0)
    lightgrey   = Colour(0.7,0.7,0.7 ,1.0)
    darkgrey    = Colour(0.3,0.3,0.3 ,1.0)
    black  = Colour(  0,  0,  0 ,1.0)
    purple = Colour(0.7,0.0,1.0,1.0)
    
#    red    = Colour(255,  0,  0,255)
#    green  = Colour(  0,255,  0,255)
#    blue   = Colour(  0,  0,255,255)
#    yellow = Colour(255,255,  0,255)
#    orange = Colour(255,127,  0,255)
#    cyan   = Colour(  0,255,255,255)
#    purple = Colour(255,  0,255,255)
#    white  = Colour(255,255,255,255)
#    grey   = Colour(128,128,218,255)
#    black  = Colour(  0,  0,  0,255)