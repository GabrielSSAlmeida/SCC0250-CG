from OpenGL.GL import *
import glm
import math
import numpy as np

def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
       
    # aplicando translacao (terceira operação a ser executada)
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao (segunda operação a ser executada)
    if angle!=0:
        matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    
    # aplicando escala (primeira operação a ser executada)
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    
    matrix_transform = np.array(matrix_transform)
    
    return matrix_transform

def make_model(vertices_objetos, qtd_vertices, program, angle = 0.0, 
                    r_x = 0.0, r_y = 0.0, r_z = 1.0, 
                    t_x = 0.0, t_y = 0.0, t_z = 0.0, 
                    s_x = 1.0, s_y = 1.0, s_z = 1.0):
    
    global vertices

    color = (0.0,0.0,0.0, 1)

    loc_color = glGetUniformLocation(program, "color")
    glUniform4f(loc_color, *color)
    
    # aplica a matriz model
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    # desenha o objeto
    glDrawArrays(GL_TRIANGLE_STRIP, vertices_objetos, qtd_vertices) ## renderizando