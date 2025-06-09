from math import sqrt
from models.model_3D import Model_3D
import glm

def world_rotation(model):
    config = model.modelConfig
    # Wordl rotate
    if config['type'] == "globo":
        model.rotate(0.002, 0, 1, 0)

def create_n_models(base_vertices, num_vertices, texture_id, positions, CONF):
    models = []
    for pos in positions:
        config = CONF.copy()
        config["t_x"] = pos[0]
        config["t_z"] = pos[1]
        models.append(Model_3D(base_vertices, num_vertices, config, texture_id))
    return models


def make_scaler(direction, scale_factor, delta_y, min_scale=1.0, max_scale=2.5):
    def scaler(model):
        s = model.modelConfig.get("s_x", 1.0)
        if direction == "up" and s < max_scale:
            model.scale(scale_factor, scale_factor, scale_factor)
            model.translate(0, delta_y, 0)
        elif direction == "down" and s > min_scale:
            model.scale(1/scale_factor, 1/scale_factor, 1/scale_factor)
            model.translate(0, -delta_y, 0)
    return scaler




def limit_camera_position(cam_pos, sphere_center=(0, -10, 0), max_radius=48.0, min_y=-1.5, padding=0.0):
    x, y, z = cam_pos
    cx, cy, cz = sphere_center

    # Prevent the camera from going below the ground (Y axis)
    y = max(y, min_y)

    # Compute the vector from the sphere center to the camera
    dx = x - cx
    dy = y - cy
    dz = z - cz

    # Compute the distance from the camera to the center of the sphere (skybox)
    distance = sqrt(dx**2 + dy**2 + dz**2) + padding

    # If the distance exceeds the allowed radius, push the camera back to the sphere's surface
    if distance > max_radius:
        scale = max_radius / distance
        x = cx + dx * scale
        y = cy + dy * scale
        z = cz + dz * scale

    return x, y, z


def nimbus_translation(model, dx=0, dy=0, dz=0, angle_x=None, angle_y=None, angle_z=None):
    config = model.modelConfig

    config.setdefault('t_x', 0.0)
    config.setdefault('t_y', 0.0)
    config.setdefault('t_z', 0.0)

    config['angle_x'] = 0.0
    config['angle_y'] = 0.0
    config['angle_z'] = 0.0

    config['t_x'] += dx
    config['t_y'] += dy
    config['t_z'] += dz

    config['t_x'], config['t_y'], config['t_z'] = limit_camera_position((config['t_x'], config['t_y'], config['t_z']), min_y=2.5, padding=4.0)
        
    if angle_x is not None:
        config['angle_x'] = angle_x
    if angle_y is not None:
        config['angle_y'] = angle_y
    if angle_z is not None:
        config['angle_z'] = angle_z


# Ilumination functions
def adjust_light_up(k: dict, name: str, increment: float = 0.1):
    current_value = k.get(name, 0.0)
    current_value += increment
    if current_value >= 10.0:
        current_value = 10.0
    k[name] = current_value
    print(f"{name.upper()}: {current_value:.2f}")

def adjust_light_down(k: dict, name: str, decrement: float = 0.1):
    current_value = k.get(name, 0.0)
    current_value -= decrement
    if current_value <= 0.0:
        current_value = 0.0
    k[name] = current_value
    print(f"{name.upper()}: {current_value:.2f}")



def toggle_moving_light_to_destination(external_lights_data, light_move_pos1, light_move_pos2, ilumination, current_light_state_ref):
    current_external_light_visual_pos = external_lights_data[0]["position"]
    tolerance = 0.5 
    
    if current_light_state_ref[0] == 0: 
        if glm.distance(current_external_light_visual_pos, light_move_pos1) < tolerance:
            current_light_state_ref[0] = 2 # Mover para pos2
        elif glm.distance(current_external_light_visual_pos, light_move_pos2) < tolerance:
            current_light_state_ref[0] = 1 # Mover para pos1
        else:
            current_light_state_ref[0] = 1
    else:
        current_light_state_ref[0] = 0
    

def make_toggle_external_light(idx, external_lights_data, ilumination):
    def toggle(_=None):
        external_lights_data[idx]["isOn"] = not external_lights_data[idx]["isOn"]
        ilumination.update_external_light_is_on(idx, external_lights_data[idx]["isOn"])
    return toggle

def toggle_dir_light(dir_light_data, ilumination):
    dir_light_data["isOn"] = not dir_light_data["isOn"]
    ilumination.update_dir_light_is_on(dir_light_data["isOn"])

def toggle_wand_lights(internal_lights_data, internal_spotlight_data, ilumination):
    current_state_point = internal_lights_data[1]["isOn"]
    current_state_spot = internal_spotlight_data[1]["isOn"]
    
    new_state = not (current_state_point or current_state_spot) 

    internal_lights_data[1]["isOn"] = new_state
    ilumination.update_internal_light_is_on(1, new_state)
    
    internal_spotlight_data[1]["isOn"] = new_state
    ilumination.update_internal_spotlight_is_on(1, new_state)

def toggle_goblet_lights(internal_lights_data, internal_spotlight_data, ilumination):
    current_state_point = internal_lights_data[0]["isOn"]
    current_state_spot = internal_spotlight_data[0]["isOn"]
    
    new_state = not (current_state_point or current_state_spot)

    internal_lights_data[0]["isOn"] = new_state
    ilumination.update_internal_light_is_on(0, new_state)
    
    internal_spotlight_data[0]["isOn"] = new_state
    ilumination.update_internal_spotlight_is_on(0, new_state)