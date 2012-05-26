'''
Created on Sep 17, 2011

@author: scottporter
'''
from OpenGL.GL import *
from OpenGL.GLU import *

class Projection(object):
    
    def __init__(self, width, height):
        self._width = width
        self._height = height
        
    def resize(self, width, height):
        self._width = width
        self._height = height
        glViewport(0, 0, width, height)
        
    def set_perspective(self, fovy):
        aspect = self._width / self._height
        zNear = 0.1
        zFar = 1000.0
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovy, aspect, zNear, zFar)
        
    def set_screen(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, (self._width - 1), 0, (self._height - 1) )