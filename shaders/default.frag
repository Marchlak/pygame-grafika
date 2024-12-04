#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
in vec4 shadowCoord;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;
uniform sampler2DShadow shadowMap;
uniform vec2 u_resolution;

uniform float u_time;
uniform float u_apply_gradient;


float lookup(float ox, float oy) {
    vec2 pixelOffset = 1 / u_resolution;
    return textureProj(shadowMap, shadowCoord + vec4(ox * pixelOffset.x * shadowCoord.w,
                                                     oy * pixelOffset.y * shadowCoord.w, 0.0, 0.0));
}

float getSoftShadowX4() {
    float shadow;
    float swidth = 1.5;  // shadow spread
    vec2 offset = mod(floor(gl_FragCoord.xy), 2.0) * swidth;
    shadow += lookup(-1.5 * swidth + offset.x, 1.5 * swidth - offset.y);
    shadow += lookup(-1.5 * swidth + offset.x, -0.5 * swidth - offset.y);
    shadow += lookup( 0.5 * swidth + offset.x, 1.5 * swidth - offset.y);
    shadow += lookup( 0.5 * swidth + offset.x, -0.5 * swidth - offset.y);
    return shadow / 4.0;
}

float getSoftShadowX16() {
    float shadow;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16.0;
}

float getSoftShadowX64() {
    float shadow;
    float swidth = 0.6;
    float endp = swidth * 3.0 + swidth / 2.0;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 64;
}

float getShadow() {
    float shadow = textureProj(shadowMap, shadowCoord);
    return shadow;
}

vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);

    // ambient light
    vec3 ambient = light.Ia;

    // diffuse light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    // specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    // shadow
//    float shadow = getShadow();
    float shadow = getSoftShadowX16();

    return color * (ambient + (diffuse + specular) * shadow);
}

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));

    // Apply gradient if u_apply_gradient is 1.0
    if (u_apply_gradient == 1.0) {
        // Compute the offset based on fragment position and time
        float speed = 1.0; // Adjust the speed as needed
        vec3 direction = vec3(1.0, 0.0, 0.0); // Gradient direction (e.g., along X-axis)
        float offset = dot(fragPos.xyz, direction) + u_time * speed;

        // Calculate the color offset using a sinusoidal function
        vec3 color_offset = vec3(
            0.5 * sin(offset) + 0.5,
            0.5 * sin(offset + 2.0) + 0.5,
            0.5 * sin(offset + 4.0) + 0.5
        );

        // Add the color offset to the texture color
        color += color_offset;

        // Clamp the color to valid range [0,1]
        color = clamp(color, 0.0, 1.0);
    }

    color = getLight(color);

    color = pow(color, vec3(1.0 / gamma));
    fragColor = vec4(color, 1.0);
}
