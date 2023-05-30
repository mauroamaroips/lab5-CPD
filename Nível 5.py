from multiprocessing import Process, Manager, Queue
from PIL import Image, ImageEnhance, ImageFilter
import os

from timeit import default_timer as timer

def aplicar_efeito(imagem, efeito):
    if efeito == 'cinzentos':
        enh = ImageEnhance.Color(imagem)
        imagem = enh.enhance(0.0)
    elif efeito == 'contraste':
        enh = ImageEnhance.Contrast(imagem)
        imagem = enh.enhance(1.8)
    elif efeito == 'arestas':
        imagem = imagem.filter(ImageFilter.FIND_EDGES)
    elif efeito == 'desfocagem':
        imagem = imagem.filter(ImageFilter.BLUR)
    # imagem.show()
    return imagem


def trabalhador(tarefa, input_queue, output_queue):
    while True:
        imagem = input_queue.get()
        if imagem is None:
            output_queue.put(None)
            return
        imagem = aplicar_efeito(imagem, tarefa)
        output_queue.put(imagem)

if __name__ == '__main__':
    diretoria = "./imagens"
    inicio = timer()
    queue_inicial = Queue()
    queue_w1_w2 = Queue()
    queue_final = Manager().Queue()
    # num_trabalhos = len(os.listdir(diretoria))
    # colocar imagens na queue inicial
    for file in os.listdir(diretoria):
        # Read image
        imagem = Image.open(diretoria + "/" + str(file))
        # Display image
        imagem.show()
        queue_inicial.put(imagem)
    # colocar o terminador na fila de trabalhos
    queue_inicial.put(None)
    trabalhador_1 = Process(target=trabalhador, args=('cinzentos', queue_inicial, queue_w1_w2))
    trabalhador_1.start()
    trabalhador_2 = Process(target=trabalhador, args=('contraste', queue_w1_w2, queue_final))
    trabalhador_2.start()
    trabalhador_2.join()
    while not queue_final.empty():
        imagem = queue_final.get()
        if imagem:
            imagem.show()
    fim = timer()
    print(f"Tempo para pipelining: {fim - inicio:.8f}")