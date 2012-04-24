'''
Created on Sep 22, 2011

@author: scottporter
'''
from Render.Colour import Preset
from Render.TextureManager import TextureManager
from Render.ShaderManager import ShaderManager
from Render.GLUtilities import *
from OpenGL.GL import *
 
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
    def texture(self, tex_name):
        # Get Texture from TextureManager
        tex = TextureManager.get_instance().get_texture(tex_name)
        if tex is not None:
            self._tex_obj = tex
            self._tex_name = tex_name
        
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
        
        
        