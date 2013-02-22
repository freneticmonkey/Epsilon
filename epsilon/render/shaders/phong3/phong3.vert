
#version 330

//out vec3 lightDir;//, eyeVec;
//out vec2 Vertex_texture_coordinate_var;

layout(location=0) in vec4 position;
layout(location=1) in vec3 normal;
layout(location=2) in vec4 colour;
layout(location=3) in vec2 texture_coordinate;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;
uniform vec3 lightPosition;

out vec3 lightDir;
out vec3 theNormal;
out vec4 vertColour;
smooth out vec2 texCoord;
//in mat3 normalMatrix;

//out vec3 thelightPosition;
//out mat3 normalsMatrix;

void main()
{
    /*
    //normal = gl_NormalMatrix * Vertex_normal;//gl_Normal;
    vec4 vVertex = gl_ModelViewMatrix * vec4(Vertex_position, 1.0);//gl_Vertex;
    //eyeVec = -vVertex.xyz;
    lightDir = vec3(gl_LightSource[0].position.xyz - vVertex.xyz);
    gl_Position = gl_ModelViewProjectionMatrix * vec4( 
                                                      Vertex_position, 1.0
                                                      );
    Vertex_texture_coordinate_var = Vertex_texture_coordinate;
    */

    /*
    normalsMatrix = normalMatrix;

    vec4 vVertex = modelViewMatrix * vec4(position, 1.0);//gl_Vertex;
    lightDir = vec3(lightPosition - vVertex.xyz);
    gl_Position = modelViewProjMatrix * vec4(position, 1.0);
    Vertex_texture_coordinate_var = texture_coordinate;
    */
    vertColour = colour;
    //texCoord = vec2((normal.x / 2.0 + 0.5), (normal.y / 2.0 + 0.5) );
    texCoord = texture_coordinate;
    theNormal = normal;
    vec4 worldPosition = position * model;
    lightDir = vec3(lightPosition - worldPosition.xyz);

    gl_Position = position * model * view * proj;

    //gl_Position = position * cameraModelViewMatrix *  cameraProjMatrix;
    //gl_Position = cameraProjMatrix * cameraModelViewMatrix * modelViewMatrix * position;
}
