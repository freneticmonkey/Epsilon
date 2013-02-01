'''
Created on Sep 22, 2011

@author: scottporter
'''
from OpenGL.GL import *

from epsilon.render.colour import Preset
from epsilon.render.texturemanager import TextureManager
from epsilon.render.texture import Texture
from epsilon.render.shadermanager import ShaderManager
from epsilon.render.glutilities import *

from epsilon.logging.logger import Logger
 
class BaseMaterial(object):
    
    def __init__(self, ambient=None, diffuse=None, specular=None, emission=None, shininess=None):
        if not ambient:
            ambient = Preset.white
        if not diffuse:
            diffuse = Preset.white
        if not specular:
            specular = Preset.white
        if not emission:
            emission = Preset.black
        if not shininess:
            shininess = 0.5
        
        self._ambient = ambient
        self._diffuse = diffuse
        self._specular = specular
        self._emission = emission
        self._shininess = shininess
        self._tex_name = None
        self._tex_obj = None
        
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
    def emission(self):
        return self._emission
    
    @emission.setter
    def emission(self, new_colour): 
        self._emission = new_colour
    
    @property
    def shininess(self):
        return self._shininess
    
    @shininess.setter
    def shininess(self, new_shine): 
        self._shininess = new_shine
        
    @property
    def texture(self):
        return self._tex_name
    
    @texture.setter
    def texture(self, new_tex):
        the_texture = None
        if isinstance(new_tex, Texture):
            the_texture = new_tex
        
        elif isinstance(new_tex, str):
            # Get Texture from TextureManager
            the_texture = TextureManager.get_instance().get_texture(new_tex)
            
        if the_texture is not None:
            self._tex_obj = the_texture
            self._tex_name = the_texture.name
        else:
            Logger.Log("Can't find texture: %s" % new_tex)
        
class GLMaterial(BaseMaterial):
    def __init__(self, ambient=None, diffuse=None, specular=None, emission=None, shininess=None):
        BaseMaterial.__init__(self, ambient, diffuse, specular, emission, shininess)
        
        # Set default Shader        
        self._shader = None
        self.shader = "phong_simple"
        
    @property
    def shader(self):
        return self._shader
    
    @shader.setter
    def shader(self, new_shader):
        # If the parameter is a string name of the shader
        if isinstance(new_shader, str):
            # Get the appropriate shader from the ShaderManager
            self._shader = ShaderManager.get_instance().get_shader(new_shader)
        else:
            # Otherwise treat it as an instanced shader
            self._shader = new_shader
            
    def draw(self, mesh):
#        glMaterialfv(GL_FRONT, GL_AMBIENT, self._ambient.get_gl_colour())
#        glMaterialfv(GL_FRONT, GL_DIFFUSE, self._diffuse.get_gl_colour())
#        glMaterialfv(GL_FRONT, GL_SPECULAR, self._specular.get_gl_colour())
#        glMaterialfv(GL_FRONT, GL_EMISSION, self._emission.get_gl_colour())
#        glMaterialf(GL_FRONT, GL_SHININESS, self._shininess * 128)
                
        if self._tex_obj is not None:
            self._tex_obj.set()
        
        # If a Shader has been defined for this material
        if self._shader:
            with self._shader as shader:
                shader.render(self, mesh)
                
        if self._tex_obj is not None:
            self._tex_obj.unset()
        
        
        