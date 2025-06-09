# keymanager.py
import glfw
import glm

# Mantém o estado das teclas que queremos monitorar continuamente (para "PRESS" e "REPEAT")
key_state = {
    # HARRY (exemplo, se você tiver um Harry)
    glfw.KEY_Y: False,
    # POMO
    glfw.KEY_UP: False,
    glfw.KEY_DOWN: False,
    glfw.KEY_LEFT: False,
    glfw.KEY_RIGHT: False,
    glfw.KEY_I: False,
    glfw.KEY_O: False,
    glfw.KEY_L: False,
    glfw.KEY_K: False,
    # VASSOURA (Câmera)
    glfw.KEY_W: False,
    glfw.KEY_S: False,
    glfw.KEY_A: False,
    glfw.KEY_D: False,
    glfw.KEY_SPACE: False,
    glfw.KEY_LEFT_CONTROL: False,
    # Novos para iluminação (contínuos)
    glfw.KEY_Z: False,
    glfw.KEY_X: False,
    glfw.KEY_C: False,
    glfw.KEY_V: False,
    glfw.KEY_B: False,
    glfw.KEY_N: False,
    # NOVO: Tecla para a luz móvel (toggle)
    glfw.KEY_M: False,
    glfw.KEY_1: False,
    glfw.KEY_2: False,
    glfw.KEY_3: False,
    glfw.KEY_4: False,
    glfw.KEY_0: False,
}

class KeyManager:
    def __init__(self, window, renderer, view, debug=False):
        self.window = window
        self.renderer = renderer
        self.key_map = {} # Mapas de chave para (ação, modelos) para ações que atuam em modelos (contínuas)
        
        # NOVO: Duas estruturas para ações globais
        self.global_key_map_continuous = {} # Para ações que se repetem enquanto a tecla está segurada (ex: iluminação)
        self.global_key_map_toggle = {}     # Para ações de toque único (ex: ligar/desligar luz, trocar polígono)
        
        self.view = view
        self.debug = debug
        
        # NOVO: Conjunto para controlar teclas de 'toggle' que já foram processadas no PRESS
        self.processed_toggle_keys = set() 
        
        glfw.set_key_callback(window.glfw_window, self.key_event)

    def set_key(self, key, action, models):
        """
        Associa uma função a um modelo(s) para uma tecla específica.
        Usado para ações que modificam modelos (presume-se que sejam contínuas).
        """
        if not isinstance(models, list):
            models = [models]
        self.key_map[key] = (action, models)
    
    # NOVO MÉTODO: set_global_key_continuous
    def set_global_key_continuous(self, key, action):
        """
        Associa uma função a uma tecla para uma ação global que se repete
        enquanto a tecla está pressionada.
        """
        self.global_key_map_continuous[key] = action
    
    # NOVO MÉTODO: set_global_key_toggle
    def set_global_key_toggle(self, key, action):
        """
        Associa uma função a uma tecla para uma ação global de toque único (toggle).
        A ação é disparada apenas no evento glfw.PRESS.
        """
        self.global_key_map_toggle[key] = action

    def key_event(self, w, key, scancode, action, mods):
        # --- Atualizar o estado global das teclas monitoradas continuamente ---
        if key in key_state:
            if action == glfw.PRESS:
                key_state[key] = True
            elif action == glfw.RELEASE:
                key_state[key] = False
                # Se a tecla foi solta, a removemos do conjunto de teclas de 'toggle' processadas
                if key in self.processed_toggle_keys:
                    self.processed_toggle_keys.remove(key)

        # --- Processar ações de Toque Único (Toggle) ---
        if action == glfw.PRESS: # Apenas no pressionar inicial da tecla
            if key in self.global_key_map_toggle and key not in self.processed_toggle_keys:
                self.global_key_map_toggle[key]() # Chama a função de toggle
                self.processed_toggle_keys.add(key) # Marca como processada para este toque

        # --- Lógica para Poligon Mode (agora tratado como toggle global) ---
        # Removi daqui e movi para `set_global_key_toggle` no `main.py`
        # para centralizar a configuração de teclas.

        # --- Escape para fechar a janela (ainda pode ser aqui ou como toggle global) ---
        if key == glfw.KEY_ESCAPE and (action == glfw.PRESS or action == glfw.REPEAT):
            self.window.close()
        
        # --- Processar ações de câmera (W, S, A, D, SPACE, L_CTRL) ---
        # Este bloco permanece para ações contínuas da câmera
        cameraSpeed = 180 * self.view.deltaTime
        
        if key_state[glfw.KEY_W]:
            self.view.cameraPos += cameraSpeed * self.view.cameraFront
            if self.debug: print(f"{self.view.cameraPos}, {self.view.cameraFront}")
        if key_state[glfw.KEY_S]:
            self.view.cameraPos -= cameraSpeed * self.view.cameraFront
            if self.debug: print(f"{self.view.cameraPos}, {self.view.cameraFront}")
        if key_state[glfw.KEY_A]:
            self.view.cameraPos -= glm.normalize(glm.cross(self.view.cameraFront, self.view.cameraUp)) * cameraSpeed
            if self.debug: print(f"{self.view.cameraPos}, {self.view.cameraFront}")
        if key_state[glfw.KEY_D]:
            self.view.cameraPos += glm.normalize(glm.cross(self.view.cameraFront, self.view.cameraUp)) * cameraSpeed
            if self.debug: print(f"{self.view.cameraPos}, {self.view.cameraFront}")
        if key_state[glfw.KEY_SPACE]:
            self.view.cameraPos += cameraSpeed * glm.vec3(0.0, 1.0, 0.0)
        if key_state[glfw.KEY_LEFT_CONTROL]:
            self.view.cameraPos -= cameraSpeed * glm.vec3(0.0, 1.0, 0.0)

        self.view.update_view_matrix()
        
        # --- Processar ações globais Contínuas ---
        # Se a tecla está pressionada (PRESS ou REPEAT) e tem uma ação global contínua associada
        for k, action_func in self.global_key_map_continuous.items():
            if k in key_state and key_state[k]:
                action_func() # Chama a função global contínua

        # --- Processar ações de modelos (já eram contínuas) ---
        for k, (action_func, models) in self.key_map.items():
            if k in key_state and key_state[k]:
                for m in models:
                    action_func(m)
                    # if self.debug: print(f"{m.type}: X: {m.modelConfig["t_x"]}, Y:{m.modelConfig["t_y"]}, Z:{m.modelConfig["t_z"]}")