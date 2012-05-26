from epsilon.render.renderer import GLRenderer

from epsilon.core.basemanager import BaseSingleton

class RenderManager(BaseSingleton):
    
    def __init__(self):
        # create a renderer
        self._renderer = GLRenderer()
        
    def __del__(self):
        del self._renderer
        
    def init(self, width, height, title):
        self._renderer.init(width, height, title)
        
    def set_camera(self, camera):
        self._renderer.camera = camera
        
    def draw(self):
        self._renderer.draw()      