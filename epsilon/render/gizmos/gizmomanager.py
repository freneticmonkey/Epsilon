
from epsilon.core.basemanager import BaseSingleton
from epsilon.geometry.euclid import Vector3
from epsilon.render.gizmos.gizmos import WireSphere, WireCube, WirePlane, Line
from epsilon.scene.node import Node

class GizmoManager(BaseSingleton):
    
    available_gizmos = {'WireSphere' : WireSphere,
                        'WireCube' : WireCube,
                        'Line' : Line
                        }
    
    @classmethod
    def draw_sphere(cls, pos, radius=1.0):
        new_sphere = WireSphere(pos, radius)
        cls.get_instance().add_gizmo(new_sphere)
        
        return new_sphere
    
    @classmethod
    def draw_cube(cls, pos, width=None, height=None, depth=None, max=Vector3(), min=Vector3()):
        new_cube = WireCube(pos, width, height, depth, max, min)
        cls.get_instance().add_gizmo(new_cube)
        return new_cube
    
    @classmethod
    def draw_line(cls, pos, dir=Vector3(), length=1.0):
        new_line = Line(pos, dir, length)
        cls.get_instance().add_gizmo(new_line)
        return new_line
    
    @classmethod
    def draw_plane(cls, pos, normal=Vector3.UP(), size=1.0):
        new_plane = WirePlane(pos, normal, size)
        cls.get_instance().add_gizmo(new_plane)
        return new_plane
    
    def __init__(self):
        self._gizmo_root = Node('gizmo_root')
        self._gizmo_root.transform.scale = Vector3(0.5, 0.5, 0.5)
        
    def add_gizmo(self, new_gizmo):
        self._gizmo_root.transform.add_child(new_gizmo.transform)
        
    def remove_gizmo(self, del_gizmo):
        self._gizmo_root.transform.remove_child(del_gizmo.transform)
            
    def draw(self):
        self._gizmo_root.draw()