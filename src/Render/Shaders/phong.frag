varying vec3 normal, eyeVec, lightDir;

struct Material 
{
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
    float shininess;
};

uniform Material material;
uniform vec4 Global_ambient;

void main ()
{   
    vec4 final_color = Global_ambient;//gl_FrontLightModelProduct.sceneColor;
    vec3 N = normalize(normal);
    vec3 L = normalize(lightDir);
    float lambertTerm = dot(N,L);
    lambertTerm = clamp(lambertTerm, 0.0, 1.0);
    
    if (lambertTerm > 0.0)
    {
//        final_color += gl_LightSource[0].ambient * material.ambient;
        final_color += gl_LightSource[0].diffuse * material.diffuse * lambertTerm;
//        final_color += gl_LightSource[0].diffuse * gl_FrontMaterial.diffuse * lambertTerm;
//        vec3 E = normalize(eyeVec);
//        vec3 R = normalize(-reflect(L, N));   // <=== This is broken.
//        float specular = max(pow(dot(R,E), material.shininess), 0.0);//gl_FrontMaterial.shininess);
//        //final_color += gl_LightSource[0].specular * gl_FrontMaterial.specular * specular;
//        final_color += gl_LightSource[0].specular * specular;
    }
//    else
//    {
//        final_color = gl_LightSource[0].ambient * material.ambient * -lambertTerm;
//    }
    gl_FragColor = final_color;
}