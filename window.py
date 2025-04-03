import glfw
from OpenGL.GL import *
from shaders.shader_s import Shader

class Window:
    def __init__(self, width=700, height=700, title="Programa"):
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            print("Failed to create GLFW window")
            glfw.terminate()

        glfw.make_context_current(self.window)
        self.shader = Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
        self.shader.use()
        self.program = self.shader.getProgram()
        self.buffer_VBO = glGenBuffers(1)

    def show(self):
        glfw.show_window(self.window)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def update(self):
        glfw.poll_events()
        glfw.swap_buffers(self.window)

    def terminate(self):
        glfw.terminate()
