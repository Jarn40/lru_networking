import socket
import pickle
from functools import cached_property
import time
import sys
from threading import Thread

# hostname = socket.gethostname()
# Ipv4 = socket.gethostbyname(hostname)

# print(f'{hostname} : {Ipv4}')

FIXED_MSG_SIZE = 1024


class CacheServerNode():
    '''Node of a big network infraestructure'''

    def __init__(self, port=5000, join=None):
        self.port = port
        self.subscribers = {}
        self.connectionThread = {}
        self.networkNodes = []
        if join:
            self.joinNetwork(join)
        else:
            self.startNetwork()

    @cached_property
    def host(self):
        '''finds the ip address of machine'''
        # return '192.168.27.253'
        return socket.gethostbyname(socket.gethostname())

    @cached_property
    def server(self):
        return socket.create_server((self.host, self.port))

    def serverNode(self):
        '''create a local node for listen start point of new nodes'''
        while 1:
            self.server.listen(1)
            conn, addr = self.server.accept()
            command = {
                'type': 'getHost',
                'host': self.host
            }
            conn.send(pickle.dumps(command))
            actual_host = conn.recv(FIXED_MSG_SIZE)
            actual_host = actual_host.decode()

            self.subscribers[actual_host] = conn
            self.networkNodes.append(actual_host)
            command = {
                'type': 'updateNodeList',
                'data': self.networkNodes,
                'host': self.host
            }

            self.syncData(command)
            print(f"New server Conected: {actual_host}")
            self.connectionThread[actual_host] = Thread(target=self.listenConectedServer, name=actual_host, args=[actual_host, self.subscribers[actual_host]])
            self.connectionThread[actual_host].setDaemon(True)
            self.connectionThread[actual_host].start()
            print(self.networkNodes)

    def listenConectedServer(self, addr, conn):
        while 1:
            try:
                data = []
                while 1:
                    packet = conn.recv(FIXED_MSG_SIZE)
                    data.append(packet)
                    if int(sys.getsizeof(packet)) < FIXED_MSG_SIZE:
                        break
                if packet == b'':
                    break
                command = pickle.loads(b"".join(data))
                # THis part is to update LRU
                self.command_dispatcher(command)
                print(f'Command Received from {addr}:\n{command}')

            except ConnectionResetError as err:
                print(f"{addr} => Disconnected!")
            except OSError as err:
                print(err)
                break

    def contactingNode(self, HOST, PORT=5000):
        '''stay in contact with each existing node in network'''
        while 1:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((HOST, PORT))
                self.subscribers[HOST] = sock
                print(f"Add by contacting +{HOST}")
                while 1:
                    data = []
                    while 1:
                        packet = sock.recv(FIXED_MSG_SIZE)
                        data.append(packet)
                        if int(sys.getsizeof(packet)) < FIXED_MSG_SIZE:
                            break
                    if packet == b'':
                        break
                    command = pickle.loads(b"".join(data))
                    # This part is to update LRU
                    self.command_dispatcher(command)
                    print(f'Command Received from {HOST}:\n{command}')

            except ConnectionResetError as err:
                print(f"{HOST} => Disconnected!")
            except ConnectionRefusedError as err:
                print(f"Trying reconnection to {HOST}!")
                time.sleep(5)
            except OSError as err:
                print(f'[ERROR] {err}')
                break

    def connectToNetwork(self):
        '''method that creates all connection threads'''
        for link in self.networkNodes:
            print(link)
            if link not in self.subscribers.keys() and link is not self.host and link not in self.connectionThread.keys():
                print("CRIANDO THREAD")
                self.connectionThread[link] = Thread(target=self.contactingNode, name=link, args=[link, 5000])
                self.connectionThread[link].setDaemon(True)
                self.connectionThread[link].start()
                print(f"{link} Conected")

    def syncData(self, data={}):
        '''Method to syncronize data across all nodes'''
        remove = []
        for conn in self.subscribers:
            try:
                self.subscribers[conn].send(pickle.dumps(data))
            except ConnectionAbortedError as err:
                print(f'{conn} EROR => {err}')
                remove.append(conn)
            except Exception as err:
                print(err)
        for conn in remove:
            del self.subscribers[conn]

        del remove

    # Commands

    def command_dispatcher(self, command):

        if type(command) is not dict or 'type' not in command.keys():
            print("Impossible to complete command")
            return

        if command['type'] == 'updateNodeList':
            print('updating node')
            for ipv4 in command['data']:
                if ipv4 not in self.networkNodes and ipv4 != self.host:
                    print(f"Adding by update + {ipv4}")
                    self.networkNodes.append(ipv4)
            self.connectToNetwork()

        elif command['type'] == 'getHost':
            print(f"HOST ==>{self.host}")
            self.subscribers[command['host']].send(self.host.encode())

        elif command['type'] == 'setKey':
            for key in command['data']:
                # TODO write on LRU
                self.syncData(command)
                pass
        elif command['type'] == 'getCache':
            # TODO get from LRU
            self.syncData(command)
        elif command['type'] == 'getKey':
            for key in command['data']:
                # TODO get specific key from LRU
                self.syncData(command)

    # CONTROLER

    def startNetwork(self):
        '''Start a new network'''
        self.serverNodeThread = Thread(target=self.serverNode, name="Server Network Listener")
        self.serverNodeThread.setDaemon(True)
        self.serverNodeThread.start()
        print("Network Started!")

    def joinNetwork(self, nodeIP):
        '''Connect to an existing network'''
        print(f"Joining Network of Node {nodeIP}")
        self.networkNodes.append(nodeIP)
        self.connectToNetwork()
        self.startNetwork()

    def stop(self):
        '''stop all sockets and threads'''
        [conn.close() for conn in self.subscribers.values()]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        node = CacheServerNode(join=sys.argv[1])
    else:
        node = CacheServerNode()
    while 1:
        try:
            pass
        except KeyboardInterrupt:
            node.stop()
            print("Exiting Network")
            break

    # print("OK1")
    # timer = time.time()
    # while 1:
    #     if time.time() - timer > 5:
    #         print("OK")
    #         node.sendData()
    #         timer = time.time()

    # import cache_server_node as csn
    # node = csn.CacheServerNode(join='192.168.27.254')
