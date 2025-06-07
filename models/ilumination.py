# ilumination.py
import glm
from OpenGL.GL import *
from typing import Dict, Any

class Ilumination:
    def __init__(self, shader_program: int,
                 internal_lights_data: Dict[str, Any],
                 external_lights_data: Dict[str, Any],
                 dir_light_data: Dict[str, Any],
                 nr_internal_lights_shader: int,
                 nr_external_lights_shader: int):

        self.shader_program = shader_program
        self.internal_lights_data = internal_lights_data
        self.external_lights_data = external_lights_data
        self.dir_light_data = dir_light_data
        self.nr_internal_lights_shader = nr_internal_lights_shader
        self.nr_external_lights_shader = nr_external_lights_shader

        self._uniform_locations = {}
        self._cache_light_uniform_locations()
        self._set_static_light_uniforms()

    def _cache_light_uniform_locations(self):
        """
        Cacheia as localizações dos uniforms das luzes no shader program.
        """
        # Luz Direcional
        self._uniform_locations["dirLight.direction"] = glGetUniformLocation(self.shader_program, "dirLight.direction")
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

        # Opcional: Desativar o shader após o envio, se não for desenhar imediatamente
        # glUseProgram(0)