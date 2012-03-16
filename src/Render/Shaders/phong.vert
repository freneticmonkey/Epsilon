varying vec3 normal, eyeVec, lightDir;

attribute vec3 Vertex_position;
attribute vec3 Vertex_normal;

void main()
{
    normal = gl_NormalMatrix * Vertex_normal;//gl_Normal;
    vec4 vVertex = gl_ModelViewMatrix * vec4(Vertex_position, 1.0);//gl_Vertex;
    eyeVec = -vVertex.xyz;
    lightDir = vec3(gl_LightSource[0].position.xyz - vVertex.xyz);
    gl_Position = gl_ModelViewProjectionMatrix * vec4( 
                                                      Vertex_position, 1.0
                                                      );
}
