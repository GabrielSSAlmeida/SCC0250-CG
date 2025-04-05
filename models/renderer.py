from OpenGL.GL import *
from window import Window
from models.model import ModelBase
from typing import List


class Renderer:
    def __init__(self, window):
        self.window: Window = window
        self.models: List[ModelBase] = []

    def add_model(self, model):
        self.models.append(model)

    def render(self):
        self.window.poll_events()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.42, 0.65, 0.95, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        for model in self.models:
            model.draw(self.window.program)

        self.window.swap_buffers()
