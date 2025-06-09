import glfw
from OpenGL.GL import *
import numpy as np
from shaders.shader_s import Shader
from utils.file_loader import FileManager

class Window:
    def __init__(self, width=700, height=700, title="Programa"):
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        self.largura = width
        self.altura = height
        
        self.glfw_window = glfw.create_window(width, height, title, None, None)

        if not self.glfw_window:
            print("Failed to create GLFW window")
            glfw.terminate()

        glfw.make_context_current(self.glfw_window)
        self.shader = Shader("shaders/multiple_lights.vs", "shaders/multiple_lights.fs")
        self.shader.use()
        self.program = self.shader.getProgram()
        self.buffer_VBO = glGenBuffers(3)
        self.VAO = glGenVertexArrays(1)

        glEnable(GL_TEXTURE_2D)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        #glEnable( GL_BLEND )
        #glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
        glEnable(GL_LINE_SMOOTH)

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
        glBindVertexArray(self.VAO)

        vertices = np.zeros(len(FileManager.vertices_list), [("position", np.float32, 3)])
        vertices['position'] = FileManager.vertices_list

        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_VBO[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)


        normals = np.zeros(len(FileManager.normals_list), [("position", np.float32, 3)])
        normals['position'] = FileManager.normals_list

        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_VBO[1])
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        stride = normals.strides[0]
        offset = ctypes.c_void_p(0)
        loc_normais = glGetAttribLocation(self.program, "normal")
        glEnableVertexAttribArray(loc_normais)
        glVertexAttribPointer(loc_normais, 3, GL_FLOAT, False, stride, offset)

        textures = np.zeros(len(FileManager.textures_coord_list), [("position", np.float32, 2)])
        textures['position'] = FileManager.textures_coord_list

        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_VBO[2])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride = textures.strides[0]
        offset = ctypes.c_void_p(0)
        loc_textures = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_textures)
        glVertexAttribPointer(loc_textures, 2, GL_FLOAT, False, stride, offset)

