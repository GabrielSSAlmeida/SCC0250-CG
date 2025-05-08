# 06/04/2025 18:00

""" 
    SCC0250 - Computação Gráfica

    Projeto 2

    Camila Donda Ronchi - 13672220
    Gabriel Sousa Santos de Almeida - 13837432

"""
from window import Window
from view import View
from projection import Projection
from models.model_3D import Model_3D
from models.model_2D import Model_2D
from models.renderer import Renderer
from utils.file_loader import FileManager
from keymanager import KeyManager
from mousemanager import MouseManager
from utils.custom_keys_callbacks import *
from OpenGL.GL import *
from config import *
import glfw
import glm

def main():
    fov = 45.0
    deltaTime = 0.001
    window = Window()
    view = View(glm.vec3(0.0, 0.0, 5.0), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0), deltaTime)
    projection = Projection(window.altura, window.largura, fov)
    renderer = Renderer(window, view, projection.mat_projection)
    glEnable(GL_TEXTURE_2D)
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    #glEnable( GL_BLEND )
    #glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
    glEnable(GL_LINE_SMOOTH)

    # load models
    verticeInicial_base_casa1, quantosVertices_base_casa1 = FileManager.load_obj_and_texture('objects/base_casa1.obj', ['textures/Pared_piedra_musgo_2K_Albedo.png'])
    verticeInicial_teto_casa, quantosVertices_teto_casa = FileManager.load_obj_and_texture('objects/teto_casa.obj', ['textures/Metal_oxidado_Azul_Albedo.png'])

    # create model objects
    base_casa1 = Model_3D(verticeInicial_base_casa1, quantosVertices_base_casa1, HARRY, 0)
    teto_casa = Model_3D(verticeInicial_teto_casa, quantosVertices_teto_casa, HARRY, )

    # ====== KEY MANAGER ======
    keymanager = KeyManager(window, renderer, view)
    mousemanager = MouseManager(window, view, projection)



    # prepare models to render
    renderer.add_model([base_casa1, teto_casa])
    
    # show windows
    window.upload_data()
    window.show()
    window.enable()
    while not window.should_close():
        renderer.render()

    window.terminate()

if __name__ == "__main__":
    main()
