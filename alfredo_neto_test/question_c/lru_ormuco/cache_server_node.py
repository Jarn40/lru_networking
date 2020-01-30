import socket
from functools import cached_property
import time
from threading import Thread

# hostname = socket.gethostname()
# Ipv4 = socket.gethostbyname(hostname)

# print(f'{hostname} : {Ipv4}')


class CacheServerNode():
    '''Node of a big network infraestructure'''

    def __init__(self, port=5000):
        self.port = port
        self.subscribers = {}
        self.networkNodes = []
        self.serverNodeThread = Thread(target=self.serverNode, name="Server Network Listener")
        self.serverNodeThread.setDaemon(True)
        self.serverNodeThread.start()
        print("Criado!")

    @cached_property
    def host(self):
        '''finds the ip address of the machine'''
        return '192.168.27.253'
        return socket.gethostbyname(socket.gethostname())

    @cached_property
    def server(self):
        return socket.create_server((self.host, self.port))

    def serverNode(self):
        while 1:
            self.server.listen(1)
            conn, addr = self.server.accept()
            conn.send('Connectado'.encode())
            self.subscribers[addr[0]] = conn
            print(f"Novo server Conectado: {addr[0]}")

    def sendData(self, data='Teste'):
        print(self.subscribers.keys())
        remove = []
        for conn in self.subscribers:
            try:
                self.subscribers[conn].send(data.encode())
            except ConnectionAbortedError as err:
                print(f'{conn} EROR => {err}')
                remove.append(conn)
                # del self.subscribers[conn]
        for conn in remove:
            del self.subscribers[conn]

        del remove

    def contactingNode(self, HOST, PORT):
        while 1:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((HOST, PORT))
                while 1:
                    data = s.recv(1024)
                    print('Received', repr(data))
            except ConnectionResetError as err:
                print(f"Server Desconectado")
            except ConnectionRefusedError as err:
                print("Trying to reconnect!")
                time.sleep(5)
            except OSError as err:
                print(err)

    def networkLink(self):
        for link in self.networkNodes:
            if link not in self.subscribers.keys():
                Thread(target=self.contactingNode, name="Server Network Listener", args=[link, 5000])


if __name__ == "__main__":
    node = CacheServerNode()
    print("OK1")
    timer = time.time()
    while 1:
        if time.time() - timer > 5:
            print("OK")
            node.sendData()
            timer = time.time()
