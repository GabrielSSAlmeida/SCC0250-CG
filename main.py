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
from models.renderer import Renderer
from utils.file_loader import FileManager
from keymanager import KeyManager
from mousemanager import MouseManager
from shaders.shader_s import Shader
from utils.custom_keys_callbacks import *
from OpenGL.GL import *
from config import *
import glfw
import glm

def main():
    fov = 45.0
    deltaTime = 0.005

    window = Window()

    view = View(glm.vec3(0.0, 10.0, 5.0), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0), deltaTime)
    projection = Projection(window.altura, window.largura, fov)
    renderer = Renderer(window, view, projection.mat_projection)


    vi_base, n_base, tex_base = FileManager.load_obj_and_texture('objects/base_casa.obj', ['textures/Pared_piedra_musgo_2K_Albedo.png'])
    vi_teto, n_teto, tex_teto = FileManager.load_obj_and_texture('objects/teto.obj', ['textures/Metal_oxidado_Azul_Albedo.png'])
    vi_portas, n_portas, tex_portas = FileManager.load_obj_and_texture('objects/portas.obj', ['textures/Madera_puerta_Albedo.png'])
    vi_escada, n_escada, tex_escada = FileManager.load_obj_and_texture('objects/escada.obj', ['textures/Madera_clara_Albedo.png'])
    vi_chao, n_chao, tex_chao = FileManager.load_obj_and_texture('objects/chao.obj', ['textures/Jardin_raices_Diffuse.png'])
    vi_pomo, n_pomo, tex_pomo = FileManager.load_obj_and_texture('objects/pomo.obj', ['textures/pomo.jpeg'])
    vi_globo, n_globo, tex_globo = FileManager.load_obj_and_texture('objects/globo.obj', ['textures/globo.png'])
    vi_nimbus, n_nimbus, tex_nimbus = FileManager.load_obj_and_texture('objects/nimbus.obj', ['textures/nimbus.jpeg'])
    vi_tree, n_tree, tex_tree = FileManager.load_obj_and_texture('objects/tree.obj', ['textures/tree.png'])
    vi_abobora, n_abobora, tex_abobora = FileManager.load_obj_and_texture('objects/abobora.obj', ['textures/abobora.png'])
    vi_mesa, n_mesa, tex_mesa = FileManager.load_obj_and_texture('objects/mesa.obj', ['textures/Madera_puerta_Albedo.png'])
    vi_sapo, n_sapo, tex_sapo = FileManager.load_obj_and_texture('objects/sapo.obj', ['textures/sapo.png'])
    vi_cartas, n_cartas, tex_cartas = FileManager.load_obj_and_texture('objects/cartas.obj', ['textures/cartas.png'])
    vi_caixa, n_caixa, tex_caixa = FileManager.load_obj_and_texture('objects/caixa.obj', ['textures/caixa.png'])
    vi_cadeira, n_cadeira, tex_cadeira = FileManager.load_obj_and_texture('objects/cadeira.obj', ['textures/Madera_puerta_Albedo.png'])
    

    base_casa = Model_3D(vi_base, n_base, DEFAULT_HUT, tex_base)
    teto = Model_3D(vi_teto, n_teto, DEFAULT_HUT, tex_teto)
    portas = Model_3D(vi_portas, n_portas, DEFAULT_HUT, tex_portas)
    escada = Model_3D(vi_escada, n_escada, DEFAULT_HUT, tex_escada)
    chao = Model_3D(vi_chao, n_chao, CHAO, tex_chao)
    pomo = Model_3D(vi_pomo, n_pomo, POMO, tex_pomo)
    globo = Model_3D(vi_globo, n_globo, GLOBO, tex_globo)
    nimbus = Model_3D(vi_nimbus, n_nimbus, NIMBUS, tex_nimbus)
    mesa = Model_3D(vi_mesa, n_mesa, MESA, tex_mesa)
    sapo = Model_3D(vi_sapo, n_sapo, SAPO, tex_sapo)
    caixa = Model_3D(vi_caixa, n_caixa, CAIXA, tex_caixa)
    cartas = Model_3D(vi_cartas, n_cartas, CARTAS, tex_cartas)
    cadeira = Model_3D(vi_cadeira, n_cadeira, CADEIRA, tex_cadeira)
    
    
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
        nimbus, 
        mesa, 
        sapo, 
        cartas, 
        caixa,
        cadeira,
    ] + trees + aboboras)


    # ABÓBORA
    keymanager.set_key(glfw.KEY_UP, make_scaler("up", 1.1, 0.15), aboboras[0])
    keymanager.set_key(glfw.KEY_DOWN, make_scaler("down", 1.1, 0.15), aboboras[0])

    # POMO DE OURO
    keymanager.set_key(glfw.KEY_O, lambda m: m.rotate(5, 1, 0, 0), pomo)
    keymanager.set_key(glfw.KEY_I, lambda m: m.rotate(5, 0, 1, 0), pomo)
    keymanager.set_key(glfw.KEY_U, lambda m: m.rotate(5, 0, 0, 1), pomo)

    # NIMBUS
    keymanager.set_key(glfw.KEY_KP_4, lambda m: nimbus_translation(m, dx=-0.3, angle_y=180), nimbus)   
    keymanager.set_key(glfw.KEY_KP_6, lambda m: nimbus_translation(m, dx=0.3, angle_x=90), nimbus)   
    keymanager.set_key(glfw.KEY_KP_2, lambda m: nimbus_translation(m, dy=-0.3, angle_z=270), nimbus)  
    keymanager.set_key(glfw.KEY_KP_5, lambda m: nimbus_translation(m, dy=0.3, angle_z=90), nimbus)   
    keymanager.set_key(glfw.KEY_KP_1, lambda m: nimbus_translation(m, dz=-0.3, angle_y=90), nimbus)    
    keymanager.set_key(glfw.KEY_KP_3, lambda m: nimbus_translation(m, dz=0.3, angle_y=270), nimbus)   

    # show windows
    window.upload_data()
    window.show()
    window.enable()

    pointLightPositions = [
        glm.vec3( 10.0,  10.0,  10.0),
    ]

    window.shader.use()
    window.shader.setInt("material.diffuse", 0)
    window.shader.setInt("material.specular", 1)

    window.shader.setVec3("dirLight.direction", -0.2, -1.0, -0.3)  # Exemplo: luz vindo de cima na diagonal

    window.shader.setVec3("dirLight.ambient", 0.2, 0.2, 0.2)   # Luz ambiente moderada
    window.shader.setVec3("dirLight.diffuse", 0.5, 0.5, 0.5)   # Luz difusa
    #window.shader.setVec3("dirLight.specular", 1.0, 1.0, 1.0)  # Reflexos brilhantes


    window.shader.setVec3("pointLights[0].position", pointLightPositions[0])
    window.shader.setVec3("pointLights[0].ambient", 0.1, 0.1, 0.05)
    window.shader.setVec3("pointLights[0].diffuse", 0.9, 0.9, 0.5)
    window.shader.setVec3("pointLights[0].specular", 1.0, 1.0, 0.6)
    window.shader.setFloat("pointLights[0].constant", 1.0)
    window.shader.setFloat("pointLights[0].linear", 0.09)
    window.shader.setFloat("pointLights[0].quadratic", 0.032)


    while not window.should_close():
        world_rotation(globo)
        renderer.render()

    window.terminate()

if __name__ == "__main__":
    main()
