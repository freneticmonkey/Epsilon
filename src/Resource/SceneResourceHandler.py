'''
Created on Mar 4, 2012

@author: scottporter
'''
from os.path import exists

from xml.etree import ElementTree as ET

from Logging import Logger

from ResourceHandler import ResourceHandlerBase
from ResourceManager import ResourceManager
from Resource.ResourceBase import ResourceType, ResourceBase

from Geometry.euclid import Vector3, Quaternion

from Scene.Node import Node
from Scene.SceneBase import SceneBase
from Scene.SceneManager import SceneManager

from Scripting import TestScripts

#from Render.ShaderManager import ShaderManager
#from Render.TextureManager import TextureManager
from Render.Camera import CameraGL
from Render.Light import GLLight
from Render.Colour import Colour
from Render.Material import BaseMaterial, GLMaterial
from Render.MeshFactory import MeshTypesString, MeshFactory

class InvalidSceneFormat(Exception): pass

from Logging.Logger import ClassLogger

class SceneResourceHandlerLog(ClassLogger):
    
    def __init__(self):
        ClassLogger.__init__(self)
        self._classname = "SceneResourceHandler"
    
class SceneResourceHandler(ResourceHandlerBase):
    
    def __init__(self):
        ResourceHandlerBase.__init__(self)
        
        self._scene_manager = SceneManager.get_instance()
        self._resource_type = ResourceType.SCENE
        self._filetypes = ["xml"]
        self._log = SceneResourceHandlerLog()
        
    def process_resource(self, filename):
        
        new_scene = None
        
        try:
            xml_dom = ET.parse(filename)
            
            xml_root = xml_dom.getroot()
            
            load_scene = self.parse_node(xml_root)
            
            # If successful in parsing the scene file
            if not load_scene is None:
                
                new_scene = SceneBase(filename=filename, root=load_scene)
                
                self._scene_manager.add_scene(new_scene)
            
        except Exception, e:
            self._log.Log("Could not parse scene in filename: %s\nERROR: %s" % (filename, e.message))
            
        return new_scene
                
    # Recursive compatible XML parsing function.  Only problem is that the line
    # number is not printed when an error occurs.  Switching to a different XML
    # library such as lxml (http://lxml.de) could solve this, but adds additional
    # dependencies...
    # @param node: an xml node.
    # @param parent: a Node() object that is the parent of the current node
    def parse_node(self, node, parent=None):
        
        
        current_node = None
        node_name = None
        
        if "name" in node.attrib:
            node_name = node.attrib["name"]
                
        if node.tag == "scene":
            if node_name is None:
                node_name = "default_scene" 
            
            current_node = Node(name=node_name)
        
        elif node.tag == "camera":
            current_node = CameraGL()
            # SIGH - There is no scene at this point because the loading has just begun
            # If the current scene doesn't yet have an active camera
