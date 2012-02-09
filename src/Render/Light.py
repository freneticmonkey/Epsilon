'''
Created on Sep 21, 2011

@author: scottporter
'''
from Render import Colour
from Render.GLUtilities import *
from Scene.Node import Node

from OpenGL.GL import *

from Events.EventBase import EventBase

# Light Events
class LightAddedEvent(EventBase):
    def __init__(self, camera):
        EventBase.__init__(self, "LightAdded", camera)
        
class LightRemovedEvent(EventBase):
    def __init__(self, camera):
        EventBase.__init__(self, "LightRemoved", camera)

class LightBase(Node):
    
    def __init__(self, name=None, ambient=None, diffuse=None, specular=None, attenuation=None):
        Node.__init__(self, name, pos=None, rot=None, scale=None, parent=None)
        if not ambient:
            ambient = Colour.Colour(0.2, 0.2, 0.2, 1.0)
        if not diffuse:
            diffuse = Colour.Colour(0.8, 0.8, 0.8, 1.0)
        if not specular:
            specular = Colour.Colour(0.5, 0.5, 0.5, 1.0)
        if not attenuation:
            # For now only linear attenuation is supported until i figure out a vec4 class
            attenuation = 0.5 
        
        self._ambient = ambient
        self._diffuse = diffuse
        self._specular = specular
        self._attenuation = attenuation
        
    @property
    def ambient(self):
        return self._ambient
    
    @ambient.setter
    def ambient(self, new_colour):
        self._ambient = new_colour
    
    @property
    def diffuse(self):
        return self._diffuse
    
    @diffuse.setter
    def diffuse(self, new_colour):
        self._diffuse = new_colour
    
    @property
    def specular(self):
        return self._specular
    
    @specular.setter
    def specular(self, new_colour):
        self._specular = new_colour
    
    
    @property
    def attenuation(self):
        return self._attenuation
    
    @attenuation.setter
    def attenuation(self, new_attenuation):
        self._attenuation = new_attenuation
        
    def OnAdd(self):
        LightAddedEvent(self).Send()
        
    def OnRemove(self):
        LightRemovedEvent(self).Send()
    
# Use for spotlights - glLightf (GL_LIGHT0, GL_SPOT_CUTOFF, 15.f);
    
class GLLight(LightBase):
    
    def __init__(self, name=None, ambient=None, diffuse=None, specular=None, attenuation=None):
        LightBase.__init__(self,name, ambient, diffuse, specular, attenuation)
    
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, self._ambient.GetGLColour())
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self._diffuse.GetGLColour())
        glLightfv(GL_LIGHT0, GL_SPECULAR, self._specular.GetGLColour())
#        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.0)#self._attenuation)
#        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 1.0)#self._attenuation)
#        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0)#self._attenuation)
        
    
    def Draw(self):
        # OpenGL uses the MODELVIEW matrix which should already have the lights
        # position from the transform of the Light's parent.
        
#        pos = self.parent.local_position
#        pos  = CreateGLArray(GLfloat, (pos.x, pos.y, pos.z, 1.0), 4 )

#        pos  = CreateGLArray(GLfloat, (0, 0, 0, 1.0), 4 )
        
        glLightfv(GL_LIGHT0, GL_POSITION, pos)
        pass
        
        
