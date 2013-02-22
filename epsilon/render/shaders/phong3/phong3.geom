#version 150
#extension GL_EXT_geometry_shader4 : enable

in vec3 lightDir; //output normal for frag shader
out vec3 lightDirection;
out vec3 normal;

in vec2 Vertex_texture_coordinate_var;
out vec2 texCoord;

in mat3 normalsMatrix;

//attribute vec3 Vertex_position;
//attribute vec3 Vertex_normal;
//attribute vec2 Vertex_texture_coordinate;

void main( void )
{
    //normal = gl_NormalMatrix * normalize(cross(gl_PositionIn[1].xyz - gl_PositionIn[0].xyz, gl_PositionIn[2].xyz - gl_PositionIn[0].xyz)); //calculate normal for this face
    normal = normalsMatrix * normalize(cross(gl_PositionIn[1].xyz - gl_PositionIn[0].xyz, gl_PositionIn[2].xyz - gl_PositionIn[0].xyz)); //calculate normal for this face
    texCoord = Vertex_texture_coordinate_var;
    //for (int i = 0;i<gl_VerticesIn;i++)
    //{
    //    gl_Position = gl_ModelViewProjectionMatrix * gl_PositionIn[i]; //multiply position by MVP matrix;
    //    EmitVertex();
    //}
    //EndPrimitive();
}