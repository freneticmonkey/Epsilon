const int LIGHT_COUNT = 3; // Originally this was a python value
const int LIGHT_SIZE = 5;  //         "            "
const int AMBIENT = 0;
const int DIFFUSE = 1;
const int SPECULAR = 2;
const int POSITION = 3;
const int ATTENUATION = 4;
uniform vec4 lights[ LIGHT_COUNT*LIGHT_SIZE ];
varying vec3 EC_Light_half[LIGHT_COUNT];
varying vec3 EC_Light_location[LIGHT_COUNT]; 
varying float Light_distance[LIGHT_COUNT]; 
varying vec3 baseNormal;

//attenuation = clamp(
//                    0.0,
//                    1.0,
//                    1.0 / (
//                           attenuations.x + 
//                           (attenuations.y * distance) +
//                           (attenuations.z * distance * distance)
//                           )
//                    );

// Vertex-shader pre-calculation for lighting...
vec3 phong_preCalc( 
                   in vec3 vertex_position,
                   in vec4 light_position,
                   out float light_distance,
                   out vec3 ec_light_location,
                   out vec3 ec_light_half
                   ) 
{
    // This is the core setup for a phong lighting pass 
    // as a reusable fragment of code.
    // vertex_position -- un-transformed vertex position (world-space)
    // light_position -- un-transformed light location (direction)
    // light_distance -- output giving world-space distance-to-light 
    // ec_light_location -- output giving location of light in eye coords 
    // ec_light_half -- output giving the half-vector optimization
    vec3 ms_vec;
    
    if (light_position.w == 0.0) 
    {
        // directional rather than positional light...
        ec_light_location = normalize(
                                      gl_NormalMatrix *
                                      light_position.xyz
                                      );
        light_distance = 0.0;
    } 
    else 
    {
        // positional light, we calculate distance in 
        // model-view space here, so we take a partial 
        // solution...
        ms_vec = (
                       light_position.xyz -
                       vertex_position
                       );
        vec3 light_direction = gl_NormalMatrix * ms_vec;
        ec_light_location = normalize( light_direction );
        light_distance = abs(length( ms_vec ));
    }
    // half-vector calculation 
    ec_light_half = normalize(
                              ec_light_location + vec3( 0,0,1 )
                              );
    return ms_vec;
}

void light_preCalc( in vec3 vertex_position, out vec3 dist_vec ) 
{
    // This function is dependent on the uniforms and 
    // varying values we've been using, it basically 
    // just iterates over the phong_lightCalc passing in 
    // the appropriate pointers...
    vec3 light_direction;
    for (int i = 0; i< LIGHT_COUNT; i++ ) 
    {
        int j = i * LIGHT_SIZE;
        dist_vec = phong_preCalc(
                      vertex_position,
                      lights[j+POSITION],
                      // following are the values to fill in...
                      Light_distance[i],
                      EC_Light_location[i],
                      EC_Light_half[i]
                      );
    }
}

attribute vec3 Vertex_position;
attribute vec3 Vertex_normal;

//varying vec3 N;
varying vec4 v;
varying vec3 dist_vec;

void main() 
{
    
    //v = gl_ModelViewMatrix * gl_Vertex;//vec4(gl_Vertex,1.0));
    gl_Position = gl_ModelViewProjectionMatrix * vec4( 
                                                      Vertex_position, 1.0
                                                      );
    v = gl_Position;
    baseNormal = gl_NormalMatrix * normalize(Vertex_normal);
    light_preCalc(Vertex_position, dist_vec);
    
}