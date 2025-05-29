import glfw
import glm

class MouseManager:
    def __init__(self, window, view, projection):
        self.window = window
        self.view = view
        self.projection = projection
        self.firstMouse = True
        self.yaw   = -90.0	# yaw is initialized to -90.0 degrees since a yaw of 0.0 results in a direction vector pointing to the right so we initially rotate a bit to the left.
        self.pitch =  0.0
        self.lastX =  window.largura / 2.0
        self.lastY =  window.altura / 2.0


        glfw.set_framebuffer_size_callback(self.window.glfw_window, self.framebuffer_size_callback)
        glfw.set_cursor_pos_callback(self.window.glfw_window, self.mouse_callback)
        glfw.set_scroll_callback(self.window.glfw_window, self.scroll_callback)

        # tell GLFW to capture our mouse
        glfw.set_input_mode(self.window.glfw_window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    
    def framebuffer_size_callback(self, window, largura, altura):

        # make sure the viewport matches the new window dimensions note that width and 
        # height will be significantly larger than specified on retina displays.
        glViewport(0, 0, largura, altura)

    # glfw: whenever the mouse moves, this callback is called
    # -------------------------------------------------------
    def mouse_callback(self, window, xpos, ypos):
    
        if (self.firstMouse):

            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos # reversed since y-coordinates go from bottom to top
        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 0.1 # change this value to your liking
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        # make sure that when self.pitch is out of bounds, screen doesn't get flipped
        if (self.pitch > 89.0):
            self.pitch = 89.0
        if (self.pitch < -89.0):
            self.pitch = -89.0

        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.view.cameraFront = glm.normalize(front)

    # glfw: whenever the mouse scroll wheel scrolls, this callback is called
    # ----------------------------------------------------------------------
    def scroll_callback(self, window, xoffset, yoffset):

        self.projection.fov -= yoffset
        if (self.projection.fov < 1.0):
            self.projection.fov = 1.0
        if (self.projection.fov > 45.0):
            self.projection.fov = 45.0
