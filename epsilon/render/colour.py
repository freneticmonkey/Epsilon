'''
Created on Sep 18, 2011

@author: scottporter
'''
from collections import namedtuple
from random import randint, uniform, random
from OpenGL.GL import GLfloat

from epsilon.render.glutilities import *

class Colour( namedtuple('Colour','r g b a')):
    
    @classmethod
    def from_string(cls,colour_string):
        rgba = colour_string.split(" ")
        if len(rgba) == 4:
            rgba = Colour(float(rgba[0]), float(rgba[1]),float(rgba[2]),float(rgba[3]))
            return rgba
        else:
            print "Colour: Invalid string parameter: " + colour_string
            return None
    
    def __repr__(self):
        return 'Colour(%f, %f, %f, %f)' % (self.r, self.g, self.b, self.a)
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    # Get a Colour object with a random colour
    @staticmethod
    def random():
        #return Colour( randint(0,255), randint(0,255), randint(0,255), 255 )
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
        
        return Colour( int(self.r * (1 - proportion) + other.r * proportion),
                       int(self.g * (1 - proportion) + other.g * proportion),
                       int(self.b * (1 - proportion) + other.b * proportion),
                       int(self.a * (1 - proportion) + other.a * proportion)                      
                     )
    # Returns the colour as an array in the range of 0 - 1.0
    def get_float_colour(self):   
        return (self.r / 255.0), (self.g / 255.0), (self.b / 255.0), (self.a / 255.0)
    
    
    # Get OpenGL Array representation of the Colour
    def get_gl_colour(self):
        return CreateGLArray(GLfloat, self, 4)
    
    # Get a normalised array representation of the colour
    def get_shader_colour(self):
        return ((self.r/256.0), (self.g/256.0), (self.b/256.0), self.a)
    
class Preset:
    # Preset Colours
    red    = Colour(1.0,  0,  0 ,1.0)
    green  = Colour(  0,1.0,  0 ,1.0)
    blue   = Colour(  0,  0,1.0 ,1.0)
    yellow = Colour(1.0,1.0,  0 ,1.0)
    orange = Colour(1.0,127,  0 ,1.0)
    cyan   = Colour(  0,1.0,1.0 ,1.0)
    purple = Colour(1.0,  0,1.0 ,1.0)
    white  = Colour(1.0,1.0,1.0 ,1.0)
    grey   = Colour(0.5,0.5,0.5 ,1.0)
    black  = Colour(  0,  0,  0 ,1.0)
    purple = Colour(0.9,0.9,0.98,1.0)
    
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