import glfw

class KeyManager:
    def __init__(self, window):
        self.window = window
        self.key_map = {}

    def set_key(self, key, action, targets):
        """
        Registra uma tecla e sua ação associada.
        :param key: tecla do GLFW (ex: glfw.KEY_W)
        :param action: função a ser executada com o(s) alvo(s)
        :param targets: um único alvo ou uma lista de alvos
        """
        if not isinstance(targets, list):
            targets = [targets]
        self.key_map[key] = (action, targets)

    def exec_keys(self):
        """
        Checa as teclas pressionadas e executa as ações correspondentes
        """
        for key, (action, targets) in self.key_map.items():
            if glfw.get_key(self.window, key) == glfw.PRESS:
                for target in targets:
                    action(target)
