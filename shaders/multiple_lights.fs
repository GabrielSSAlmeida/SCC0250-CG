#version 330 core

out vec4 FragColor;

struct Material {
    sampler2D diffuse;
    float shininess;
};

struct PointLight {
    vec3 position;

    float constant;
    float linear;
    float quadratic;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

struct DirLight {
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};


#define NR_INTERNAL_LIGHTS 1 // Certifique-se de que este número é o máximo que você terá
#define NR_EXTERNAL_LIGHTS 1 // Certifique-se de que este número é o máximo que você terá

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoords;

uniform vec3 viewPos; // Posição da câmera no mundo
uniform PointLight internalLights[NR_INTERNAL_LIGHTS];
uniform PointLight externalLights[NR_EXTERNAL_LIGHTS];
uniform DirLight dirLight;
uniform Material material;

// Novos uniforms para os limites da casa
uniform vec3 houseMinBounds;
uniform vec3 houseMaxBounds;

uniform float global_ka; 
uniform float global_kd; 
uniform float global_ks;

// --- Função modular para iluminação Phong com uma luz pontual ---
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir)
{
    vec3 lightDir = normalize(light.position - fragPos);
    
    // Difuso
    float diff = max(dot(normal, lightDir), 0.0);
    
    // Especular
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = 0.0;
    // Evita cálculo de specular se a luz está atrás da superfície
    if(dot(normal, lightDir) > 0.0)
    {
        spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    }

    // Atenuação
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + 
                               light.quadratic * (distance * distance));
    
    // Cor base da textura
    vec3 texColor = vec3(texture(material.diffuse, TexCoords));
    //vec3 texColorSpec = vec3(texture(material.specular, TexCoords));
    
    // Componentes
    vec3 ambient = light.ambient * texColor * global_ka;   // Multiplica pelo fator ambiente global
    vec3 diffuse = light.diffuse * diff * texColor * global_kd; // Multiplica pelo fator difuso global
    vec3 specular = light.specular * spec * global_ks; // Multiplica pelo fator especular global

    // Aplicar atenuação
    ambient *= attenuation;
    diffuse *= attenuation;
    specular *= attenuation;
    
    return (ambient + diffuse + specular);
}

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir)
{
    vec3 lightDir = normalize(-light.direction);

    // Difuso
    float diff = max(dot(normal, lightDir), 0.0);

    // Especular
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);

    vec3 texColor = vec3(texture(material.diffuse, TexCoords));
    //vec3 texColorSpec = vec3(texture(material.specular, TexCoords));

    vec3 ambient = light.ambient * texColor * global_ka; // Multiplica pelo fator ambiente global
    vec3 diffuse = light.diffuse * diff * texColor * global_kd; // Multiplica pelo fator difuso global
    vec3 specular = light.specular * spec * global_ks; // Multiplica pelo fator especular global

    return (ambient + diffuse + specular);
}


void main()
{
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);

    // Começamos com a luz direcional.
    // Você pode decidir se ela afeta o interior da casa ou não.
    // Por enquanto, vamos aplicá-la sempre, já que ela simula o sol/lua.
    vec3 result; 

    // Verificar se a câmera está DENTRO da caixa delimitadora da casa
    const float MIN_X = -3.06421f;
    const float MIN_Y = -2.0f;
    const float MIN_Z = -0.489827f;
    const float MAX_X = 13.2461f;
    const float MAX_Y = 3.53016f;
    const float MAX_Z = 14.0987f;

    bool is_camera_inside_house = (viewPos.x > MIN_X && viewPos.x < MAX_X &&
                                   viewPos.y > MIN_Y && viewPos.y < MAX_Y &&
                                   viewPos.z > MIN_Z && viewPos.z < MAX_Z);

    if (is_camera_inside_house) {
        // Câmera está DENTRO da casa: aplicar SOMENTE luzes internas
        for (int i = 0; i < NR_INTERNAL_LIGHTS; i++) {
            result += CalcPointLight(internalLights[i], norm, FragPos, viewDir);
        }
    } else {
        result += CalcDirLight(dirLight, norm, viewDir);
        // Câmera está FORA da casa: aplicar SOMENTE luzes externas
        for (int i = 0; i < NR_EXTERNAL_LIGHTS; i++) {
            result += CalcPointLight(externalLights[i], norm, FragPos, viewDir);
        }
    }

    FragColor = vec4(result, 1.0);
}