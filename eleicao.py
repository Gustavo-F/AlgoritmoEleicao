import os
import sys
import json
import time
import socket
import threading
from urllib import response



portas = [5001, 5002, 5003, 5004, 5005, 5006, 5007]
porta_lider = 0

ip = '127.0.0.1'


def envia_mensagem(mensagem, destino):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.connect(destino)
        s.send(mensagem.encode('UTF-8'))
        
        s.close() 
        return True

    except:
        return False


def eleicao(id):
    print('Iniciando eleição...')

    global ip
    global portas
    global porta_lider

    portas_maiores = []
    novo_lider = 0

    for porta in portas:
        if porta != portas[id - 1] and porta != porta_lider:
            resposta = envia_mensagem(
                mensagem=json.dumps({'processo': id, 'eleicao': True}), 
                destino=(ip, porta),
            )  
            if resposta:       
                if porta > portas[id - 1] and porta != porta_lider:
                    portas_maiores.append(porta)

    if len(portas_maiores) == 0:
        print('Sou o novo líder...')
        novo_lider = portas[id - 1]
        porta_lider = novo_lider

        for i in range(id - 1):
            envia_mensagem(
                mensagem=json.dumps({'processo': id, 'eleicao': True, 'novo_lider': novo_lider}),
                destino=(ip, portas[i])
            )

            print(portas[i])
    else:
        for i in range(id - 1, len(portas)):
            pass

    print('\n')
    return novo_lider

def verifica_lider(lider, id):
    global porta_lider
    mensagem = json.dumps({'processo': id})
    
    while True:
        print(f'Líder: {lider}')
        status = envia_mensagem(mensagem, lider)

        if not status:
            novo_lider = eleicao(id)
            if novo_lider == portas[id - 1]:
                break
            else:
                porta_lider = novo_lider
                lider = (ip, porta_lider)

        else:
            print('ON')

        time.sleep(2)

def main():
    global ip
    global porta_lider

    argumentos = sys.argv
    id = int(argumentos[1])
    
    if id < 1 or id > 7:
        print('ID inválido')
        return

    try:
        porta_lider = portas[6]
        porta = portas[id - 1]

        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_socket.bind((ip, porta))
    except:
        print('------------ Erro! ------------')
        print(f'Informe o identificador do processo (1 a 7)\n')

    main_socket.listen()

    if porta != porta_lider:
        thread_verificacao = threading.Thread(target=verifica_lider, args=[(ip, porta_lider), id])
        thread_verificacao.start()

    conexao, endereco = main_socket.accept()
    dados = conexao.recv(1024)

    while True:
        print(f'Cliente Conectado => {endereco[0]}:{endereco[1]}')

        if dados:
            mensagem = dados.decode('UTF-8')
            mensagem = json.loads(mensagem)

            print(mensagem)
            
            dados = None
        else:
            print('erro dados')
            conexao, endereco = main_socket.accept()
            dados = conexao.recv(1024)



if __name__ == '__main__':
    main()
