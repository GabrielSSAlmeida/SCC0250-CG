from OpenGL.GL import *

class Renderer:
    def __init__(self, window):
        self.window = window
        self.models = []

    def add_model(self, model):
        self.models.append(model)

    def render(self):
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        for model in self.models:
            model.draw(self.window.program)

        self.window.update()