#            if not parent is None and \
#               isinstance(parent, Node) and \
#               parent.scene.active_camera is None:
#                # Set this camera as the active camera
#                parent.scene.active_camera = current_node
                    
            if not node_name is None:
                current_node.name = node_name
                        
        elif node.tag == "light":
            if node_name is None:
                node_name = "default_light"
            current_node = GLLight(name=node_name)
        
        elif node.tag == "node":
            current_node = Node()
        
        # Child Nodes
        
        # Transform
        elif node.tag == "transform":
            if not parent is None:
                if "position" in node.attrib:
                    coord = node.attrib["position"].split(" ")
                    if len(coord) == 3:
                        coord = Vector3(float(coord[0]), float(coord[1]), float(coord[2]) )
                    else:
                        self._log.Log("Invalid position: [%s]" % (" ".join(coord)))
                        
                    parent.position = coord
                
                if "rotation" in node.attrib:
                    rot = node.attrib["rotation"].split(" ")
                    if len(rot) == 4:
                        rot = Quaternion().new_rotate_axis(float(rot[0]), Vector3(float(rot[1]),float(rot[2]),float(rot[3])))
                    else:
                        self._log.Log( "Invalid rotation: [%s]" % (" ".join(rot)) )
                        
                    parent.rotation = rot
                    
                if "scale" in node.attrib:
                    scale = node.attrib["scale"].split(" ")
                    if len(scale) == 3:
                        scale = Vector3(float(scale[0]), float(scale[1]), float(scale[2]) )
                    else:
                        self._log.Log( "Invalid scale: [%s]" % (" ".join(scale)) )
                    parent.local_scale = scale
        # Colour
        elif node.tag == "colour":
            if not parent is None and isinstance(parent, GLLight) or isinstance(parent, BaseMaterial):
                if "ambient" in node.attrib:
                    parent.ambient = Colour.from_string(node.attrib["ambient"])
                
                if "diffuse" in node.attrib:
                    parent.diffuse = Colour.from_string(node.attrib["diffuse"])
                
                if "specular" in node.attrib:
                    parent.specular = Colour.from_string(node.attrib["specular"])
                        
        elif node.tag == "attenuation":
            if not current_node is None and isinstance(current_node, GLLight):
                if "value" in node.attrib:
                    atten = node.attrib["value"].split(" ")
                    if len(atten) == 1:
                        atten = float(atten)
                    else:
                        self._log.Log( "Invalid attenuation: [%s]" % (str(atten)) )
                    
                    if isinstance(parent, GLLight):
                        parent.attenuation = float(atten)
        
        # Mesh
        elif node.tag == "mesh":
            if not isinstance(parent, GLLight) or not isinstance(parent, CameraGL):
                if "preset" in node.attrib:
                    preset = node.attrib["preset"]
                    if preset in MeshTypesString.MESHES:
                        parent.mesh = MeshFactory.GetMesh(MeshTypesString.MESHES[preset])
                    else:
                        self._log.Log( "Invalid Mesh Preset: [%s]" % ( preset ) )
                        
                if "file" in node.attrib:
                    # Load the mesh
                    mesh = ResourceManager.get_instance().process_resource(node.attrib["file"])
                    # Set it to the node
                    parent.mesh = mesh
        
        # Children        
        elif node.tag == "children":
            if not parent is None:
                # Get the child nodes of the children Element
                
                children = node.getchildren()
                
                # Process each of the child elements found.
                for child in children:
                    self.parse_node(child, parent)
            
        # Scripts
        elif node.tag == "scripts":
            if not parent is None:
                # Get the scripts applied to this node
                scripts = node.getchildren()
                
                # Process and attach each of the scripts
                for script in scripts:
                    self.parse_node(script, parent)
                    
        elif node.tag == "script":
            # If this tag is used as a child tag of another node.
            if not parent is None:
                script_name = node.attrib["name"]
                parameters = {}
                for key in node.attrib:
                    if not key == "name":
                        parameters[key] = node.attrib[key]
                        
                # The current limitation of this is that the only scripts that can be used
                # are the ones listed in TestScripts.  TBD: Change to dynamic import, allow
                # files to be included in the scene description.
                
                # The python files listed in the scene definition need to be parsed and loaded
                # into the engine before this parsing occurs if this is to be made more
                # flexible
                
                # Create the Script
                script = None
                try:
                    script = getattr(TestScripts, script_name)
                    new_script = script()
                except Exception, e:
                    self._log.Log("Could not create Script with name: " + script_name)
                
                if not script is None:
                    try:
                        # Initialise it using the parameters in the XML
                        
                        new_script.init_parameters(parameters)
                        parent.AddScript(new_script)
                    except Exception, e:
                        self._log.Log("Invalid parameters for script: " + script_name)
        
        elif node.tag == "material":
            if not parent is None and isinstance(parent, Node):
                # Set the material of the parent as the parent
                # so that when the child XML tags are passed they assign
                # their values to the material
#                if not parent.material is None:
#                    parent = parent.material
                    
                parent.material = GLMaterial()
                    
                # Get any properties of the material
                properties = node.getchildren()
                
                # Process and attach each of the scripts
                for property in properties:
                    self.parse_node(property, parent.material)
        
        # Resources
        elif node.tag == "texture":
            
            # If the texture is referenced by filename
            if "filename" in node.attrib:
                # Load the texture
                texture = ResourceManager.get_instance().process_resource(node.attrib["filename"])
            
            if not texture is None:
                if "name" in node.attrib:
                    texture.name = node.attrib["name"]
            
            # If the current parent is a Material node, set the material node's texture 
            if not parent is None and not texture is None and isinstance(parent, BaseMaterial):
                parent.texture = texture.filename
        
#        elif node.tag == "shader":
#            pass
        
        # Unknown XML tag    
        else:
            self._log.Log("WARNING: Unknown XML Tag: " + node.tag)
        
        # If it's not a node that has already had it's children processed
        if not node.tag in ["children","scripts","material"]:
            # Get the Element children of the current XML Element
            children = node.getchildren()
            
            # Process each of the child elements found.
            for child in children:
                self.parse_node(child, current_node)
        
        # If a parent Node is defined add the current node to it
        if not parent is None and not current_node is None:
            parent.AddChild(current_node)
            
        return current_node
        