import glfw
import glm

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
    def __init__(self, window, renderer, view):
        self.window = window
        self.renderer = renderer
        self.key_map = {}
        self.view = view
        glfw.set_key_callback(window.glfw_window, self.key_event)

    # Sets a specific function to a model for a key
    def set_key(self, key, action, models):
        if not isinstance(models, list):
            models = [models]
        self.key_map[key] = (action, models)

    def key_event(self, w, key, scancode, action, mods):
        if key == glfw.KEY_P and (action == glfw.PRESS or action == glfw.REPEAT):
            self.renderer.setPolygonMode()
        if key == glfw.KEY_ESCAPE and (action == glfw.PRESS or action == glfw.REPEAT):
            self.window.close()

        cameraSpeed = 200 * self.view.deltaTime

        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            self.view.cameraPos += cameraSpeed * self.view.cameraFront
        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            self.view.cameraPos -= cameraSpeed * self.view.cameraFront
        if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
            self.view.cameraPos -= glm.normalize(glm.cross(self.view.cameraFront, self.view.cameraUp)) * cameraSpeed
        if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
            self.view.cameraPos += glm.normalize(glm.cross(self.view.cameraFront, self.view.cameraUp)) * cameraSpeed
        
        if key == glfw.KEY_SPACE and (action == glfw.PRESS or action == glfw.REPEAT):
            self.view.cameraPos += cameraSpeed * glm.vec3(0.0, 1.0, 0.0)

        if key == glfw.KEY_LEFT_CONTROL and (action == glfw.PRESS or action == glfw.REPEAT):
            self.view.cameraPos -= cameraSpeed * glm.vec3(0.0, 1.0, 0.0)

        self.view.update_view_matrix()

        # Model keys
        if action == 1 and (key in self.key_map):
            key_state[key] = True
        elif action == 0 and (key in self.key_map):
            key_state[key] = False

        for key in key_state:
            if key_state[key]:
                func, model = self.key_map[key]
                if not isinstance(model, list):
                    model = [model]
                for m in model:
                    func(m)