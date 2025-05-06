# 06/04/2025 18:00

""" 
    SCC0250 - Computação Gráfica

    Projeto 1

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

    # load models
    verticeInicial_harry, quantosVertices_harry = FileManager.load_obj_and_texture('objects/Harry.obj', [])
    verticeInicial_arco, quantosVertices_arco = FileManager.load_obj_and_texture('objects/Arco.obj', [])
    verticeInicial_pomo, quantosVertices_pomo = FileManager.load_obj_and_texture('objects/Pomo.obj', [])
    verticeInicial_nimbus, quantosVertices_nimbus = FileManager.load_obj_and_texture('objects/Nimbus2000.obj', [])
    verticeInicial_chapeu, quantosVertices_chapeu = FileManager.load_obj_and_texture('objects/Chapeu.obj', [])
    verticeInicial_grama, quantosVertices_grama = FileManager.load_obj_2D_and_texture('objects/Quadrado.obj', [])

    # create model objects
    grama = Model_2D(verticeInicial_grama, quantosVertices_grama, GRAMA, (0.19, 0.85, 0.5, 1))
    harry = Model_3D(verticeInicial_harry, quantosVertices_harry, HARRY, (1, 0.9, 0.8, 1))
    arco = Model_3D(verticeInicial_arco, quantosVertices_arco, ARCO, (0.5, 0.5, 0.5, 1))
    pomo = Model_3D(verticeInicial_pomo, quantosVertices_pomo, POMO, (1, 1, 0, 1))
    nimbus = Model_3D(verticeInicial_nimbus, quantosVertices_nimbus, NIMBUS, (0.7, 0.5, 0.3, 1))
    chapeu = Model_3D(verticeInicial_chapeu, quantosVertices_chapeu, CHAPEU, (0.4, 0.2, 0, 1))

    # ====== KEY MANAGER ======
    keymanager = KeyManager(window, renderer, view)
    mousemanager = MouseManager(window, view, projection)



    # prepare models to render
    renderer.add_model([grama, harry, arco, pomo, nimbus, chapeu])
    
    # show windows
    window.upload_data()
    window.show()
    window.enable()
    while not window.should_close():
        renderer.render()

    window.terminate()

if __name__ == "__main__":
    main()
