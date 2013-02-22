from epsilon.render.windowrenderer import GLWindowRenderer

from epsilon.core.basemanager import BaseSingleton

class RenderManager(BaseSingleton):
    
    def __init__(self):
        # create a renderer
        self._renderer = GLWindowRenderer()

        self._render_queue = []
        
    def __del__(self):
        del self._renderer
        
    def init(self, width, height, title):
        self._renderer.init(width, height, title)
        
    def set_camera(self, camera):
        self._renderer.camera = camera
        
    def cull(self):
        self._renderer.cull()

    def draw(self):
        self._renderer.draw()      