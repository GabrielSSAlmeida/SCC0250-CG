
from config import TREE
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