from window import Window
from models.model import Model
from models.renderer import Renderer
from utils.file_loader import load_model_from_file

def main():
    window = Window()
    renderer = Renderer(window)

    # Carregar modelo
    model_data = load_model_from_file("objects/Harry.obj")
    vertices = model_data["vertices"]
    faces = model_data["faces"]

    # Criar objeto Model
    harry = Model(vertices, len(faces))
    renderer.add_model(harry)

    # Exibir janela
    window.show()

    while not window.should_close():
        renderer.render()

    window.terminate()

if __name__ == "__main__":
    main()
