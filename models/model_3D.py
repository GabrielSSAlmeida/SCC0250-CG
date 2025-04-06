import glm
import numpy as np
import math
from OpenGL.GL import *
from models.model import ModelBase


class Model_3D(ModelBase):
    @property
    def primitive_type(self):
        return GL_TRIANGLES

    # implements get_transform_matrix
    def get_transform_matrix(self, angle_x=0.0, angle_y=0.0, angle_z=0.0,
                         t_x=0.0, t_y=0.0, t_z=0.0,
                         s_x=1.0, s_y=1.0, s_z=1.0, **kwargs):

        angle_x = math.radians(angle_x)
        angle_y = math.radians(angle_y)
        angle_z = math.radians(angle_z)

        matrix_transform = glm.mat4(1.0)
        matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))

        if angle_x != 0:
            matrix_transform = glm.rotate(matrix_transform, angle_x, glm.vec3(1, 0, 0))
        if angle_y != 0:
            matrix_transform = glm.rotate(matrix_transform, angle_y, glm.vec3(0, 1, 0))
        if angle_z != 0:
            matrix_transform = glm.rotate(matrix_transform, angle_z, glm.vec3(0, 0, 1))

        matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
        return np.array(matrix_transform)