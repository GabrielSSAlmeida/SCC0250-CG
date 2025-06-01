from models.texture import Texture
from OpenGL.GL import *


class FileManager:
    vertices_list = []  # Agora é um atributo estático
    textures_coord_list = []  # Agora é um atributo estático
    normals_list = []

    @staticmethod
    @staticmethod
    def load_model_from_file(filename):
        """Loads a Wavefront OBJ file, including normals."""
        vertices = []
        texture_coords = []
        normals = []
        faces = []

        material = None

        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue

            if values[0] == 'v':
                vertices.append(values[1:4])
            elif values[0] == 'vt':
                texture_coords.append(values[1:3])
            elif values[0] == 'vn':
                normals.append(values[1:4])
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':
                face = []
                face_texture = []
                face_normal = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and w[1]:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)
                    if len(w) == 3 and w[2]:
                        face_normal.append(int(w[2]))
                    else:
                        face_normal.append(0)
                faces.append((face, face_texture, face_normal, material)) 

        model = {
            'vertices': vertices,
            'texture': texture_coords,
            'normals': normals,
            'faces': faces
        }
        return model


    @staticmethod
    def circular_sliding_window_of_three(arr):
        if len(arr) == 3:
            return arr
        circular_arr = arr + [arr[0]]
        result = []
        for i in range(len(circular_arr) - 2):
            result.extend(circular_arr[i:i+3])
        return result

    @classmethod
    def load_obj_and_texture(cls, objFile, texturesList=[]):
        modelo = cls.load_model_from_file(objFile)

        verticeInicial = len(cls.vertices_list)
        faces_visited = []

        for face in modelo['faces']:
            face_vertices, face_textures, face_normals, material = face
            if material not in faces_visited:
                faces_visited.append(material)
            for vertice_id in cls.circular_sliding_window_of_three(face_vertices):
                cls.vertices_list.append(modelo['vertices'][vertice_id - 1])
            for texture_id in cls.circular_sliding_window_of_three(face_textures):
                cls.textures_coord_list.append(modelo['texture'][texture_id - 1])
            for normal_id in cls.circular_sliding_window_of_three(face_normals):
                if normal_id != 0:
                    cls.normals_list.append(modelo['normals'][normal_id - 1])
                else:
                    cls.normals_list.append([0.0, 0.0, 0.0])  # caso não tenha normal

        verticeFinal = len(cls.vertices_list)

        texture_ids = []
        for texture_path in texturesList:
            texture_id = Texture.get_next_texture_id()
            Texture.load(texture_id, texture_path)
            texture_ids.append(texture_id)

        return verticeInicial, verticeFinal - verticeInicial, texture_ids[0] if texture_ids else 0

    
    @classmethod
    def load_obj_2D_and_texture(cls, objFile, texturesList=[]):
        modelo = cls.load_model_from_file(objFile)

        verticeInicial = len(cls.vertices_list)
        #print(f'Processando modelo 2D {objFile}. Vértice inicial: {verticeInicial}')
        faces_visited = []

        for face in modelo['faces']:
            if face[2] not in faces_visited:
                faces_visited.append(face[2])

            # Assumindo que as coordenadas estão no plano XY (Z será 0.0)
            for vertice_id in cls.circular_sliding_window_of_three(face[0]):
                vertice = modelo['vertices'][vertice_id - 1]
                vertice_2d = (vertice[0], vertice[1], 0.0)  # Força Z como 0.0
                cls.vertices_list.append(vertice_2d)

            for texture_id in cls.circular_sliding_window_of_three(face[1]):
                cls.textures_coord_list.append(modelo['texture'][texture_id - 1])

        verticeFinal = len(cls.vertices_list)
        #print(f'Processando modelo 2D {objFile}. Vértice final: {verticeFinal}')

        for id in range(len(texturesList)):
            Texture.load(id, texturesList[id])

        return verticeInicial, verticeFinal - verticeInicial
