# 09/05/2025 19:00

""" 
    SCC0250 - Computação Gráfica

    Projeto 3

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
from models.ilumination import Ilumination
from utils.custom_keys_callbacks import *
from OpenGL.GL import *
from config import *
import glfw
import glm

def main():
    DEBUG = False
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
    vi_globo, n_globo, tex_globo = FileManager.load_obj_and_texture('objects/globo.obj', ['textures/globo.png'])
    vi_tree, n_tree, tex_tree = FileManager.load_obj_and_texture('objects/tree.obj', ['textures/tree.png'])
    vi_abobora, n_abobora, tex_abobora = FileManager.load_obj_and_texture('objects/abobora.obj', ['textures/abobora.png'])
    vi_mesa, n_mesa, tex_mesa = FileManager.load_obj_and_texture('objects/mesa.obj', ['textures/Madera_puerta_Albedo.png'])
    vi_sapo, n_sapo, tex_sapo = FileManager.load_obj_and_texture('objects/sapo.obj', ['textures/sapo.png'])
    vi_cartas, n_cartas, tex_cartas = FileManager.load_obj_and_texture('objects/cartas.obj', ['textures/cartas.png'])
    vi_caixa, n_caixa, tex_caixa = FileManager.load_obj_and_texture('objects/caixa.obj', ['textures/caixa.png'])
    vi_cadeira, n_cadeira, tex_cadeira = FileManager.load_obj_and_texture('objects/cadeira.obj', ['textures/Madera_puerta_Albedo.png'])
    vi_sphere, n_sphere, tex_sphere = FileManager.load_obj_and_texture('objects/low_poly_sphere.obj', ['textures/branco.jpg'])
    vi_poste, n_poste, tex_poste = FileManager.load_obj_and_texture('objects/lamp_street_.obj', ['textures/lamp_street.png'])
    vi_trofeu, n_trofeu, tex_trofeu = FileManager.load_obj_and_texture('objects/trofeu.obj', ['textures/trofeu.png'])
    vi_varinha, n_varinha, tex_varinha = FileManager.load_obj_and_texture('objects/varinha.obj', ['textures/varinha.png'])
    vi_lamparina, n_lamparina, tex_lamparina = FileManager.load_obj_and_texture('objects/lamparina.obj', ['textures/lamparina.png'])
    

    base_casa = Model_3D(vi_base, n_base, DEFAULT_HUT, tex_base)
    teto = Model_3D(vi_teto, n_teto, DEFAULT_HUT, tex_teto)
    portas = Model_3D(vi_portas, n_portas, DEFAULT_HUT, tex_portas)
    escada = Model_3D(vi_escada, n_escada, DEFAULT_HUT, tex_escada)
    chao = Model_3D(vi_chao, n_chao, CHAO, tex_chao)
    globo = Model_3D(vi_globo, n_globo, GLOBO, tex_globo)
    mesa = Model_3D(vi_mesa, n_mesa, MESA, tex_mesa)
    sapo = Model_3D(vi_sapo, n_sapo, SAPO, tex_sapo)
    caixa = Model_3D(vi_caixa, n_caixa, CAIXA, tex_caixa)
    cartas = Model_3D(vi_cartas, n_cartas, CARTAS, tex_cartas)
    cadeira = Model_3D(vi_cadeira, n_cadeira, CADEIRA, tex_cadeira)
    poste = Model_3D(vi_poste, n_poste, POSTE, tex_poste)
    trofeu = Model_3D(vi_trofeu, n_trofeu, TROFEU, tex_trofeu)
    varinha = Model_3D(vi_varinha, n_varinha, VARINHA, tex_varinha)
    lamparina = Model_3D(vi_lamparina, n_lamparina, LAMPARINA, tex_lamparina)
    
    sphereEx = Model_3D(vi_sphere, n_sphere, SPHERE, tex_sphere)


    tree_positions = [(-20, -20), (10, -20), (-20, 20), (20, 20)]
    trees = create_n_models(vi_tree, n_tree, tex_tree, tree_positions, TREE)

    abobora_positions = [(-10, -10), (-5, -5), (-2, -5), (-5, -2)]
    aboboras = create_n_models(vi_abobora, n_abobora, tex_abobora, abobora_positions, ABOBORA)


    # ====== KEY MANAGER ======
    keymanager = KeyManager(window, renderer, view, debug=DEBUG)
    mousemanager = MouseManager(window, view, projection)

    # prepare models to render
    renderer.add_model([
        base_casa, 
        teto, 
        portas, 
        escada, 
        chao, 
        globo, 
        mesa, 
        sapo, 
        cartas, 
        caixa,
        cadeira,
        sphereEx,
        poste,
        trofeu,
        varinha,
        lamparina,
    ] + trees + aboboras)


    # ABÓBORA
    keymanager.set_key(glfw.KEY_UP, make_scaler("up", 1.1, 0.15), aboboras[0])
    keymanager.set_key(glfw.KEY_DOWN, make_scaler("down", 1.1, 0.15), aboboras[0])


    light_factors = {
        "ka": 1.0,
        "kd": 1.0,
        "ks": 1.0
    }
    keymanager.set_global_key_continuous(glfw.KEY_Z, lambda: adjust_light_up(light_factors, "ka"))
    keymanager.set_global_key_continuous(glfw.KEY_X, lambda: adjust_light_down(light_factors, "ka"))
    keymanager.set_global_key_continuous(glfw.KEY_C, lambda: adjust_light_up(light_factors, "kd"))
    keymanager.set_global_key_continuous(glfw.KEY_V, lambda: adjust_light_down(light_factors, "kd"))
    keymanager.set_global_key_continuous(glfw.KEY_B, lambda: adjust_light_up(light_factors, "ks"))
    keymanager.set_global_key_continuous(glfw.KEY_N, lambda: adjust_light_down(light_factors, "ks"))
    

    # show windows
    window.upload_data()

    light_move_pos1 = glm.vec3(-2.09392, 7.35174, -8.98131) 
    light_move_pos2 = glm.vec3(3.0, -0.625115, 3.0)

    
    current_light_state = [0]
    # Point Lights
    internal_lights_data = [
        { # Trofeu
            "position": glm.vec3(-0.5, -3.0, 12.3),
            "ambient": glm.vec3(0.0, 0.2, 0.8),   
            "diffuse": glm.vec3(0.0, 0.4, 1.0),     
            "specular": glm.vec3(0.0, 0.6, 1.0),   
            "constant": 1.0,
            "linear": 0.35,
            "quadratic": 0.44,
            "isOn": True,
        },
        { # Varinha
            "position": glm.vec3(4.49986, -1.16163, 11.8),
            "ambient": glm.vec3(0.2, 0.2, 0.2),
            "diffuse": glm.vec3(1.0, 1.0, 1.0),
            "specular": glm.vec3(1.0, 1.0, 1.0),
            "constant": 1.0,
            "linear": 0.09,
            "quadratic": 50.0,
            "isOn": True,
        }

    ]
    external_lights_data = [
        {
            "position": light_move_pos1, 
            "ambient": glm.vec3(0.8, 0.8, 0.8), 
            "diffuse": glm.vec3(0.8, 0.8, 0.8), 
            "specular": glm.vec3(1.0, 1.0, 1.0), 
            "constant": 1.0,
            "linear": 0.07,
            "quadratic": 0.017, 
            "isOn": True,
        }
    ]

    internal_spotlight_data = [
        { # Trofeu
            "position": glm.vec3(-0.5, -3.0, 12.3),
            "direction": glm.vec3(0.0, 1.0, 0.0),
            "ambient": glm.vec3(0.0, 0.0, 0.0),   
            "diffuse": glm.vec3(0.0, 0.4, 1.0),     
            "specular": glm.vec3(0.0, 0.6, 1.0),   
            "constant": 1.0,
            "linear": 0.09,
            "quadratic": 0.032,
            "cutOff": glm.cos(glm.radians(12.5)),
            "outerCutOff": glm.cos(glm.radians(15.0)),
            "isOn": True,
        },
        { # Varinha
            "position": glm.vec3(4.49986, -1.16163, 11.8),
            "direction": glm.vec3(0.873249, 0.147809, -0.464315),
            "ambient": glm.vec3(0.0, 0.0, 0.0),
            "diffuse": glm.vec3(0.8, 0.8, 0.8),
            "specular": glm.vec3(0.8, 0.8, 0.8),
            "constant": 1.0,
            "linear": 0.09,
            "quadratic": 0.032,
            "cutOff": glm.cos(glm.radians(50.0)), 
            "outerCutOff": glm.cos(glm.radians(60.5)),
            "isOn": True,
        }
    ]
    external_spotlight_data = [
    ]

    # Direcional Light
    dir_light_data = {
        "direction": glm.vec3(-0.2, -1.0, -0.3),
        "ambient": glm.vec3(0.05, 0.05, 0.05),
        "diffuse": glm.vec3(0.4, 0.4, 0.4),
        "isOn": True,
    }


    ilumination = Ilumination(
        window.program,
        [internal_lights_data, len(internal_lights_data)],
        [external_lights_data, len(external_lights_data)],
        [internal_spotlight_data, len(internal_spotlight_data)],
        [external_spotlight_data, len(external_spotlight_data)],
        dir_light_data,
    )

    
    keymanager.set_global_key_toggle(glfw.KEY_M, lambda: toggle_moving_light_to_destination(external_lights_data, light_move_pos1, light_move_pos2, ilumination, current_light_state))
    keymanager.set_global_key_toggle(glfw.KEY_1, lambda: toggle_goblet_lights(internal_lights_data, internal_spotlight_data, ilumination)) # Trofeu (Point + Spotlight)
    keymanager.set_global_key_toggle(glfw.KEY_2, lambda: toggle_wand_lights(internal_lights_data, internal_spotlight_data, ilumination)) # Varinha (Point + Spotlight)
    keymanager.set_global_key_toggle(glfw.KEY_3, make_toggle_external_light(0, external_lights_data, ilumination)) # Externa
    keymanager.set_global_key_toggle(glfw.KEY_4, lambda: toggle_dir_light(dir_light_data, ilumination)) # Direcional


    window.show()
    window.enable()

    last_frame_time = glfw.get_time()
    while not window.should_close():
        current_frame_time = glfw.get_time()
        deltaTime = current_frame_time - last_frame_time
        last_frame_time = current_frame_time

        world_rotation(globo)
        
        if current_light_state[0] != 0: 
            move_speed = 10.0 * deltaTime 
            
            target_pos = None
            start_pos = external_lights_data[0]["position"] 

            if current_light_state[0] == 1: 
                target_pos = light_move_pos1
            elif current_light_state[0] == 2: 
                target_pos = light_move_pos2

            if target_pos is not None:
                distance_to_target = glm.distance(start_pos, target_pos)

                if distance_to_target > move_speed: 
                    direction_vector = glm.normalize(target_pos - start_pos)
                    current_external_light_pos = start_pos + direction_vector * move_speed
                    external_lights_data[0]["position"] = current_external_light_pos
                    ilumination.update_external_light_position(0, current_external_light_pos)
                else: 
                    external_lights_data[0]["position"] = target_pos
                    ilumination.update_external_light_position(0, target_pos)
                    current_light_state[0] = 0
        
        light_pos = external_lights_data[0]["position"]
        sphereEx.set_position(light_pos.x, light_pos.y, light_pos.z)

        world_rotation(globo)
        renderer.render(light_factors["ka"], light_factors["kd"], light_factors["ks"])

    window.terminate()

if __name__ == "__main__":
    main()