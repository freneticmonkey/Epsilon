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

vec3 phong_weightCalc( 
                      in vec3 light_pos, // light position/direction
                      in vec3 half_light, // half-way vector between light and view
                      in vec3 frag_normal, // geometry normal
                      in float shininess, // shininess exponent
                      in float distance, // distance for attenuation calculation...
                      in vec4 attenuations // attenuation parameters...
                      ) 
{
    // returns vec3( ambientMult, diffuseMult, specularMult )
    float n_dot_pos = max( 0.0, dot( 
                                    frag_normal, light_pos
                                    ));
    float n_dot_half = 0.0;
    float attenuation = 1.0;
    if (n_dot_pos > -.05) 
    {
        n_dot_half = pow(
                         max(0.0,dot( 
                                     half_light, frag_normal
                                     )), 
                         shininess
                         );
        if (distance != 0.0) 
        {
            attenuation = clamp(
                                0.0,
                                1.0,
                                1.0 / (
                                       attenuations.x + 
                                       (attenuations.y * distance) +
                                       (attenuations.z * distance * distance)
                                       )
                                );
            n_dot_pos *= attenuation;
            n_dot_half *= attenuation;
        }
    }
    return vec3( attenuation, n_dot_pos, n_dot_half);
}

struct Material 
{
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
    float shininess;
};

uniform Material material;
uniform vec4 Global_ambient;

void main() 
{
    vec4 fragColor = Global_ambient * material.ambient;
    int i,j;
    for (i=0;i<LIGHT_COUNT;i++) 
    {
        j = i* LIGHT_SIZE;
        vec3 weights = phong_weightCalc(
                                        normalize(EC_Light_location[i]),
                                        normalize(EC_Light_half[i]),
                                        baseNormal,
                                        material.shininess,
                                        // some implementations will produce negative values interpolating positive float-arrays!
                                        // so we have to do an extra abs call for distance
                                        abs(Light_distance[i]),
                                        lights[j+ATTENUATION]
                                        );
        fragColor = (
                     fragColor 
                     + (lights[j+AMBIENT] * material.ambient * weights.x)
                     + (lights[j+DIFFUSE] * material.diffuse * weights.y)
                     + (lights[j+SPECULAR] * material.specular * weights.z)
                     );
    }
    //fragColor = vec4(Light_distance[0],Light_distance[1],Light_distance[2],1.0);
    gl_FragColor = fragColor;
}