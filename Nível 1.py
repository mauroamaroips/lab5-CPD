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


# Nível 1
# Pergunta 1 - Explique o que faz o programa.

# Resposta - Este programa utiliza a biblioteca PIL (Python Imaging Library) para aplicar dois tipos
# de tratamento em imagens presentes numa determinada pasta, neste caso a pasta ",/imagens".

# O primeiro tratamento é a conversão da imagem para preto e branco, realizado pela função "cinzentos".
# O segundo tratamento é o aumento do contraste, realizado pela função "contraste".
#
# Após aplicar esses dois tratamentos, a imagem resultante é exibida com o título "B&W e mais contraste".
# O programa também exibe o tempo total gasto para realizar o tratamento em todas as imagens presentes na pasta,
# através dos tempos guardados nas variáveis 'inicio' e 'fim', tendo o tempo como 'fim' - 'inicio'.
# O programa é executado em modo sequencial, ou seja, cada imagem é tratada uma após a outra.
