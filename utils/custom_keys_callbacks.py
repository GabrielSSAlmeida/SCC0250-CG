

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


    if angle_x is not None:
        config['angle_x'] = angle_x
    if angle_y is not None:
        config['angle_y'] = angle_y
    if angle_z is not None:
        config['angle_z'] = angle_z
        