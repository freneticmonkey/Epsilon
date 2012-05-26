'''
Created on Apr 4, 2012

@author: scottporter
'''

from Geometry.euclid import Vector2, Vector3

from ShaderNodeBase import ShaderVariable
from ShaderNodeBase import ShaderProperty
from ShaderNodeBase import ShaderDataType
from ShaderNodeBase import ShaderNodeBase
from ShaderNodeBase import ConnectionSocket
from ShaderNodeBase import ConnectionType

# Connection Types
from Render import Colour

# Input/Settings Nodes
material_source = """
struct Material
{
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
    float emit;
    float alpha;
    vec2 uv;
}
"""
class MaterialNode(ShaderNodeBase):
    def _process_connections(self):
        material_name = ShaderVariable("material")
        ambient = ConnectionSocket.create(self, ConnectionType.OUTPUT, "ambient", Colour.Preset.white, "<ambient>",ShaderDataType.VECTOR4)
        diffuse = ConnectionSocket.create(self, ConnectionType.OUTPUT, "diffuse", Colour.Preset.white, "<diffuse>",ShaderDataType.VECTOR4)
        specular = ConnectionSocket.create(self, ConnectionType.OUTPUT, "specular", Colour.Preset.white, "<specular>",ShaderDataType.VECTOR4)
        
        emit = ConnectionSocket.create(self, ConnectionType.OUTPUT, "emit", 0.1, "<emit>",ShaderDataType.FLOAT)
        alpha = ConnectionSocket.create(self, ConnectionType.OUTPUT, "alpha", Colour.Preset.white, "<alpha>",ShaderDataType.VECTOR4)
        
        uv_coord = ConnectionSocket.create(self, ConnectionType.OUTPUT, "uv", Colour.Preset.white, "<uv>",ShaderDataType.VECTOR2)
        
        self._definition = material_source
        self._call_format = "uniform Material " + material_name.name + ";"
    
class RGB(ShaderNodeBase):
    pass
    
# Data Nodes

class TextureNode(ShaderNodeBase):
    def _process_connections(self):
        texture_name = ShaderVariable("texture" )
        
        texture = ConnectionSocket.create(self, ConnectionType.OUTPUT, "texture", None, "<texture>",ShaderDataType.IMAGE_BUFFER)
        
        uv_coord = ConnectionSocket.create(self, ConnectionType.INPUT, "uv", Vector2.zero, "<uv>",ShaderDataType.VECTOR2)
        
        output = ConnectionSocket.create(self, ConnectionType.OUTPUT, "colour", Colour.Preset.white, "<colour>",ShaderDataType.VECTOR4)
        
        self._definition = "uniform sampler2d " + texture_name.name + ";"
        self._call_format = output.placeholder + " = texture2d(" + texture_name.placeholder + "," + uv_coord.placeholder + ");"
    
class ImageNode(ShaderNodeBase):
    pass

class VertexNode(ShaderNodeBase):
#    position = ConnectionSocket.create(self, ConnectionType.OUTPUT, "position", Vector3.zero, "<position>",ShaderDataType.VECTOR3)
#    normal = ConnectionSocket.create(self, ConnectionType.OUTPUT, "normal", Vector3.zero, "<normal>",ShaderDataType.VECTOR3)
    
    pass

# Output Nodes

class CompositeOutputNode(ShaderNodeBase):
    pass

class ViewerOutputNode(ShaderNodeBase):
    def _process_connections(self):
        output = ConnectionSocket.create(self, ConnectionType.INPUT, "output", Colour.Preset.white, "<output>", ShaderDataType.VECTOR4)
        
        self._call_format = "gl_FragColor = " + output.placeholder + ";"

class FileOutputNode(ShaderNodeBase):
    pass

# Colour Nodes

mix_source = """
vec4 mix(in vec4 colour1, in vec4 colour2, in float factor)
{
    return colour1 * factor + colour2 * (1.0 - factor);
}
"""
class MixNode(ShaderNodeBase):
    
    def _process_connections(self):
        # Inputs
        colour1 = ConnectionSocket.create(self, ConnectionType.INPUT, "colour", Colour.Preset.white, "<colour_one>",ShaderDataType.VECTOR4)
        colour2 = ConnectionSocket.create(self, ConnectionType.INPUT, "colour",Colour.Preset.white, "<colour_two>",ShaderDataType.VECTOR4)
        factor = ConnectionSocket.create(self, ConnectionType.INPUT, "factor", 0.5, "<factor>",ShaderDataType.FLOAT)
        
        # Output
        out_colour = ConnectionSocket.create(self, ConnectionType.OUTPUT, "colour","<colour_output>",ShaderDataType.VECTOR4)
    
        # define functions that this node is wrapping and the function call format based on the connections above
        self._definition = mix_source
        self._call_format = out_colour.placeholder + " = mix(" + colour1.placeholder + "," + colour2.placeholder + "," + factor.placeholder + ")"
        
        
invert_source = """
vec4 invert(in vec4 input, in bool rgb, in bool alpha)
{
    vec4 output = input;
    if (rgb)
    {
        output.x = 255 - input.x;
        output.y = 255 - input.y;
        output.z = 255 - input.z;
    }
    if (alpha)
    {
        output.a = 1.0 - input.a;
    }
    return output;
}
"""
        
class InvertNode(ShaderNodeBase):
    
    def _process_connections(self):
        #Input
        colour = ConnectionSocket.create(self, ConnectionType.INPUT, "colour", Colour.Preset.white, "<colour_one>",ShaderDataType.VECTOR4)
        rgb = ShaderProperty.create(self, "rgb", True, "<rgb>",ShaderDataType.BOOL)
        alpha = ShaderProperty.create(self, "alpha", False, "<alpha>",ShaderDataType.BOOL)
        
        out_colour = ConnectionSocket.create(self, ConnectionType.OUTPUT, "colour", "<colour_output>", ShaderDataType.VECTOR4)

        self._definition = invert_source
        self._call_format = out_colour.placeholder + " = invert(" + colour.placeholder + "," + rgb.placeholder + "," + alpha.placeholder + ")"
        
        