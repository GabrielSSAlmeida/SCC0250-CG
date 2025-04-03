from OpenGL.GL import *
import glfw
class Renderer:
    def __init__(self, window):
        self.window = window
        self.models = []

    def add_model(self, model):
        self.models.append(model)

    def render(self):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        for model in self.models:
            model.draw(self.window.program)

        glfw.swap_buffers(self.window.glfw_window)
        #self.window.update()
