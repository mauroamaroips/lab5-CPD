from threading import Thread
from PIL import Image, ImageEnhance
import os
import queue

from timeit import default_timer as timer


def aplicar_efeito(imagem, efeito):
    if efeito == 'cinzentos':
        enh = ImageEnhance.Color(imagem)
        imagem = enh.enhance(0.0)
    elif efeito == 'contraste':
        enh = ImageEnhance.Contrast(imagem)
        imagem = enh.enhance(1.8)
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
    queue_inicial = queue.Queue()
    queue_w1_w2 = queue.Queue()
    queue_final = queue.Queue()
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
    trabalhador_1 = Thread(target=trabalhador, args=('cinzentos', queue_inicial, queue_w1_w2))
    trabalhador_1.start()
    trabalhador_2 = Thread(target=trabalhador, args=('contraste', queue_w1_w2, queue_final))
    trabalhador_2.start()
    trabalhador_2.join()
    while not queue_final.empty():
        imagem = queue_final.get()
        if imagem:
            imagem.show()
    fim = timer()
    print(f"Tempo para pipelining: {fim - inicio:.8f}")


# Nível 2
# Pergunta 1 - Explique como é utilizado o pipelining no código apresentado realçando o papel de cada uma
# das queues utilizadas.

# Resposta - Neste programa em específico são criadas 3 queues (queue_inicial, queue_w1_w2 e queue_final).
# A queue_inicial recebe todas as imagens presentes na pasta "./imagens", sem processamento. É também adicionado
# um sinalizador de terminação à queue para os trabalhadores saberem quando não há mais imagens a serem processadas.
# O trabalhador 1 irá processar as imagens da queue_inicial com o efeito "cizentos" e colocá-las na queue_w1_w2.
# O trabalhador 2 é responsável por aplicar o efeito de 'contraste' nas imagens da queue_w1_w2 e adicioná-las à
# queue_final.
#
# Após iniciar os trabalhadores, o programa espera até que
# todos os trabalhos sejam concluídos usando trabalhador_2.join().

# Por fim, o programa itera sobre a queue_final, mostrando as imagens resultaantes com os efeitos aplicados, em sequência.
# O tempo total de execução do pipeline é medido com a biblioteca timeit e é exibido como saída do programa