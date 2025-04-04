from window import Window
from models.model import Model
from models.renderer import Renderer
from utils.file_loader import FileManager
from OpenGL.GL import *

def main():
    window = Window()
    renderer = Renderer(window)

    # Carregar modelo
    verticeInicial_harry, quantosVertices_harry = FileManager.load_obj_and_texture('objects/Harry.obj', [])

    # Criar objeto Model
    harry = Model(verticeInicial_harry, quantosVertices_harry)
    renderer.add_model(harry)


    # Exibir janela
    window.upload_data()
    window.show()
    window.enable()
    while not window.should_close():
        renderer.render()

    window.terminate()

if __name__ == "__main__":
    main()
