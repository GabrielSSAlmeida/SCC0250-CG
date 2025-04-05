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

    def translate(self, dx=0, dy=0, dz=0):
        self.modelConfig["t_x"] = self.modelConfig.get("t_x", 0) + dx
        self.modelConfig["t_y"] = self.modelConfig.get("t_y", 0) + dy
        self.modelConfig["t_z"] = self.modelConfig.get("t_z", 0) + dz

    def scale(self, sx=1, sy=1, sz=1):
        self.modelConfig["s_x"] = self.modelConfig.get("s_x", 1) * sx
        self.modelConfig["s_y"] = self.modelConfig.get("s_y", 1) * sy
        self.modelConfig["s_z"] = self.modelConfig.get("s_z", 1) * sz

    def rotate(self, angle=0, rx=0, ry=0, rz=0):
        self.modelConfig["angle"] = self.modelConfig.get("angle", 0) + angle
        self.modelConfig["r_x"] = rx
        self.modelConfig["r_y"] = ry
        self.modelConfig["r_z"] = rz

