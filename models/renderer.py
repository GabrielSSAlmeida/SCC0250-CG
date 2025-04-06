from OpenGL.GL import *
from window import Window
from models.model import ModelBase
from typing import List


class Renderer:
    def __init__(self, window):
        self.window: Window = window
        self.models: List[ModelBase] = []
        self.polygonMode = GL_FILL

    # add models to the list that renders
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

    def render(self):
        self.window.poll_events()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.42, 0.65, 0.95, 1) # blue sky
        glPolygonMode(GL_FRONT_AND_BACK, self.polygonMode)

        for model in self.models:
            model.draw(self.window.program)

        self.window.swap_buffers()
