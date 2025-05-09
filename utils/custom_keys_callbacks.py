from math import sqrt
from models.model_3D import Model_3D

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




def limit_camera_position(cam_pos, sphere_center=(0, -10, 0), max_radius=48.0, min_y=-1.5):
    x, y, z = cam_pos
    cx, cy, cz = sphere_center

    # Prevent the camera from going below the ground (Y axis)
    y = max(y, min_y)

    # Compute the vector from the sphere center to the camera
    dx = x - cx
    dy = y - cy
    dz = z - cz

    # Compute the distance from the camera to the center of the sphere (skybox)
    distance = sqrt(dx**2 + dy**2 + dz**2)

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

    if config["t_y"] > config.get("upper_lim", float('inf')):
        config["t_y"] = config["upper_lim"]
        
    if angle_x is not None:
        config['angle_x'] = angle_x
    if angle_y is not None:
        config['angle_y'] = angle_y
    if angle_z is not None:
        config['angle_z'] = angle_z