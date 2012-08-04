'''
Created on Sep 21, 2011

@author: scottporter
'''
import math
from epsilon.geometry.euclid import Vector3
from epsilon.render.colour import Colour
from epsilon.render.glutilities import *
from epsilon.scene.node import Node
from epsilon.scene.nodecomponent import NodeComponent
#from epsilon.render.transform import Transform
from epsilon.events.eventbase import EventBase

from OpenGL.GL import *

# Light Events
class LightAddedEvent(EventBase):
    def __init__(self, camera):
        EventBase.__init__(self, "LightAdded", camera)
        
class LightRemovedEvent(EventBase):
    def __init__(self, camera):
        EventBase.__init__(self, "LightRemoved", camera)

class LightBase(NodeComponent):
    
    def __init__(self, ambient=None, diffuse=None, specular=None, attenuation=None):
        NodeComponent.__init__(self)
        
        if not ambient:
            ambient = Colour(0.2, 0.2, 0.2, 1.0)
        if not diffuse:
            diffuse = Colour(0.8, 0.8, 0.8, 1.0)
        if not specular:
            specular = Colour(0.5, 0.5, 0.5, 1.0)
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
        
    def on_add(self):
        if not self.node_parent.transform.scene is None:
            self.node_parent.transform.scene.add_light(self)
        #LightAddedEvent(self).Send()
        
    def on_remove(self):
        if not self.node_parent.transform.scene is None:
            self.node_parent.transform.scene.remove_light(self)
        #LightRemovedEvent(self).Send()
        
    
# Use for spotlights - glLightf (GL_LIGHT0, GL_SPOT_CUTOFF, 15.f);
    
class GLLight(LightBase):
    
    def __init__(self, ambient=None, diffuse=None, specular=None, attenuation=None):
        LightBase.__init__(self, ambient, diffuse, specular, attenuation)
    
        
#        glLightfv(GL_LIGHT0, GL_AMBIENT, self._ambient.GetGLColour())
#        glLightfv(GL_LIGHT0, GL_DIFFUSE, self._diffuse.GetGLColour())
#        glLightfv(GL_LIGHT0, GL_SPECULAR, self._specular.GetGLColour())
#        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.0)#self._attenuation)
#        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 1.0)#self._attenuation)
#        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0)#self._attenuation)
        
    
    def draw(self):
        self._setup_draw()
        # Nothing
        self._teardown_draw()
        
        pass
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, self._ambient.get_gl_colour())
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self._diffuse.get_gl_colour())
        glLightfv(GL_LIGHT0, GL_SPECULAR, self._specular.get_gl_colour())
        
        # OpenGL uses the MODELVIEW matrix which should already have the lights
        # position from the transform of the Light's parent.
        
        pos = self.parent.position
        pos  = CreateGLArray(GLfloat, (pos.x, pos.y, pos.z, 1.0), 4 )

#        pos  = CreateGLArray(GLfloat, (0, 0, 0, 1.0), 4 )
        
#        glDisable(GL_LIGHTING)
#        glDisable(GL_BLEND)
            
        glBegin(GL_LINE_LOOP)
        vt = Vector3()
        
        # On x-axis
        radius = 0.25
        for i in range(0, 50):
            vt.x = math.cos((2*math.pi/50)*i) * 0.25
            vt.y = math.sin((2*math.pi/50)*i) * 0.25
            vt.z = 0
            glVertex3f(vt.x,vt.y,vt.z)
        glEnd()
        
        glBegin(GL_LINE_LOOP)
        vt = Vector3()
        # On z-axis
        for i in range(0, 50):
            vt.x = 0
            vt.z = math.cos((2*math.pi/50)*i) * 0.25
            vt.y = math.sin((2*math.pi/50)*i) * 0.25
            glVertex3f(vt.x,vt.y,vt.z)
        glEnd()
        
        
#        glEnable(GL_LIGHTING)
#        glEnable(GL_BLEND)
            
        
        glLightfv(GL_LIGHT0, GL_POSITION, pos)
        pass
        
class Light(Node):
    def __init__(self):
        Node.__init__(self, name="default_light", light=GLLight(), renderer=None)
        
