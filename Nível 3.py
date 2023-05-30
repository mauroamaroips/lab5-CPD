from PIL import Image, ImageFilter, ImageEnhance
import os
from timeit import default_timer as timer


def cinzentos(imagem):
    enh = ImageEnhance.Color(imagem)
    imagem = enh.enhance(0.0)
    return imagem


def contraste(imagem):
    enh = ImageEnhance.Contrast(imagem)
    imagem = enh.enhance(1.8)
    return imagem


def arestas(imagem):
    imagem = imagem.filter(ImageFilter.FIND_EDGES)
    return imagem


def desfocagem(imagem):
    imagem = imagem.filter(ImageFilter.BLUR)
    return imagem


if __name__ == '__main__':
    inicio = timer()
    diretoria = "./imagens"  # As imagens devem estar na pasta imagens
    for file in os.listdir(diretoria):
        im = Image.open(diretoria + "/" + str(file))
        im.show()
        im = cinzentos(im)
        im = contraste(im)
        im.show("B&W e mais contraste")
    fim = timer()
    print(f"Tempo para tratamento sequencial: {fim - inicio:.8f}")
