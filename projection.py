from OpenGL.GL import *
import numpy as np
import glm


class Projection():
    def __init__(self, altura, largura, fov):
        self.altura = altura
        self.largura = largura
        self.fov = fov
        self.mat_projection = glm.perspective(glm.radians(fov), largura/altura, 0.1, 100.0)

        self.mat_projection = np.array(self.mat_projection)
    
    def set_fov(self, fov):
        self.fov = fov