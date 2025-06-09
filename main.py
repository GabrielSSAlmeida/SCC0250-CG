# 06/04/2025 18:00

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
    DEBUG = True
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
    # vi_pomo, n_pomo, tex_pomo = FileManager.load_obj_and_texture('objects/pomo.obj', ['textures/pomo.jpeg'])
    vi_globo, n_globo, tex_globo = FileManager.load_obj_and_texture('objects/globo.obj', ['textures/globo.png'])
    # vi_nimbus, n_nimbus, tex_nimbus = FileManager.load_obj_and_texture('objects/nimbus.obj', ['textures/nimbus.jpeg'])
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
    # pomo = Model_3D(vi_pomo, n_pomo, POMO, tex_pomo)
    globo = Model_3D(vi_globo, n_globo, GLOBO, tex_globo)
    # nimbus = Model_3D(vi_nimbus, n_nimbus, NIMBUS, tex_nimbus)
    mesa = Model_3D(vi_mesa, n_mesa, MESA, tex_mesa)
    sapo = Model_3D(vi_sapo, n_sapo, SAPO, tex_sapo)
    caixa = Model_3D(vi_caixa, n_caixa, CAIXA, tex_caixa)
    cartas = Model_3D(vi_cartas, n_cartas, CARTAS, tex_cartas)
    cadeira = Model_3D(vi_cadeira, n_cadeira, CADEIRA, tex_cadeira)
    poste = Model_3D(vi_poste, n_poste, POSTE, tex_poste)
    trofeu = Model_3D(vi_trofeu, n_trofeu, TROFEU, tex_trofeu)
    varinha = Model_3D(vi_varinha, n_varinha, VARINHA, tex_varinha)
    lamparina = Model_3D(vi_lamparina, n_lamparina, LAMPARINA, tex_lamparina)
    
    # ATENÇÃO: removi a translação inicial do sphereEx para que ele comece na posição da luz
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
        # pomo, 
        # nimbus, 
        mesa, 
        sapo, 
        cartas, 
        caixa,
        cadeira,
        # sphereIn, # sphere interno, permanece aqui
        sphereEx, # AGORA INCLUÍMOS O sphere EXTERNO AQUI
        poste,
        trofeu,
        varinha,
        lamparina,
    ] + trees + aboboras) # Adicionei aboboras aqui também


    # ABÓBORA
    keymanager.set_key(glfw.KEY_UP, make_scaler("up", 1.1, 0.15), aboboras[0])
    keymanager.set_key(glfw.KEY_DOWN, make_scaler("down", 1.1, 0.15), aboboras[0])

    # POMO DE OURO
    # keymanager.set_key(glfw.KEY_O, lambda m: m.rotate(5, 1, 0, 0), pomo)
    # keymanager.set_key(glfw.KEY_I, lambda m: m.rotate(5, 0, 1, 0), pomo)
    # keymanager.set_key(glfw.KEY_U, lambda m: m.rotate(5, 0, 0, 1), pomo)

    # # NIMBUS
    # keymanager.set_key(glfw.KEY_KP_4, lambda m: nimbus_translation(m, dx=-0.3, angle_y=180), nimbus)   
    # keymanager.set_key(glfw.KEY_KP_6, lambda m: nimbus_translation(m, dx=0.3, angle_x=90), nimbus)   
    # keymanager.set_key(glfw.KEY_KP_2, lambda m: nimbus_translation(m, dy=-0.3, angle_z=270), nimbus)  
    # keymanager.set_key(glfw.KEY_KP_5, lambda m: nimbus_translation(m, dy=0.3, angle_z=90), nimbus)   
    # keymanager.set_key(glfw.KEY_KP_1, lambda m: nimbus_translation(m, dz=-0.3, angle_y=90), nimbus)    
    # keymanager.set_key(glfw.KEY_KP_3, lambda m: nimbus_translation(m, dz=0.3, angle_y=270), nimbus)  


    # --- CONFIGURAR AS TECLAS GLOBAIS NO KeyManager ---
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

    # Ação de Toque Único (Toggle) para o modo de polígono
    keymanager.set_global_key_toggle(glfw.KEY_P, renderer.setPolygonMode)

    
    # show windows
    window.upload_data()

    # --- NOVA POINTLIGHT EXTERNA MÓVEL ---
    # Definir as duas posições para a luz se mover
    light_move_pos1 = glm.vec3(-2.09392,      7.35174,     -8.98131) # Posição inicial (sphereEx)
    light_move_pos2 = glm.vec3(3.0,     -0.625115,       3.0) # Posição final (sphereEx)
    
    # Variáveis de controle para a luz móvel
    current_light_state = 0 
    moving_light_progress = 0.0
    # Point Lights
    internal_lights_data = [
        { # Taça
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
            "position": light_move_pos1, # Posição inicial
            "ambient": glm.vec3(0.8, 0.8, 0.8), # Um pouco de ambiente
            "diffuse": glm.vec3(0.8, 0.8, 0.8), # Cor verde (ou a que preferir para diferenciar)
            "specular": glm.vec3(1.0, 1.0, 1.0), 
            "constant": 1.0,
            "linear": 0.07,
            "quadratic": 0.017, # Pode ajustar esta atenuação também
            "isOn": True,
        }
    ]

    internal_spotlight_data = [
        { # Taça
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

    
    def toggle_moving_light_to_destination():
        nonlocal current_light_state, moving_light_progress
        
        if current_light_state == 0: # Se está parada, começa a mover para a próxima posição
            current_external_light_visual_pos = external_lights_data[0]["position"]
            tolerance = 0.5 
            if glm.distance(current_external_light_visual_pos, light_move_pos1) < tolerance:
                current_light_state = 2 # Mover para pos2
                print("Luz Externa Móvel: Indo para Posição 2")
            elif glm.distance(current_external_light_visual_pos, light_move_pos2) < tolerance:
                current_light_state = 1 # Mover para pos1
                print("Luz Externa Móvel: Indo para Posição 1")
            else:
                current_light_state = 1
                print("Luz Externa Móvel: Posição desconhecida, indo para Posição 1")
            moving_light_progress = 0.0
        else:
            current_light_state = 0
            print("Luz Externa Móvel: Parada (movimento interrompido)")

    keymanager.set_global_key_toggle(glfw.KEY_M, toggle_moving_light_to_destination)

    # ====== FUNÇÕES PARA LIGAR/DESLIGAR LUZES ======
    def toggle_internal_light(idx):
        def toggle(_=None):
            internal_lights_data[idx]["isOn"] = not internal_lights_data[idx]["isOn"]
            ilumination.update_internal_light_is_on(idx, internal_lights_data[idx]["isOn"]) # Chamada correta
            print(f"Luz interna {idx} {'ligada' if internal_lights_data[idx]['isOn'] else 'desligada'}")
        return toggle

    def toggle_external_light(idx):
        def toggle(_=None):
            external_lights_data[idx]["isOn"] = not external_lights_data[idx]["isOn"]
            ilumination.update_external_light_is_on(idx, external_lights_data[idx]["isOn"]) # NOVO MÉTODO
            print(f"Luz externa {idx} {'ligada' if external_lights_data[idx]['isOn'] else 'desligada'}")
        return toggle

    def toggle_internal_spotlight(idx):
        def toggle(_=None):
            internal_spotlight_data[idx]["isOn"] = not internal_spotlight_data[idx]["isOn"]
            ilumination.update_internal_spotlight_is_on(idx, internal_spotlight_data[idx]["isOn"]) # Chamada correta
            print(f"Spotlight interna {idx} {'ligada' if internal_spotlight_data[idx]['isOn'] else 'desligada'}")
        return toggle

    def toggle_external_spotlight(idx):
        def toggle(_=None):
            # Descomente e use este bloco se você habilitar externalSpotLights no shader
            # external_spotlight_data[idx]["isOn"] = not external_spotlight_data[idx]["isOn"]
            # ilumination.update_external_spotlight_is_on(idx, external_spotlight_data[idx]["isOn"])
            print(f"Spotlight externa {idx} {'ligada' if external_spotlight_data[idx]['isOn'] else 'desligada'}")
        return toggle

    def toggle_dir_light():
        dir_light_data["isOn"] = not dir_light_data["isOn"]
        ilumination.update_dir_light_is_on(dir_light_data["isOn"]) # Chamada correta
        print(f"Luz direcional {'ligada' if dir_light_data['isOn'] else 'desligada'}")
    

    # --- NOVAS FUNÇÕES PARA LIGAR/DESLIGAR GRUPOS DE LUZES ---
    def toggle_wand_lights():
        # A luz da varinha é o ponto de luz interno 1 e o spotlight interno 1
        # Vamos verificar o estado atual de uma delas para decidir se ligamos ou desligamos
        # Se a point light da varinha estiver ligada, vamos desligar tudo. Se estiver desligada, ligar.
        
        # O índice 1 para internal_lights_data e internal_spotlight_data corresponde à varinha
        # based on your current internal_lights_data and internal_spotlight_data arrays.
        # (check the comments: { # Varinha } )
        
        current_state_point = internal_lights_data[1]["isOn"]
        current_state_spot = internal_spotlight_data[1]["isOn"]
        
        # Decide o novo estado: se qualquer uma estiver ligada, desliga tudo; senão, liga tudo.
        new_state = not (current_state_point or current_state_spot) 

        internal_lights_data[1]["isOn"] = new_state
        ilumination.update_internal_light_is_on(1, new_state)
        
        internal_spotlight_data[1]["isOn"] = new_state
        ilumination.update_internal_spotlight_is_on(1, new_state)
        
        print(f"Luzes da Varinha {'ligadas' if new_state else 'desligadas'}")

    def toggle_goblet_lights():
        # A luz da taça é o ponto de luz interno 0 e o spotlight interno 0
        # O índice 0 para internal_lights_data e internal_spotlight_data corresponde à taça
        # (check the comments: { # Taça } )

        current_state_point = internal_lights_data[0]["isOn"]
        current_state_spot = internal_spotlight_data[0]["isOn"]
        
        new_state = not (current_state_point or current_state_spot)

        internal_lights_data[0]["isOn"] = new_state
        ilumination.update_internal_light_is_on(0, new_state)
        
        internal_spotlight_data[0]["isOn"] = new_state
        ilumination.update_internal_spotlight_is_on(0, new_state)
        
        print(f"Luzes da Taça {'ligadas' if new_state else 'desligadas'}")

    # ====== ATRIBUIR TECLAS ======
    keymanager.set_global_key_toggle(glfw.KEY_1, toggle_goblet_lights) # Taça (Point + Spotlight)
    keymanager.set_global_key_toggle(glfw.KEY_2, toggle_wand_lights) # Varinha (Point + Spotlight)
    # Externa: 3
    keymanager.set_global_key_toggle(glfw.KEY_3, toggle_external_light(0))
    # Spotlights internas: 4, 5
    # keymanager.set_global_key_toggle(glfw.KEY_4, toggle_internal_spotlight(0)) # Taça Spotlight
    # keymanager.set_global_key_toggle(glfw.KEY_5, toggle_internal_spotlight(1)) # Varinha Spotlight
    # Spotlights externas: 6 (se houver)
    if len(external_spotlight_data) > 0:
        keymanager.set_global_key_toggle(glfw.KEY_4, toggle_external_spotlight(0))
    # Direcional: 0
    keymanager.set_global_key_toggle(glfw.KEY_0, toggle_dir_light)

    # --- NOVAS TECLAS PARA GRUPOS DE LUZES ---
    # Sugestões: KEY_Q para Taça, KEY_E para Varinha
    # keymanager.set_global_key_toggle(glfw.KEY_Q, toggle_goblet_lights) # Ligar/desligar luzes da Taça (Point + Spotlight)
    # keymanager.set_global_key_toggle(glfw.KEY_E, toggle_wand_lights)    # Ligar/desligar luzes da Varinha (Point + Spotlight)


    window.show()
    window.enable()

    last_frame_time = glfw.get_time()
    while not window.should_close():
        current_frame_time = glfw.get_time()
        deltaTime = current_frame_time - last_frame_time
        last_frame_time = current_frame_time

        #view.deltaTime = deltaTime
        
        world_rotation(globo)
        
        # --- LÓGICA DE MOVIMENTO DA LUZ EXTERNA NO LOOP PRINCIPAL ---
        if current_light_state != 0: # Se a luz está em estado de movimento
            move_speed = 10.0 * deltaTime # Ajuste a velocidade conforme necessário
            
            target_pos = None
            start_pos = external_lights_data[0]["position"] # Posição atual da luz

            if current_light_state == 1: # Indo para pos1
                target_pos = light_move_pos1
            elif current_light_state == 2: # Indo para pos2
                target_pos = light_move_pos2

            if target_pos is not None:
                # Calcula a distância restante
                distance_to_target = glm.distance(start_pos, target_pos)

                if distance_to_target > move_speed: # Se ainda não chegou, move
                    # Normaliza o vetor direção e move um passo
                    direction_vector = glm.normalize(target_pos - start_pos)
                    current_external_light_pos = start_pos + direction_vector * move_speed
                    external_lights_data[0]["position"] = current_external_light_pos
                    ilumination.update_external_light_position(0, current_external_light_pos)
                else: # Chegou ao destino
                    external_lights_data[0]["position"] = target_pos # Define a posição exata
                    ilumination.update_external_light_position(0, target_pos)
                    current_light_state = 0 # Para o movimento
                    print("Luz Externa Móvel: Chegou ao destino e parou.")
        
        # --- NOVO: ATUALIZAR A POSIÇÃO DO sphere_EX PARA SER A MESMA DA LUZ EXTERNA ---
        # Certifique-se de que a posição da luz foi atualizada antes de usar.
        # A variável `current_external_light_pos` ou `external_lights_data[0]["position"]`
        # já conterá a posição mais recente da luz.
        light_pos = external_lights_data[0]["position"]
        sphereEx.set_position(light_pos.x, light_pos.y, light_pos.z)

        world_rotation(globo)
        renderer.render(light_factors["ka"], light_factors["kd"], light_factors["ks"])

    window.terminate()

if __name__ == "__main__":
    main()