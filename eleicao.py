import sys
import time
import socket
from threading import Thread

portas = [5551, 5552, 5553, 5554, 5555, 5556, 5557]
eleito = None

def main():
    argumentos = sys.argv
    
    id_processo = argumentos[1]
    porta = portas[int(id_processo)-1]

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind(('127.0.0.1', porta))

    print(f'\nPort => {porta}; Process ID => {id_processo}\n')

if __name__ == '__main__':
    main()
