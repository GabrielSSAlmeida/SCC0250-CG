# 05/04/2025 18:20

from window import Window
from models.model_3D import Model_3D
from models.model_2D import Model_2D
from models.renderer import Renderer
from utils.file_loader import FileManager
from OpenGL.GL import *
import glfw

def update_model(model, dx=0, dy=0, angle=None):
        config = model.modelConfig
        
        config.setdefault('t_x', 0.0)
        config.setdefault('t_y', 0.0)
        config.setdefault('angle', 0.0)
        config.setdefault('r_x', 0.0)
        config.setdefault('r_y', 0.0)
        config.setdefault('r_z', 1.0)

        config['t_x'] += dx
        config['t_y'] += dy

        if angle is not None:
            config['angle'] = angle
            config['r_x'] = 0.0
            config['r_y'] = 0.0
            config['r_z'] = 1.0

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

    # Criar objeto Model
    grama = Model_2D(verticeInicial_grama, quantosVertices_grama, {"t_y": -3.4,"t_x": -3.0, "angle": 10, "r_x":1.0,"s_x": 0.05, "s_y": 0.028}, (0.19, 0.85, 0.5, 1))
    harry = Model_3D(verticeInicial_harry, quantosVertices_harry, {"t_x": -0.5, "t_y": -0.3, "angle": 20, "r_x":1.0,"s_x": 0.15, "s_y": 0.15, "s_z": 0.15}, (1, 0.9, 0.8, 1))
    arco = Model_3D(verticeInicial_arco, quantosVertices_arco, {"t_x": 0.6, "angle": 0, "r_x":1.0, "r_y":1.0, "s_x": 0.1, "s_y": 0.1, "s_z": 0.1}, (0.5, 0.5, 0.5, 1))
    pomo = Model_3D(verticeInicial_pomo, quantosVertices_pomo, {"t_x": -0.6, "t_y": 0.6, "t_z": 0.001, "angle": 20, "r_x":1.0, "s_x": 0.04, "s_y": 0.04, "s_z": 0.04}, (1, 1, 0, 1))
    nimbus = Model_3D(verticeInicial_nimbus, quantosVertices_nimbus, {"t_x": -0.27, "t_y": -0.3, "angle": -10, "r_x":1.0, "s_x": 0.1, "s_y": 0.1, "s_z": 0.1}, (0.7, 0.5, 0.3, 1))
    chapeu = Model_3D(verticeInicial_chapeu, quantosVertices_chapeu, {"t_x": -0.5, "t_y": 0.025, "angle": -10, "r_x":1.0, "s_x": 0.11, "s_y": 0.11, "s_z": 0.11}, (0.4, 0.2, 0, 1))

    key_map = {
        #   HARRY
        
        glfw.KEY_Y: (lambda m: m.rotate(5, 0, 1, 0), harry),
        #   POMO
        glfw.KEY_UP: (lambda m: m.translate(0, 0.05, 0), pomo),
        glfw.KEY_DOWN: (lambda m: m.translate(0, -0.05, 0), pomo),
        glfw.KEY_LEFT: (lambda m: m.translate(-0.05, 0, 0), pomo),
        glfw.KEY_RIGHT: (lambda m: m.translate(0.05, 0, 0), pomo),
        glfw.KEY_I: (lambda m: m.rotate(5, 0, 1, 0), pomo),
        glfw.KEY_O: (lambda m: m.rotate(5, 1, 0, 0), pomo),
        glfw.KEY_L: (lambda m: m.scale(1.1, 1.1, 1.1), pomo),
        glfw.KEY_K: (lambda m: m.scale(0.9, 0.9, 0.9), pomo),
        # VASSOURA
        glfw.KEY_W: (lambda m: update_model(m, dx=0, dy=0.05, angle=0), nimbus),
        glfw.KEY_S: (lambda m: update_model(m, dx=0, dy=-0.05, angle=180), nimbus),
        glfw.KEY_A: (lambda m: update_model(m, dx=-0.05, dy=0, angle=90), nimbus),
        glfw.KEY_D: (lambda m: update_model(m, dx=0.05, dy=0, angle=270), nimbus),

    }
    
    def key_event(window, key, scancode, action, mods):
        if action in [glfw.PRESS, glfw.REPEAT]:
            if key in key_map:
                func, model = key_map[key]
                func(model)

    glfw.set_key_callback(window.glfw_window, key_event)

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
