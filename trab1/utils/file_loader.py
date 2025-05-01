from models.texture import Texture
from OpenGL.GL import *


class FileManager:
    vertices_list = []  # Agora é um atributo estático
    textures_coord_list = []  # Agora é um atributo estático

    @staticmethod
    def load_model_from_file(filename):
        """Loads a Wavefront OBJ file. """
        vertices = []
        texture_coords = []
        faces = []

        material = None

        # abre o arquivo obj para leitura
        for line in open(filename, "r"): ## para cada linha do arquivo .obj
            if line.startswith('#'): continue ## ignora comentarios
            values = line.split() # quebra a linha por espaço
            if not values: continue

            ### recuperando vertices
            if values[0] == 'v':
                vertices.append(values[1:4])

            ### recuperando coordenadas de textura
            elif values[0] == 'vt':
                texture_coords.append(values[1:3])

            ### recuperando faces 
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':
                face = []
                face_texture = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, material))

        model = {}
        model['vertices'] = vertices
        model['texture'] = texture_coords
        model['faces'] = faces

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
    
        ### inserindo vertices do modelo no vetor de vertices
        verticeInicial = len(cls.vertices_list)
        print('Processando modelo {}. Vertice inicial: {}'.format(objFile, len(cls.vertices_list)))
        faces_visited = []
        for face in modelo['faces']:
            if face[2] not in faces_visited:
                faces_visited.append(face[2])
            for vertice_id in cls.circular_sliding_window_of_three(face[0]):
                cls.vertices_list.append(modelo['vertices'][vertice_id - 1])
            for texture_id in cls.circular_sliding_window_of_three(face[1]):
                cls.textures_coord_list.append(modelo['texture'][texture_id - 1])
            
        verticeFinal = len(cls.vertices_list)
        print('Processando modelo {}. Vertice final: {}'.format(objFile, len(cls.vertices_list)))
        
        ### carregando textura equivalente e definindo um id (buffer): use um id por textura!
        for id in range(len(texturesList)):
            Texture.load(id,texturesList[id])
        
        return verticeInicial, verticeFinal - verticeInicial
    
    @classmethod
    def load_obj_2D_and_texture(cls, objFile, texturesList=[]):
        modelo = cls.load_model_from_file(objFile)

        verticeInicial = len(cls.vertices_list)
        print(f'Processando modelo 2D {objFile}. Vértice inicial: {verticeInicial}')
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
        print(f'Processando modelo 2D {objFile}. Vértice final: {verticeFinal}')

        for id in range(len(texturesList)):
            Texture.load(id, texturesList[id])

        return verticeInicial, verticeFinal - verticeInicial
