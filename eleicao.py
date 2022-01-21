import sys
import json
import time
import socket
from threading import Thread

portas = [5551, 5552, 5553, 5554, 5555, 5556, 5557]
eleito = portas[6]

def iniciar_eleicao(id_processo):
    print('Iniciando eleição...')

    socket_eleicao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_eleicao.bind(('127.0.0.1', portas[id_processo - 1] + 20))

    resposta_superior = False

    for i in range(id_processo, len(portas)):
        porta_destino = portas[i]

        if porta_destino != eleito:
            destino = ('127.0.0.1', porta_destino)
            mensagem = json.dumps({'eleicao': True})

            try:
                socket_eleicao.connect(destino)
                socket_eleicao.send(mensagem.encode('UTF-8'))

                resposta, servidor = socket_eleicao.recvfrom(1024)
                print(f'\nResposta Eleição => {resposta}\n')
            except:
                pass



def emissor(id_processo):
    loop_emissor = True

    socket_emissor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    socket_emissor.bind(('127.0.0.1', portas[id_processo - 1] + 10))
    socket_emissor.settimeout(2)

    while loop_emissor:
        mensagem = json.dumps({'processo': id_processo})
        destino = ('127.0.0.1', eleito)

        try:
            socket_emissor.connect(destino)
            socket_emissor.send(mensagem.encode('UTF-8'))

            resposta, servidor = socket_emissor.recvfrom(1024)
            print(f'Resposta: {resposta.decode("UTF-8")}')
        except ConnectionResetError as e:
            pass
        except ConnectionRefusedError as error:
            iniciar_eleicao(id_processo) 
        except socket.timeout:
            iniciar_eleicao(id_processo)
        
        time.sleep(2)

def receptor(server_socket, id_processo):
    while True:
        server_socket.listen()

        s, addr = server_socket.accept()
        print(f'\nCliente Conectado => {addr[0]}:{addr[1]}')

        resposta = json.dumps({'status': 'ok'})
        s.send(resposta.encode('UTF-8'))
        s.close()


def main():
    argumentos = sys.argv
    
    try:
        id_processo = int(argumentos[1])
        porta = portas[id_processo - 1]
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server_socket.bind(('127.0.0.1', porta))

        thread_receptor = Thread(target=receptor, args=[server_socket, id_processo])
        thread_receptor.start()
        
        if porta != eleito:
            thread_emissor = Thread(target=emissor, args=[id_processo])
            thread_emissor.start()

    except:
        print('------------ Erro! ------------')
        print(f'Informe o identificador do processo (1 a 7)\n')

if __name__ == '__main__':
    main()
