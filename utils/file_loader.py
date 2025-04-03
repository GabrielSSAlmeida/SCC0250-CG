from models.texture import Texture
from OpenGL.GL import *
from PIL import Image
import numpy as np

class FileManager:
    vertices_list = []  # Agora é um atributo estático
    textures_coord_list = []  # Agora é um atributo estático

    @staticmethod
    def load_model_from_file(filename):
        """Loads a Wavefront OBJ file."""
        objects = {}
        vertices = []
        texture_coords = []
        faces = []

        material = None

        # Abre o arquivo OBJ para leitura
        for line in open(filename, "r"):  # Para cada linha do arquivo .obj
            if line.startswith("#"):
                continue  # Ignora comentários
            values = line.split()  # Quebra a linha por espaço
            if not values:
                continue

            # Recuperando vértices
            if values[0] == "v":
                vertices.append(values[1:4])

            # Recuperando coordenadas de textura
            elif values[0] == "vt":
                texture_coords.append(values[1:3])

            # Recuperando faces
            elif values[0] in ("usemtl", "usemat"):
                material = values[1]
            elif values[0] == "f":
                face = []
                face_texture = []
                for v in values[1:]:
                    w = v.split("/")
                    face.append(int(w[0]))
                    if len(w) >= 2 and w[1]:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, material))

        model = {
            "vertices": vertices,
            "texture": texture_coords,
            "faces": faces,
        }
        return model

    @staticmethod
    def load_texture_from_file(texture_id, img_textura):
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        img = Image.open(img_textura)
        img_width, img_height = img.size
        image_data = img.tobytes("raw", "RGB", 0, -1)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    @staticmethod
    def circular_sliding_window_of_three(arr):
        """Gera triângulos a partir dos vértices de uma face"""
        if len(arr) == 3:
            return arr
        circular_arr = arr + [arr[0]]
        result = []
        for i in range(len(circular_arr) - 2):
            result.extend(circular_arr[i : i + 3])
        return result

    @classmethod
    def load_obj_and_texture(cls, objFile, texturesList):
        modelo = cls.load_model_from_file(objFile)

        # Inserindo vértices do modelo no vetor de vértices
        verticeInicial = len(cls.vertices_list)
        print(f"Processando modelo {objFile}. Vértice inicial: {len(cls.vertices_list)}")

        faces_visited = []
        for face in modelo["faces"]:
            if face[2] not in faces_visited:
                faces_visited.append(face[2])
            for vertice_id in cls.circular_sliding_window_of_three(face[0]):
                cls.vertices_list.append(modelo["vertices"][vertice_id - 1])

        verticeFinal = len(cls.vertices_list)
        print(f"Processando modelo {objFile}. Vértice final: {len(cls.vertices_list)}")

        # Carregando textura equivalente e definindo um id (buffer)
        for id in range(len(texturesList)):
            Texture.load(id, texturesList[id])

        return verticeInicial, verticeFinal - verticeInicial
