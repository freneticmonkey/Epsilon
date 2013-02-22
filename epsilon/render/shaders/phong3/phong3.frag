
#version 330

// out vec4 fragColour;

// void main()
// {
//     fragColour = vec4(1.0, 0.0, 0.0, 1.0);
// }


in vec3 theNormal, lightDir;
in vec4 vertColour;
in vec2 texCoord;

uniform sampler2D diffuse_texture;

out vec4 fragColour;

void main ()
{
    //fragColour = vec4(0.0, 0.0, 0.0, 1.0);//texture2D(diffuse_texture, texCoord);
    
    vec4 tex_diffuse = texture2D(diffuse_texture, texCoord);
    //vec4 tex_diffuse = vec4(1.0, 0.0, 0.0, 1.0);
   
    vec4 final_color = vec4(0.2, 0.2, 0.2, 1.0);
    
    vec3 N = normalize(theNormal);
    vec3 L = normalize(lightDir);
    float lambertTerm = dot(N,L);
    lambertTerm = clamp(lambertTerm, 0.0, 1.0);
    
    if (lambertTerm > 0.0)
    {
        final_color += vec4(1.0, 1.0, 1.0, 1.0) * vertColour * lambertTerm;
    }
    
    //fragColour = tex_diffuse;

    fragColour = mix(tex_diffuse, final_color, 0.5);
}

/*
in vec3 normal, lightDirection;

in vec2 texCoord;

in struct Material 
{
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
    float shininess;
} material;

in vec4 Global_ambient;
in sampler2D diffuse_texture;

out vec4 fragColour;

void main ()
{
    vec4 tex_diffuse = texture2D(diffuse_texture, texCoord);
    vec4 final_color = Global_ambient;
    vec3 N = normalize(normal);
    vec3 L = normalize(lightDirection);
    float lambertTerm = dot(N,L);
    lambertTerm = clamp(lambertTerm, 0.0, 1.0);
    
    if (lambertTerm > 0.0)
    {
        final_color += gl_LightSource[0].diffuse * material.diffuse * lambertTerm;
    }
    
    fragColour = mix(tex_diffuse, final_color, 0.5);
}
*/