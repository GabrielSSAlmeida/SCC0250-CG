import glm
import numpy as np
import math
from OpenGL.GL import *
from models.model import ModelBase

class Model_2D(ModelBase):
    @property
    def primitive_type(self):
        return GL_TRIANGLE_STRIP

    def get_transform_matrix(self, angle=0.0, r_x=0.0, r_y=0.0,
                             t_x=0.0, t_y=0.0,
                             s_x=1.0, s_y=1.0):
        angle = math.radians(angle)
        matrix_transform = glm.mat4(1.0)
        matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, 0.0))
        if angle != 0:
            matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, 1.0))
        matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, 1.0))
        return np.array(matrix_transform)
