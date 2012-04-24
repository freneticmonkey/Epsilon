"""
    ShaderManager Class
    This class will manage an array of Shaders and access to those Shaders.
    
    For the time being the path to shaders will be hard-coded within the Render.Shaders folder.


"""
import os

from Logging.Logger import ClassLogger
from Render.Shader import *
from Core.BaseManager import FrameListenerManager

_default_shader_path = os.path.join("Render","Shaders")

#_instance = None

#def GetShaderManager():
#    global _instance
#    if _instance is None:
#        _instance = ShaderManager()
#    return _instance

def get_shader_path(shader_filename):
    return os.path.join(_default_shader_path, shader_filename)

class ShaderManagerLog(ClassLogger):
    
    def __init__(self):
        ClassLogger.__init__(self)
        self._classname = "ShaderManager"
    
class ShaderManager(FrameListenerManager):
    
    def init(self):
        self._shaders = {}
        self._smlog = ShaderManagerLog()
        
    def add_shader_object(self, name, new_shader):
        if not name in self._shaders:
            compile_result = new_shader.compile()
            if len(compile_result) > 0:
                print "Compiled " + name + " Shader.\nResult:\n" + compile_result
            self._shaders[name] = new_shader
        else:
            self._smlog.Log("Shader already exists.")
        
    def add_shader_from_files(self, name, vert, frag):
        new_shader = ShaderProgram( VertexShader(get_shader_path(vert)), FragmentShader(get_shader_path(frag)) )
        shader_message = new_shader.compile()  
        if len(shader_message) > 0:
            self._smlog.Log("Shader compile result: " + shader_message)
        
        self._shaders[name] = new_shader
            
#        #lighting shader
#        vs_path = os.path.join("Render", "Shaders", "lighting.vert")
#        fs_path = os.path.join("Render", "Shaders", "lighting.frag")
#        
#        #phong shader
##        vs_path = os.path.join("Render", "Shaders", "lighting.vert")
##        fs_path = os.path.join("Render", "Shaders", "lighting.frag")
#        
#        vs = VertexShader(vs_path)
#        fs = FragmentShader(fs_path)
#        self._shader = ShaderProgram(vs, fs)
#        shader_message = self._shader.Use()  
#        if len(shader_message) > 0:
#            Logger.Log("Shader compile result: " + shader_message)

    def get_shader(self, name):
        if name in self._shaders:
            return self._shaders[name]
        else:
            self._smlog.Log("Requested Shader doesn't exist: " + name)
        
        
    def on_frame_start(self):
        for shader in self._shaders.itervalues():
            shader.on_frame_start()
        
    