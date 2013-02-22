
from epsilon.core.basemanager import BaseSingleton
from epsilon.geometry.euclid import Vector3
from epsilon.render.gizmos.gizmos import WireSphere, WireCube, WirePlane, Line
from epsilon.render.colour import Preset
from epsilon.scene.node import Node

class GizmoManager(BaseSingleton):
    
    available_gizmos = {'WireSphere' : WireSphere,
                        'WireCube' : WireCube,
                        'Line' : Line,
                        'WirePlane' : WirePlane
                        }
    
    @classmethod
    def draw_sphere(cls, pos, radius=1.0):
        new_sphere = WireSphere(pos, radius)
        cls.get_instance()._add_gizmo(new_sphere)
        
        return new_sphere
    
    @classmethod
    def draw_cube(cls, pos, width=None, height=None, depth=None, max=Vector3(), min=Vector3(), colour=Preset.white):
        new_cube = WireCube(pos, width, height, depth, max, min, colour)
        cls.get_instance()._add_gizmo(new_cube)
        return new_cube
    
    @classmethod
    def draw_line(cls, pos, dir=Vector3(), length=1.0, colour=None):
        new_line = Line(pos, dir, length, colour)
        cls.get_instance()._add_gizmo(new_line)
        return new_line
    
    @classmethod
    def draw_plane(cls, pos, normal=Vector3.UP(), size=1.0, colour=Preset.white):
        new_plane = WirePlane(pos, normal, size, colour)
        cls.get_instance()._add_gizmo(new_plane)
        return new_plane

    @classmethod
    def remove_gizmo(cls, del_gizmo):
        cls.get_instance()._remove_gizmo(del_gizmo)
    
    def __init__(self):
        self._gizmo_root = Node('gizmo_root')
        self._gizmo_root.transform.scale = Vector3(0.5, 0.5, 0.5)
        
    def _add_gizmo(self, new_gizmo):
        self._gizmo_root.transform.add_child(new_gizmo.transform)
        
    def _remove_gizmo(self, del_gizmo):
        self._gizmo_root.transform.remove_child(del_gizmo.transform)

    def get_gizmo_root(self):
        return self._gizmo_root