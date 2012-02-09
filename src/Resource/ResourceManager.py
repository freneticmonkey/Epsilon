'''
Created on Nov 19, 2011

@author: scottporter
'''
import os
from xml.etree import ElementTree as ET

from Core.BaseSingleton import BaseSingleton

from Render.ShaderManager import ShaderManager
from Render.TextureManager import TextureManager

from Scene.SceneManager import SceneManager

from Scene.Node import Node
from Geometry.euclid import Vector3, Quaternion
from Render.Colour import Colour
from Render.MeshFactory import MeshTypesString, MeshFactory

class ResourceManager(BaseSingleton):
    
    def __init__(self):
        self._shader_manager = ShaderManager.get_instance()
        self._texture_manager = TextureManager.get_instance()

class InvalidSceneFormat(Exception): pass
    
class SceneLoader(object):
    
    node_inc = 0
    
    @classmethod
    def get_node_id(cls):
        cls.node_inc += 1
        return cls.node_inc
    
    def __init__(self):
        self._scene_manager = SceneManager.get_instance()
        
        self._scene = None
    
    def load_scene_file(self, filepath):
        
        if not os.path.exists(filepath):
            raise
        
        xml_dom = ET.parse(filepath)
        
        xml_root = xml_dom.getroot()
        
        self.parse_node(xml_root)
                
    # Recursive compatible XML parsing function.  Only problem is that the line
    # number is not printed when an error occurs.  Switching to a different XML
    # library such as lxml (http://lxml.de) could solve this, but adds additional
    # dependencies...
    # @param node: an xml node.
    # @param parent: a Node() object that is the parent of the current node
    def parse_node(self, node, parent=None):
        node_parent = None
        node_name = None
        
        if "name" in node.attrib:
            node_name = node.attrib["name"]
                
        if node.tag == "scene":
            if node_name is None:
                node_name = "default_scene" 
            
            self._scene = Node(name=node_name)
            node_parent = self._scene
        
        elif node.tag == "camera":
            if node_name is None:
                node_name = "default_camera"
            node_parent = Node(name=node_name)
                    
        elif node.tag == "light":
            if node_name is None:
                node_name = "default_light"
            node_parent = Node(name=node_name)
        
        elif node.tag == "node":
            if node_name is None:
                node_name = "node" + str(SceneLoader.get_node_id())
            node_parent = Node(name=node_name)
            
        # Child Nodes
        
        # Transform
        if node.tag == "transform":
            if not parent is None:
                if "position" in node.attrib:
                    coord = node.attrib["position"].split(" ")
                    if len(coord) == 3:
                        coord = Vector3(float(coord[0]), float(coord[1]), float(coord[2]) )
                    else:
                        print "Invalid position: [%s]" % (" ".join(coord))
                        
                    parent.position = coord
                
                if "rotation" in node.attrib:
                    rot = node.attrib["rotation"].split(" ")
                    if len(rot) == 4:
                        rot = Quaternion().new_rotate_axis(float(rot[0]), Vector3(float(rot[1]),float(rot[2]),float(rot[3])))
                    else:
                        print "Invalid rotation: [%s]" % (" ".join(rot))
                        
                    parent.rotation = rot
                    
                if "scale" in node.attrib:
                    scale = node.attrib["scale"].split(" ")
                    if len(scale) == 3:
                        scale = Vector3(float(scale[0]), float(scale[1]), float(scale[2]) )
                    else:
                        print "Invalid scale: [%s]" % (" ".join(scale))
                    parent.scale = scale
        # Colour
        if node.tag == "colour":
            if not parent is None and not parent.light is None:
                if "ambient" in node.attrib:
                    rgba = node.attrib["ambient"].split(" ")
                    if len(rgba) == 4:
                        rgba = Colour(float(rgba[0]), float(rgba),float(rgba[2]),float(rgba[3]))
                    else:
                        print "Invalid rgba value: [%s]" % (" ".join(rgba))
                    
                    parent.light.diffuse = rgba
                
                if "diffuse" in node.attrib:
                    rgba = node.attrib["diffuse"].split(" ")
                    if len(rgba) == 4:
                        rgba = Colour(float(rgba[0]), float(rgba),float(rgba[2]),float(rgba[3]))
                    else:
                        print "Invalid rgba value: [%s]" % (" ".join(rgba))
                    
                    parent.light.diffuse = rgba
                
                if "specular" in node.attrib:
                    rgba = node.attrib["specular"].split(" ")
                    if len(rgba) == 4:
                        rgba = Colour(float(rgba[0]), float(rgba),float(rgba[2]),float(rgba[3]))
                    else:
                        print "Invalid rgba value: [%s]" % (" ".join(rgba))
                    
                    parent.light.diffuse = rgba
                        
        if node.tag == "attenuation":
            if not parent is None and not parent.light is None:
                if "value" in node.attrib:
                    atten = node.attrib["value"].split(" ")
                    if len(atten) == 1:
                        atten = float(atten)
                    else:
                        print "Invalid attenuation: [%s]" % (str(atten))
                        
                    parent.light.attenuation = float(atten)
        
        # Mesh
        
        # This currently doesn't check if the node is a Light or camera.  Needs fixing
        if node.tag == "mesh":
            if not parent is None:
                if "preset" in node.attrib:
                    preset = node.attrib["preset"]
                    if preset in MeshTypesString.MESHES:
                        parent.mesh = MeshFactory.GetMesh(MeshTypesString.MESHES[preset])
                    else:
                        print "Invalid Mesh Preset: [%s]" % ( preset )
                        
                if "file" in node.attrib:
                    pass # NYI
                
        if node.tag == "children":
            if not parent is None:
                pass
                
                        
        
                    
                    
        
        
        
            
            
            
            
        
        
