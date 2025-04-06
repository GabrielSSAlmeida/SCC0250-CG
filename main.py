# 05/04/2025 18:20

from window import Window
from models.model_3D import Model_3D
from models.model_2D import Model_2D
from models.renderer import Renderer
from utils.file_loader import FileManager
from utils.custom_keys_callbacks import *
from OpenGL.GL import *
from constants import *
import glfw


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
    grama = Model_2D(verticeInicial_grama, quantosVertices_grama, GRAMA, (0.19, 0.85, 0.5, 1))
    harry = Model_3D(verticeInicial_harry, quantosVertices_harry, HARRY, (1, 0.9, 0.8, 1))
    arco = Model_3D(verticeInicial_arco, quantosVertices_arco, ARCO, (0.5, 0.5, 0.5, 1))
    pomo = Model_3D(verticeInicial_pomo, quantosVertices_pomo, POMO, (1, 1, 0, 1))
    nimbus = Model_3D(verticeInicial_nimbus, quantosVertices_nimbus, NIMBUS, (0.7, 0.5, 0.3, 1))
    chapeu = Model_3D(verticeInicial_chapeu, quantosVertices_chapeu, CHAPEU, (0.4, 0.2, 0, 1))

    key_map = {
        glfw.KEY_R: (lambda m: m.reset(), [harry, pomo, nimbus, chapeu]),
        #   HARRY
        glfw.KEY_Y: (lambda m: m.rotate(5, 0, 1, 0), [harry, chapeu]),
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
        glfw.KEY_W: (lambda m: nimbus_t_and_r(m, dx=0, dy=0.05, angle_z=0), nimbus),
        glfw.KEY_S: (lambda m: nimbus_t_and_r(m, dx=0, dy=-0.05, angle_z=180), nimbus),
        glfw.KEY_A: (lambda m: nimbus_t_and_r(m, dx=-0.05, dy=0, angle_z=90), nimbus),
        glfw.KEY_D: (lambda m: nimbus_t_and_r(m, dx=0.05, dy=0, angle_z=270), nimbus),

    }
    
    def key_event(w, key, scancode, action, mods):
        if key in key_map:
            if action in [glfw.PRESS, glfw.REPEAT]:
                func, model = key_map[key]
                if not isinstance(model, list):
                    model = [model]
                for m in model:
                    func(m)

        if key == glfw.KEY_P and (action == glfw.PRESS or action == glfw.REPEAT):
            renderer.setPolygonMode()
        if key == glfw.KEY_ESCAPE and (action == glfw.PRESS or action == glfw.REPEAT):
            window.close()


    glfw.set_key_callback(window.glfw_window, key_event)

    renderer.add_model([grama, harry, arco, pomo, nimbus, chapeu])
    
    # Exibir janela
    window.upload_data()
    window.show()
    window.enable()
    while not window.should_close():
        renderer.render()

    window.terminate()

if __name__ == "__main__":
    main()
