from window import Window
from models.model_3D import Model_3D
from models.model_2D import Model_2D
from models.renderer import Renderer
from utils.file_loader import FileManager
from OpenGL.GL import *

def main():
    window = Window()
    renderer = Renderer(window)

    # Carregar modelo
    verticeInicial_harry, quantosVertices_harry = FileManager.load_obj_and_texture('objects/Harry.obj', [])
    verticeInicial_arco, quantosVertices_arco = FileManager.load_obj_and_texture('objects/Arco.obj', [])
    verticeInicial_pomo, quantosVertices_pomo = FileManager.load_obj_and_texture('objects/Pomo.obj', [])
    verticeInicial_nimbus, quantosVertices_nimbus = FileManager.load_obj_and_texture('objects/Nimbus2000.obj', [])
    verticeInicial_chapeu, quantosVertices_chapeu = FileManager.load_obj_and_texture('objects/Chapeu.obj', [])
    verticeInicial_grama, quantosVertices_grama = FileManager.load_obj_2D_and_texture('objects/Quadrado.obj', [])
    verticeInicial_ceu, quantosVertices_ceu = FileManager.load_obj_2D_and_texture('objects/Quadrado.obj', [])

    # Criar objeto Model
    ceu = Model_2D(verticeInicial_ceu, quantosVertices_ceu, {"t_y": -0.27,"t_x": -1.0,"s_x": 1.0, "s_y": 0.18}, (0.42, 0.65, 0.95, 1))
    grama = Model_2D(verticeInicial_grama, quantosVertices_grama, {"t_y": -3.0,"t_x": -3.0,"s_x": 0.05, "s_y": 0.028}, (0.19, 0.85, 0.5, 1))
    harry = Model_3D(verticeInicial_harry, quantosVertices_harry, {"s_x": 0.15, "s_y": 0.15, "s_z": 0.15}, (1, 0.9, 0.8, 1))
    arco = Model_3D(verticeInicial_arco, quantosVertices_arco, {"t_x": 0.6, "s_x": 0.1, "s_y": 0.1, "s_z": 0.1}, (0.5, 0.5, 0.5, 1))
    pomo = Model_3D(verticeInicial_pomo, quantosVertices_pomo, {"t_x": -0.6, "t_y": 0.6, "s_x": 0.04, "s_y": 0.04, "s_z": 0.04}, (1, 1, 0, 1))
    nimbus = Model_3D(verticeInicial_nimbus, quantosVertices_nimbus, {"t_x": 0.23, "s_x": 0.1, "s_y": 0.1, "s_z": 0.1}, (0.7, 0.5, 0.3, 1))
    chapeu = Model_3D(verticeInicial_chapeu, quantosVertices_chapeu, {"t_y": 0.38, "s_x": 0.11, "s_y": 0.11, "s_z": 0.11}, (0.4, 0.2, 0, 1))
    

    renderer.add_model(ceu)
    renderer.add_model(grama)
    renderer.add_model(harry)
    renderer.add_model(arco)
    renderer.add_model(pomo)
    renderer.add_model(nimbus)
    renderer.add_model(chapeu)
    


    # Exibir janela
    window.upload_data()
    window.show()
    window.enable()
    while not window.should_close():
        renderer.render()

    window.terminate()

if __name__ == "__main__":
    main()
