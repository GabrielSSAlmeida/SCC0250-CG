from OpenGL.GL import *
import numpy as np
import glm


class View():
    def __init__(self, cameraPos, cameraFront, cameraUp, deltaTime):
        self.cameraPos = cameraPos
        self.cameraFront = cameraFront
        self.cameraUp = cameraUp
        self.deltaTime = deltaTime
        self.mat_view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)

        self.mat_view = np.array(self.mat_view)

    def set_cameraPos(self, pos):
        self.cameraPos = pos
        self.update_view_matrix()

    def update_view_matrix(self):
        self.mat_view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
        self.mat_view = np.array(self.mat_view)

