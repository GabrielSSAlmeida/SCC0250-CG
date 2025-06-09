from OpenGL.GL import *
from window import Window
from models.model import ModelBase
from typing import List
import glm


class Renderer:
    def __init__(self, window, view, mat_projection):
        self.window: Window = window
        self.models: List[ModelBase] = []
        self.view = view
        self.mat_projection: List = mat_projection
        self.polygonMode = GL_FILL

        self._uniform_locations = {}
        self._cache_shader_uniform_locations()
    
    def add_model(self, model):
        if not isinstance(model, list):
            model = [model]
        for m in model:
            self.models.append(m)

    def setPolygonMode(self):
        if self.polygonMode == GL_FILL:
            self.polygonMode = GL_LINE
        else:
            self.polygonMode = GL_FILL

    def _cache_shader_uniform_locations(self):
        program = self.window.program
        self._uniform_locations["view"] = glGetUniformLocation(program, "view")
        self._uniform_locations["projection"] = glGetUniformLocation(program, "projection")
        self._uniform_locations["viewPos"] = glGetUniformLocation(program, "viewPos")

        
        self._uniform_locations["global_ka"] = glGetUniformLocation(program, "global_ka")
        self._uniform_locations["global_kd"] = glGetUniformLocation(program, "global_kd")
        self._uniform_locations["global_ks"] = glGetUniformLocation(program, "global_ks")

    def render(self, ka_val, kd_val, ks_val):
        self.window.poll_events()
        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.polygonMode)

        self.view.update_view_matrix()
        glUniformMatrix4fv(self._uniform_locations["view"], 1, GL_TRUE, self.view.mat_view)
        glUniformMatrix4fv(self._uniform_locations["projection"], 1, GL_TRUE, self.mat_projection)
        glUniform3f(self._uniform_locations["viewPos"], *self.view.cameraPos)


        glUniform1f(self._uniform_locations["global_ka"], ka_val)
        glUniform1f(self._uniform_locations["global_kd"], kd_val)
        glUniform1f(self._uniform_locations["global_ks"], ks_val)

        for model in self.models:
            model.draw(self.window.program, self.view.cameraPos)

        self.window.swap_buffers()
