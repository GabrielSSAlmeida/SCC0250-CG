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
    view = View(glm.vec3(0.0, 10.0, 5.0), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0), deltaTime)
    projection = Projection(window.altura, window.largura, fov)
    renderer = Renderer(window, view, projection.mat_projection)
    glEnable(GL_TEXTURE_2D)
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    #glEnable( GL_BLEND )
    #glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
    glEnable(GL_LINE_SMOOTH)

    vi_base, n_base, tex_base = FileManager.load_obj_and_texture('objects/base_casa.obj', ['textures/Pared_piedra_musgo_2K_Albedo.png'])
    vi_teto, n_teto, tex_teto = FileManager.load_obj_and_texture('objects/teto.obj', ['textures/Metal_oxidado_Azul_Albedo.png'])
    vi_portas, n_portas, tex_portas = FileManager.load_obj_and_texture('objects/portas.obj', ['textures/Madera_puerta_Albedo.png'])
    vi_escada, n_escada, tex_escada = FileManager.load_obj_and_texture('objects/escada.obj', ['textures/Madera_clara_Albedo.png'])
    vi_chao, n_chao, tex_chao = FileManager.load_obj_and_texture('objects/chao.obj', ['textures/Jardin_raices_Diffuse.png'])
    vi_pomo, n_pomo, tex_pomo = FileManager.load_obj_and_texture('objects/pomo.obj', ['textures/pomo.jpeg'])
    vi_globo, n_globo, tex_globo = FileManager.load_obj_and_texture('objects/globo.obj', ['textures/globo.png'])
    vi_vassoura, n_vassoura, tex_vassoura = FileManager.load_obj_and_texture('objects/vassoura.obj', ['textures/vassoura.jpeg'])
    vi_tree, n_tree, tex_tree = FileManager.load_obj_and_texture('objects/tree.obj', ['textures/tree.png'])
    vi_abobora, n_abobora, tex_abobora = FileManager.load_obj_and_texture('objects/abobora.obj', ['textures/abobora.png'])


    base_casa = Model_3D(vi_base, n_base, DEFAULT_HUT, tex_base)
    teto = Model_3D(vi_teto, n_teto, DEFAULT_HUT, tex_teto)
    portas = Model_3D(vi_portas, n_portas, DEFAULT_HUT, tex_portas)
    escada = Model_3D(vi_escada, n_escada, DEFAULT_HUT, tex_escada)
    chao = Model_3D(vi_chao, n_chao, CHAO, tex_chao)
    pomo = Model_3D(vi_pomo, n_pomo, POMO, tex_pomo)
    globo = Model_3D(vi_globo, n_globo, GLOBO, tex_globo)
    vassoura = Model_3D(vi_vassoura, n_vassoura, DEFAULT_HUT, tex_vassoura)
    
    
    tree_positions = [(-20, -20), (10, -20), (-20, 20), (20, 20)]
    trees = create_n_models(vi_tree, n_tree, tex_tree, tree_positions, TREE)
   

    abobora_positions = [(-10, -10), (-5, -5), (-2, -5), (-5, -2)]
    aboboras = create_n_models(vi_abobora, n_abobora, tex_abobora, abobora_positions, ABOBORA)


    # ====== KEY MANAGER ======
    keymanager = KeyManager(window, renderer, view)
    mousemanager = MouseManager(window, view, projection)



    # prepare models to render
    renderer.add_model([
        base_casa, 
        teto, 
        portas, 
        escada, 
        chao, 
        globo, 
        pomo, 
        vassoura
    ] + trees + aboboras)

    """ keymanager.set_key(glfw.KEY_UP, lambda m: m.translate(0, 0.1, 0), tree)
    keymanager.set_key(glfw.KEY_DOWN, lambda m: m.translate(0, -0.1, 0), tree) """

    keymanager.set_key(glfw.KEY_UP, make_scaler("up", 1.1, 0.15), aboboras[0])
    keymanager.set_key(glfw.KEY_DOWN, make_scaler("down", 1.1, 0.15), aboboras[0])

    
    # show windows
    window.upload_data()
    window.show()
    window.enable()
    while not window.should_close():
        world_rotation(globo)
        renderer.render()

    window.terminate()

if __name__ == "__main__":
    main()
