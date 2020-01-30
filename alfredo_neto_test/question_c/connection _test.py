import socket
from time import sleep
HOST = socket.gethostbyname(socket.gethostname())
HOST = '192.168.27.253'
PORT = 5000

while 1:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        while 1:
            data = s.recv(1024)
            print('Received', repr(data))
    except ConnectionResetError as err:
        print(f"Server Desconectado")
    except ConnectionRefusedError as err:
        print("Trying to reconnect!")
        sleep(1)
    except OSError as err:
        print(err)
