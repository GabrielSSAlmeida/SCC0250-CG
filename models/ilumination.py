# ilumination.py
import glm
from OpenGL.GL import *
from typing import Dict, Any

class Ilumination:
    def __init__(self, shader_program: int,
                 internal_lights,
                 external_lights,
                 internal_spotlights,
                 external_spotlights,
                 dir_light_data: Dict[str, Any]):

        self.shader_program = shader_program
        self.internal_lights_data = internal_lights[0]
        self.external_lights_data = external_lights[0]
        self.nr_internal_lights_shader = internal_lights[1]
        self.nr_external_lights_shader = external_lights[1]

        self.internal_spotlights_data = internal_spotlights[0]
        self.external_spotlights_data = external_spotlights[0]
        self.nr_internal_spotlights_shader = internal_spotlights[1]
        self.nr_external_spotlights_shader = external_spotlights[1]

        self.dir_light_data = dir_light_data

        self._uniform_locations = {}
        self._cache_light_uniform_locations()
        self._set_static_light_uniforms()

    def _cache_light_uniform_locations(self):
        """
        Cacheia as localizações dos uniforms das luzes no shader program.
        """
        # Luz Direcional
        self._uniform_locations["dirLight.direction"] = glGetUniformLocation(self.shader_program, "dirLight.direction")
        self._uniform_locations["dirLight.ambient"] = glGetUniformLocation(self.shader_program, "dirLight.ambient")
        self._uniform_locations["dirLight.diffuse"] = glGetUniformLocation(self.shader_program, "dirLight.diffuse")
        self._uniform_locations["dirLight.specular"] = glGetUniformLocation(self.shader_program, "dirLight.specular")

        # Luzes Internas
        for i in range(self.nr_internal_lights_shader):
            self._uniform_locations[f"internalLights[{i}].position"] = glGetUniformLocation(self.shader_program, f"internalLights[{i}].position")
            self._uniform_locations[f"internalLights[{i}].ambient"] = glGetUniformLocation(self.shader_program, f"internalLights[{i}].ambient")
            self._uniform_locations[f"internalLights[{i}].diffuse"] = glGetUniformLocation(self.shader_program, f"internalLights[{i}].diffuse")
            self._uniform_locations[f"internalLights[{i}].specular"] = glGetUniformLocation(self.shader_program, f"internalLights[{i}].specular")
            self._uniform_locations[f"internalLights[{i}].constant"] = glGetUniformLocation(self.shader_program, f"internalLights[{i}].constant")
            self._uniform_locations[f"internalLights[{i}].linear"] = glGetUniformLocation(self.shader_program, f"internalLights[{i}].linear")
            self._uniform_locations[f"internalLights[{i}].quadratic"] = glGetUniformLocation(self.shader_program, f"internalLights[{i}].quadratic")

        # Luzes Externas
        for i in range(self.nr_external_lights_shader):
            self._uniform_locations[f"externalLights[{i}].position"] = glGetUniformLocation(self.shader_program, f"externalLights[{i}].position")
            self._uniform_locations[f"externalLights[{i}].ambient"] = glGetUniformLocation(self.shader_program, f"externalLights[{i}].ambient")
            self._uniform_locations[f"externalLights[{i}].diffuse"] = glGetUniformLocation(self.shader_program, f"externalLights[{i}].diffuse")
            self._uniform_locations[f"externalLights[{i}].specular"] = glGetUniformLocation(self.shader_program, f"externalLights[{i}].specular")
            self._uniform_locations[f"externalLights[{i}].constant"] = glGetUniformLocation(self.shader_program, f"externalLights[{i}].constant")
            self._uniform_locations[f"externalLights[{i}].linear"] = glGetUniformLocation(self.shader_program, f"externalLights[{i}].linear")
            self._uniform_locations[f"externalLights[{i}].quadratic"] = glGetUniformLocation(self.shader_program, f"externalLights[{i}].quadratic")

        # Spotlights Internos
        for i in range(self.nr_internal_spotlights_shader):
            self._uniform_locations[f"internalSpotLights[{i}].position"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].position")
            self._uniform_locations[f"internalSpotLights[{i}].direction"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].direction")
            self._uniform_locations[f"internalSpotLights[{i}].ambient"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].ambient")
            self._uniform_locations[f"internalSpotLights[{i}].diffuse"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].diffuse")
            self._uniform_locations[f"internalSpotLights[{i}].specular"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].specular")
            self._uniform_locations[f"internalSpotLights[{i}].constant"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].constant")
            self._uniform_locations[f"internalSpotLights[{i}].linear"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].linear")
            self._uniform_locations[f"internalSpotLights[{i}].quadratic"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].quadratic")
            self._uniform_locations[f"internalSpotLights[{i}].cutOff"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].cutOff")
            self._uniform_locations[f"internalSpotLights[{i}].outerCutOff"] = glGetUniformLocation(self.shader_program, f"internalSpotLights[{i}].outerCutOff")

        # Spotlights Externos
        """  for i in range(self.nr_external_spotlights_shader):
            self._uniform_locations[f"externalSpotLights[{i}].position"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].position")
            self._uniform_locations[f"externalSpotLights[{i}].direction"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].direction")
            self._uniform_locations[f"externalSpotLights[{i}].ambient"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].ambient")
            self._uniform_locations[f"externalSpotLights[{i}].diffuse"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].diffuse")
            self._uniform_locations[f"externalSpotLights[{i}].specular"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].specular")
            self._uniform_locations[f"externalSpotLights[{i}].constant"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].constant")
            self._uniform_locations[f"externalSpotLights[{i}].linear"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].linear")
            self._uniform_locations[f"externalSpotLights[{i}].quadratic"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].quadratic")
            self._uniform_locations[f"externalSpotLights[{i}].cutOff"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].cutOff")
            self._uniform_locations[f"externalSpotLights[{i}].outerCutOff"] = glGetUniformLocation(self.shader_program, f"externalSpotLights[{i}].outerCutOff") """

    def _set_static_light_uniforms(self):
        """
        Envia os uniforms das luzes para o shader.
        Este método é chamado apenas uma vez, pois as luzes são estáticas.
        """
        # Garante que o shader está ativo antes de enviar uniforms
        glUseProgram(self.shader_program)

        # Luz Direcional
        if self.dir_light_data.get("direction") is not None:
            glUniform3fv(self._uniform_locations["dirLight.direction"], 1, glm.value_ptr(self.dir_light_data["direction"]))
        if self.dir_light_data.get('ambient') is not None:
            glUniform3fv(self._uniform_locations["dirLight.ambient"], 1, glm.value_ptr(self.dir_light_data["ambient"]))
        if self.dir_light_data.get('diffuse') is not None:
            glUniform3fv(self._uniform_locations["dirLight.diffuse"], 1, glm.value_ptr(self.dir_light_data["diffuse"]))
        if self.dir_light_data.get('specular') is not None:
            glUniform3fv(self._uniform_locations["dirLight.specular"], 1, glm.value_ptr(self.dir_light_data["specular"]))
        
        # luzes internas
        for idx, light in enumerate(self.internal_lights_data):
            # Adicionando verificações para cada propriedade da luz
            if light.get("position") is not None:
                glUniform3fv(self._uniform_locations[f"internalLights[{idx}].position"], 1, glm.value_ptr(light["position"]))
            if light.get("ambient") is not None:
                glUniform3fv(self._uniform_locations[f"internalLights[{idx}].ambient"], 1, glm.value_ptr(light["ambient"]))
            if light.get("diffuse") is not None:
                glUniform3fv(self._uniform_locations[f"internalLights[{idx}].diffuse"], 1, glm.value_ptr(light["diffuse"]))
            if light.get("specular") is not None:
                glUniform3fv(self._uniform_locations[f"internalLights[{idx}].specular"], 1, glm.value_ptr(light["specular"]))
            if light.get("constant") is not None:
                glUniform1f(self._uniform_locations[f"internalLights[{idx}].constant"], light["constant"])
            if light.get("linear") is not None:
                glUniform1f(self._uniform_locations[f"internalLights[{idx}].linear"], light["linear"])
            if light.get("quadratic") is not None:
                glUniform1f(self._uniform_locations[f"internalLights[{idx}].quadratic"], light["quadratic"])

        # Luzes Externas
        for idx, light in enumerate(self.external_lights_data):
            # Adicionando verificações para cada propriedade da luz
            if light.get("position") is not None:
                glUniform3fv(self._uniform_locations[f"externalLights[{idx}].position"], 1, glm.value_ptr(light["position"]))
            if light.get("ambient") is not None:
                glUniform3fv(self._uniform_locations[f"externalLights[{idx}].ambient"], 1, glm.value_ptr(light["ambient"]))
            if light.get("diffuse") is not None:
                glUniform3fv(self._uniform_locations[f"externalLights[{idx}].diffuse"], 1, glm.value_ptr(light["diffuse"]))
            if light.get("specular") is not None:
                glUniform3fv(self._uniform_locations[f"externalLights[{idx}].specular"], 1, glm.value_ptr(light["specular"]))
            if light.get("constant") is not None:
                glUniform1f(self._uniform_locations[f"externalLights[{idx}].constant"], light["constant"])
            if light.get("linear") is not None:
                glUniform1f(self._uniform_locations[f"externalLights[{idx}].linear"], light["linear"])
            if light.get("quadratic") is not None:
                glUniform1f(self._uniform_locations[f"externalLights[{idx}].quadratic"], light["quadratic"])

        # Spotlights Internos
        for idx, spotlight in enumerate(self.internal_spotlights_data):
            if spotlight.get("position") is not None:
                glUniform3fv(self._uniform_locations[f"internalSpotLights[{idx}].position"], 1, glm.value_ptr(spotlight["position"]))
            if spotlight.get("direction") is not None:
                glUniform3fv(self._uniform_locations[f"internalSpotLights[{idx}].direction"], 1, glm.value_ptr(spotlight["direction"]))
            if spotlight.get("ambient") is not None:
                glUniform3fv(self._uniform_locations[f"internalSpotLights[{idx}].ambient"], 1, glm.value_ptr(spotlight["ambient"]))
            if spotlight.get("diffuse") is not None:
                glUniform3fv(self._uniform_locations[f"internalSpotLights[{idx}].diffuse"], 1, glm.value_ptr(spotlight["diffuse"]))
            if spotlight.get("specular") is not None:
                glUniform3fv(self._uniform_locations[f"internalSpotLights[{idx}].specular"], 1, glm.value_ptr(spotlight["specular"]))
            if spotlight.get("constant") is not None:
                glUniform1f(self._uniform_locations[f"internalSpotLights[{idx}].constant"], spotlight["constant"])
            if spotlight.get("linear") is not None:
                glUniform1f(self._uniform_locations[f"internalSpotLights[{idx}].linear"], spotlight["linear"])
            if spotlight.get("quadratic") is not None:
                glUniform1f(self._uniform_locations[f"internalSpotLights[{idx}].quadratic"], spotlight["quadratic"])
            if spotlight.get("cutOff") is not None:
                glUniform1f(self._uniform_locations[f"internalSpotLights[{idx}].cutOff"], spotlight["cutOff"])
            if spotlight.get("outerCutOff") is not None:
                glUniform1f(self._uniform_locations[f"internalSpotLights[{idx}].outerCutOff"], spotlight["outerCutOff"])
        # Spotlights Externos
        """ for idx, spotlight in enumerate(self.external_spotlights_data):
            if spotlight.get("position") is not None:
                glUniform3fv(self._uniform_locations[f"externalSpotLights[{idx}].position"], 1, glm.value_ptr(spotlight["position"]))
            if spotlight.get("direction") is not None:
                glUniform3fv(self._uniform_locations[f"externalSpotLights[{idx}].direction"], 1, glm.value_ptr(spotlight["direction"]))
            if spotlight.get("ambient") is not None:
                glUniform3fv(self._uniform_locations[f"externalSpotLights[{idx}].ambient"], 1, glm.value_ptr(spotlight["ambient"]))
            if spotlight.get("diffuse") is not None:
                glUniform3fv(self._uniform_locations[f"externalSpotLights[{idx}].diffuse"], 1, glm.value_ptr(spotlight["diffuse"]))
            if spotlight.get("specular") is not None:
                glUniform3fv(self._uniform_locations[f"externalSpotLights[{idx}].specular"], 1, glm.value_ptr(spotlight["specular"]))
            if spotlight.get("constant") is not None:
                glUniform1f(self._uniform_locations[f"externalSpotLights[{idx}].constant"], spotlight["constant"])
            if spotlight.get("linear") is not None:
                glUniform1f(self._uniform_locations[f"externalSpotLights[{idx}].linear"], spotlight["linear"])
            if spotlight.get("quadratic") is not None:
                glUniform1f(self._uniform_locations[f"externalSpotLights[{idx}].quadratic"], spotlight["quadratic"])
            if spotlight.get("cutOff") is not None:
                glUniform1f(self._uniform_locations[f"externalSpotLights[{idx}].cutOff"], spotlight["cutOff"])
            if spotlight.get("outerCutOff") is not None:
                glUniform1f(self._uniform_locations[f"externalSpotLights[{idx}].outerCutOff"], spotlight["outerCutOff"]) """

        # Opcional: Desativar o shader após o envio, se não for desenhar imediatamente
        # glUseProgram(0)
    
    def update_external_light_position(self, light_index: int, new_position: glm.vec3):
        """
        Atualiza a posição de uma luz externa específica no shader.
        Chame este método a cada frame se a luz for dinâmica.
        """
        glUseProgram(self.shader_program)
        uniform_name = f"externalLights[{light_index}].position"
        if uniform_name in self._uniform_locations:
            glUniform3fv(self._uniform_locations[uniform_name], 1, glm.value_ptr(new_position))