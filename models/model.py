import glm
import numpy as np
import math
from OpenGL.GL import *
from abc import ABC, abstractmethod

class ModelBase(ABC):
    def __init__(self, vertices, num_vertices, modelConfig, color=(0.0, 0.0, 0.0, 1)):
        self.vertices = vertices
        self.num_vertices = num_vertices
        self.modelConfig = modelConfig
        self.color = color

    @abstractmethod
    def get_transform_matrix(self, **kwargs):
        pass

    @property
    @abstractmethod
    def primitive_type(self):
        pass

    def draw(self, program):
        loc_color = glGetUniformLocation(program, "color")
        glUniform4f(loc_color, *self.color)

        mat_model = self.get_transform_matrix(**self.modelConfig)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glDrawArrays(self.primitive_type, self.vertices, self.num_vertices)