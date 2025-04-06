import glfw

key_state = {
        #  HARRY
        glfw.KEY_Y: False,
        #  POMO
        glfw.KEY_UP: False,
        glfw.KEY_DOWN: False,
        glfw.KEY_LEFT: False,
        glfw.KEY_RIGHT: False,
        glfw.KEY_I: False,
        glfw.KEY_O: False,
        glfw.KEY_L: False,
        glfw.KEY_K: False,
        # VASSOURA
        glfw.KEY_W: False,
        glfw.KEY_S: False,
        glfw.KEY_A: False,
        glfw.KEY_D: False,
}

class KeyManager:
    def __init__(self, window, renderer):
        self.window = window
        self.renderer = renderer
        self.key_map = {}
        glfw.set_key_callback(window.glfw_window, self.key_event)

    # Sets a specific function to a model for a key
    def set_key(self, key, action, models):
        if not isinstance(models, list):
            models = [models]
        self.key_map[key] = (action, models)

    def key_event(self, w, key, scancode, action, mods):
        # General scene keys
        if key == glfw.KEY_P and (action == glfw.PRESS or action == glfw.REPEAT):
            self.renderer.setPolygonMode()
        if key == glfw.KEY_ESCAPE and (action == glfw.PRESS or action == glfw.REPEAT):
            self.window.close()

        # Keys referring to a model
        if action == 1 and (key in self.key_map):
            key_state[key] = True
        elif action == 0 and (key in self.key_map):
            key_state[key] = False

        # runs the functions of all pressed keys (state = True)
        for key in key_state:
            if key_state[key] == True:
                func, model = self.key_map[key]
                if not isinstance(model, list):
                    model = [model]
                for m in model:
                    func(m)