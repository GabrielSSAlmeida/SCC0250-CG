"""
    Nomes: Camila Donda Ronchi                              NUSP: 13672220
           Gabriel Sousa Santos de Almeida                        13837432
"""

import glfw
from OpenGL.GL import *
import numpy as np
from models2 import *
import utils2 as u

from shaders.shader_s import Shader


def upload_data(buffer_VBO, program):
    vertices = np.zeros(len(u.vertices_list), [("position", np.float32, 3)])
    vertices['position'] = u.vertices_list

    # Upload data
    glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)
    loc_vertices = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc_vertices)
    glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

def init_window():
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    altura = 700
    largura = 700

    window = glfw.create_window(largura, altura, "Programa", None, None)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate() 
        
    glfw.make_context_current(window)

    ourShader = Shader("vertex_shader.vs", "fragment_shader.fs")
    ourShader.use()

    program = ourShader.getProgram()


    buffer_VBO = glGenBuffers(1)

    return window, program, buffer_VBO

def main():
    
    window, program, buffer_VBO = init_window()

    # load objects
    verticeInicial_harry, quantosVertices_harry = u.load_obj_and_texture('objetos/Harry.obj', []) 


    upload_data(buffer_VBO, program)



    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)
    while not glfw.window_should_close(window):

        glfw.poll_events() 
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        

        make_model(verticeInicial_harry, quantosVertices_harry, program, s_x=0.2, s_y=0.2, s_z=0.2)
        
        glfw.swap_buffers(window)

    glfw.terminate()



if __name__ == "__main__":
    main()