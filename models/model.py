import glm
import numpy as np
import math
from OpenGL.GL import *

class Model:
    def __init__(self, vertices, num_vertices):
        self.vertices = vertices
        self.num_vertices = num_vertices

    def get_transform_matrix(self, angle=0, r_x=0, r_y=0, r_z=1, t_x=0, t_y=0, t_z=0, s_x=0.2, s_y=0.2, s_z=0.2):
        angle = math.radians(angle)
        matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade

        # aplicando translacao (terceira operação a ser executada)
        matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))  

        # aplicando rotacao (segunda operação a ser executada)
        if angle!=0:
            matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
            
        # aplicando escala (primeira operação a ser executada)
        matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
        
        return np.array(matrix_transform)

    def draw(self, program, color=(0.0, 0.0, 0.0, 1)):
        loc_color = glGetUniformLocation(program, "color")
        glUniform4f(loc_color, *color)
        
        mat_model = self.get_transform_matrix()
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glDrawArrays(GL_TRIANGLE_STRIP, self.vertices, self.num_vertices)
