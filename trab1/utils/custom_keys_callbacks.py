dy_state = {"dy": 0.01}

def harry_crazy_chapeu(model):
    config = model.modelConfig
    # Harry just rotate
    # Chapeu goes up and down 
    if config['type'] == "harry":
        model.rotate(5, 0, 1, 0)
    elif config['type'] == "chapeu":
        if "upper_lim" in config:
            if config["t_y"] > config["upper_lim"] or config["t_y"] < config["lower_lim"]:
                dy_state["dy"] *= -1
                
        config["t_y"] = config.get("t_y", 0) + dy_state["dy"]     


def nimbus_t_and_r(model, dx=0, dy=0, angle_x=None, angle_y=None, angle_z=None):
    config = model.modelConfig

    config.setdefault('t_x', 0.0)
    config.setdefault('t_y', 0.0)
    config.setdefault('t_z', 0.0)
    config.setdefault('angle_x', 0.0)
    config.setdefault('angle_y', 0.0)
    config.setdefault('angle_z', 0.0)


    config['t_x'] += dx
    config['t_y'] += dy

    # preserves rotation
    if config["t_y"] > config["upper_lim"]:
        config["t_y"] = config["upper_lim"]

    if angle_x is not None:
        config['angle_x'] = angle_x
    if angle_y is not None:
        config['angle_y'] = angle_y
    if angle_z is not None:
        config['angle_z'] = angle_z