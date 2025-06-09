# keymanager.py
import glfw
import glm

key_state = {
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
    # View
    glfw.KEY_W: False,
    glfw.KEY_S: False,
    glfw.KEY_A: False,
    glfw.KEY_D: False,
    glfw.KEY_SPACE: False,
    glfw.KEY_LEFT_CONTROL: False,
    # Illumination constants
    glfw.KEY_Z: False,
    glfw.KEY_X: False,
    glfw.KEY_C: False,
    glfw.KEY_V: False,
    glfw.KEY_B: False,
    glfw.KEY_N: False,
    # on/off illumination
    glfw.KEY_M: False,
    glfw.KEY_1: False,
    glfw.KEY_2: False,
    glfw.KEY_3: False,
    glfw.KEY_4: False,
    glfw.KEY_5: False,
}

class KeyManager:
    def __init__(self, window, renderer, view, debug=False):
        self.window = window
        self.renderer = renderer
        self.key_map = {}
        
        # For actions that repeat while the key is held down
        self.global_key_map_continuous = {}
        # For single-tap actions 
        self.global_key_map_toggle = {}
        
        self.view = view
        self.debug = debug
        
        # Set to control 'toggle' keys that have already been processed on PRESS
        self.processed_toggle_keys = set() 
        
        glfw.set_key_callback(window.glfw_window, self.key_event)

    def set_key(self, key, action, models):
        if not isinstance(models, list):
            models = [models]
        self.key_map[key] = (action, models)
    
    def set_global_key_continuous(self, key, action):
        self.global_key_map_continuous[key] = action
    
    def set_global_key_toggle(self, key, action):
        self.global_key_map_toggle[key] = action

    def key_event(self, w, key, scancode, action, mods):
        if key in key_state:
            if action == glfw.PRESS:
                key_state[key] = True
            elif action == glfw.RELEASE:
                key_state[key] = False
                # If the key was released, remove it from the set of processed 'toggle' keys
                if key in self.processed_toggle_keys:
                    self.processed_toggle_keys.remove(key)

        if action == glfw.PRESS:
            if key in self.global_key_map_toggle and key not in self.processed_toggle_keys:
                self.global_key_map_toggle[key]()
                self.processed_toggle_keys.add(key)


        if key == glfw.KEY_ESCAPE and (action == glfw.PRESS or action == glfw.REPEAT):
            self.window.close()
        if key == glfw.KEY_P and (action == glfw.PRESS or action == glfw.REPEAT):
            self.renderer.setPolygonMode()

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
        
    
        for k, action_func in self.global_key_map_continuous.items():
            if k in key_state and key_state[k]:
                action_func() # Call the global continuous function

        for k, (action_func, models) in self.key_map.items():
            if k in key_state and key_state[k]:
                for m in models:
                    action_func(m)
                    # if self.debug: print(f"{m.type}: X: {m.modelConfig['t_x']}, Y:{m.modelConfig['t_y']}, Z:{m.modelConfig['t_z']}")