# keymanager.py
import glfw
import glm

# Mantém o estado das teclas que queremos monitorar continuamente (para "PRESS" e "REPEAT")
# Pode ser expandido com mais teclas se necessário.
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
    # Novos para iluminação
    glfw.KEY_Z: False,
    glfw.KEY_X: False,
    glfw.KEY_C: False,
    glfw.KEY_V: False,
    glfw.KEY_B: False,
    glfw.KEY_N: False,
}

class KeyManager:
    def __init__(self, window, renderer, view, debug=False):
        self.window = window
        self.renderer = renderer
        self.key_map = {} # Mapas de chave para (ação, modelos) para ações que atuam em modelos
        self.global_key_map = {} # Novo: Mapas de chave para ação global
        self.view = view
        self.debug = debug
        glfw.set_key_callback(window.glfw_window, self.key_event)

    def set_key(self, key, action, models):
        """
        Associa uma função a um modelo(s) para uma tecla específica.
        Usado para ações que modificam modelos.
        """
        if not isinstance(models, list):
            models = [models]
        self.key_map[key] = (action, models)
    
    # --- NOVO MÉTODO: set_global_key ---
    def set_global_key(self, key, action):
        """
        Associa uma função a uma tecla específica, sem ligá-la a modelos.
        Usado para ações globais (ex: mudar iluminação, modo de polígono).
        """
        self.global_key_map[key] = action
    # ------------------------------------

    def key_event(self, w, key, scancode, action, mods):
        # --- Lógica para teclas de pressão única ou que iniciam um estado ---
        # Poligon Mode (pode ser um toggle, então só PRESS ou REPEAT faz sentido)
        if key == glfw.KEY_P and (action == glfw.PRESS or action == glfw.REPEAT):
            self.renderer.setPolygonMode()
        # Escape para fechar a janela
        if key == glfw.KEY_ESCAPE and (action == glfw.PRESS or action == glfw.REPEAT):
            self.window.close()
        
        # --- Atualizar o estado global das teclas ---
        if key in key_state:
            if action == glfw.PRESS:
                key_state[key] = True
            elif action == glfw.RELEASE: # Importante para liberar o estado da tecla
                key_state[key] = False

        # --- Processar ações de câmera (W, S, A, D, SPACE, L_CTRL) ---
        # Estas podem ser processadas diretamente aqui ou você pode movê-las
        # para callbacks separados para maior modularidade, similar aos modelos.
        # Por enquanto, mantemos aqui para simplicidade com a câmera.
        cameraSpeed = 200 * self.view.deltaTime # Mantenha o cálculo do delta time atualizado
        
        if key_state[glfw.KEY_W]:
            self.view.cameraPos += cameraSpeed * self.view.cameraFront
            if self.debug: print(f"{self.view.cameraPos}")
        if key_state[glfw.KEY_S]:
            self.view.cameraPos -= cameraSpeed * self.view.cameraFront
            if self.debug: print(f"{self.view.cameraPos}")
        if key_state[glfw.KEY_A]:
            self.view.cameraPos -= glm.normalize(glm.cross(self.view.cameraFront, self.view.cameraUp)) * cameraSpeed
            if self.debug: print(f"{self.view.cameraPos}")
        if key_state[glfw.KEY_D]:
            self.view.cameraPos += glm.normalize(glm.cross(self.view.cameraFront, self.view.cameraUp)) * cameraSpeed
            if self.debug: print(f"{self.view.cameraPos}")
        if key_state[glfw.KEY_SPACE]:
            self.view.cameraPos += cameraSpeed * glm.vec3(0.0, 1.0, 0.0)
        if key_state[glfw.KEY_LEFT_CONTROL]:
            self.view.cameraPos -= cameraSpeed * glm.vec3(0.0, 1.0, 0.0)

        self.view.update_view_matrix()
        
        # --- Processar ações globais (NOVAS) ---
        # Se a tecla está pressionada e tem uma ação global associada
        for k, action_func in self.global_key_map.items():
            if k in key_state and key_state[k]:
                action_func() # Chama a função global

        # --- Processar ações de modelos ---
        # Se a tecla está pressionada e tem uma ação de modelo associada
        for k, (action_func, models) in self.key_map.items():
            if k in key_state and key_state[k]:
                for m in models:
                    action_func(m)
                    # if self.debug: print(f"{m.type}: X: {m.modelConfig["t_x"]}, Y:{m.modelConfig["t_y"]}, Z:{m.modelConfig["t_z"]}")