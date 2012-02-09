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
//                      in vec3 frag_pos
                      ) 
{
    
    // recalculate distance to the fragment
//    distance = abs( length( light_pos.xyz - frag_pos));
    
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
                                1.0 / (
                                       attenuations.x + 
                                       (attenuations.y * distance) +
                                       (attenuations.z * distance * distance)
                                       ),
                                0.0,
                                1.0
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

//varying vec3 N;
varying vec4 v;  
varying vec3 dist_vec;

void main() 
{
    vec4 fragColor = Global_ambient * material.ambient;
//    fragColor = vec4(normalize(EC_Light_location[0]),1.0);
    int i,j;
    vec3 weight;
    for (i=0;i<1;i++) 
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
                                        lights[j+ATTENUATION]//,
//                                        v.xyz
                                        );
        fragColor = (
                     fragColor 
                     + (lights[j+AMBIENT] * material.ambient * weights.x)
                     + (lights[j+DIFFUSE] * material.diffuse * weights.y)
                     + (lights[j+SPECULAR] * material.specular * weights.z  )
                     );
        weight = weights;
    }
//    //fragColor = vec4(Light_distance[1],Light_distance[0],Light_distance[2],1.0);
//    fragColor = vec4(weight.x,weight.y,weight.z,1.0);
//    gl_FragColor = vec4((Light_distance[0]/4.0),0.0,0.0, 1.0);
//    gl_FragColor = vec4(normalize(dist_vec), 1.0);
    gl_FragColor = fragColor;
//    
//    vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
//    vec3 E = normalize(-v); // we are in Eye Coordinates, so EyePos is (0,0,0)  
//    vec3 R = normalize(-reflect(L,N));  
//    
//    //calculate Ambient Term:  
//    vec4 Iamb = gl_FrontLightProduct[0].ambient;    
//    
//    //calculate Diffuse Term:  
//    vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(N,L), 0.0);
//    Idiff = clamp(Idiff, 0.0, 1.0);     
//    
//    // calculate Specular Term:
//    vec4 Ispec = gl_FrontLightProduct[0].specular 
//    * pow(max(dot(R,E),0.0),0.3*gl_FrontMaterial.shininess);
//    Ispec = clamp(Ispec, 0.0, 1.0); 
    // write Total Color:  
    //gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec;
//    gl_FragColor = vec4(L, 1.0);
}