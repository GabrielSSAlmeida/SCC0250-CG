import glfw
from OpenGL.GL import *
import numpy as np
from shaders.shader_s import Shader
from utils.file_loader import FileManager

class Window:
    def __init__(self, width=700, height=700, title="Programa"):
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        self.glfw_window = glfw.create_window(width, height, title, None, None)

        if not self.glfw_window:
            print("Failed to create GLFW window")
            glfw.terminate()

        glfw.make_context_current(self.glfw_window)
        self.shader = Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
        self.shader.use()
        self.program = self.shader.getProgram()
        self.buffer_VBO = glGenBuffers(1)

    def show(self):
        glfw.show_window(self.glfw_window)

    def close(self):
        glfw.set_window_should_close(self.glfw_window, True)

    def should_close(self):
        return glfw.window_should_close(self.glfw_window)

    def terminate(self):
        glfw.terminate()

    def enable(self):
        glEnable(GL_DEPTH_TEST)

    def poll_events(self):
        glfw.poll_events()

    def swap_buffers(self):
        glfw.swap_buffers(self.glfw_window)

    def upload_data(self):
        vertices = np.zeros(len(FileManager.vertices_list), [("position", np.float32, 3)])
        vertices['position'] = FileManager.vertices_list

        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)
