from OpenGL.GL import *
from window import Window
from models.model import ModelBase
from typing import List


class Renderer:
    def __init__(self, window, view, mat_projection):
        self.window: Window = window
        self.models: List[ModelBase] = []
        self.view = view
        self.mat_projection: List = mat_projection
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
        glClearColor(1.0, 1.0, 1.0, 1) # white background
        glPolygonMode(GL_FRONT_AND_BACK, self.polygonMode)

        for model in self.models:
            model.draw(self.window.program)
        
        self.view.update_view_matrix()
        loc_view = glGetUniformLocation(self.window.program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, self.view.mat_view)

        loc_projection = glGetUniformLocation(self.window.program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, self.mat_projection)    

        self.window.swap_buffers()
