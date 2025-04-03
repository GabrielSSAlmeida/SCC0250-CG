def load_model_from_file(filename):
    vertices = []
    faces = []

    for line in open(filename, "r"):
        values = line.split()
        if not values: continue

        if values[0] == 'v':
            vertices.append(list(map(float, values[1:4])))
        elif values[0] == 'f':
            face = [int(v.split('/')[0]) for v in values[1:]]
            faces.append(face)

    return {"vertices": vertices, "faces": faces}
