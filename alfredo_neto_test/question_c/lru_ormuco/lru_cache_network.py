'''Module responsable for creating and sync a lru_cache network'''
import socket
import pickle
import time
import sys
from threading import Thread
import lru_cache

FIXED_MSG_SIZE = 1024
CON_RETRY = 5


class CacheNetwork():
    '''Node of a big network infraestructure
        Public Methods:
            get_key(key) -> get key on cache
            set_key(key,value) -> save key,value on cache
            spy() -> get entire cache without touching it
        Public Decorator
            cache_io -> cache I/O of a function/method
    '''

    def __init__(self, port=5000, join=None, max_size=1000, expire_after=60):
        self.port = port
        self.subscribers = {}
        self.connection_thread = {}
        self.network_nodes = []
        self.local_cache = lru_cache.LRUCache(max_size, expire_after)
        self.host = socket.gethostbyname(socket.gethostname())
        self.server = socket.create_server((self.host, self.port))
        if join:
            self.join_network(join)
        else:
            self.start_network()

    def get_host(self):
        '''returns ip address of machine'''
        return self.host

    def local_node(self):
        '''create a local node for listen start point of new nodes'''
        while 1:
            self.server.listen(1)
            conn, _ = self.server.accept()
            ##This part is to allow tunnel networking, avoiding moden's IP
            command = {
                'type': 'getHost',
                'host': self.host
            }
            conn.send(pickle.dumps(command))
            actual_host = conn.recv(FIXED_MSG_SIZE)
            actual_host = actual_host.decode()
            ##-----------------------------------------------------
            self.subscribers[actual_host] = conn
            self.network_nodes.append(actual_host)
            command = {
                'type': 'updateNode',
                'nodes': self.network_nodes,
                'data': self.spy(),
                'host': self.host
            }

            self.sync_data(command)
            print(f'New server Conected: {actual_host}')
            self.connection_thread[actual_host] = Thread(target=self.listen_local_node, name=actual_host, args=[actual_host, self.subscribers[actual_host]])
            self.connection_thread[actual_host].setDaemon(True)
            self.connection_thread[actual_host].start()
            print(self.network_nodes)

    def listen_local_node(self, addr, conn):
        '''Method responsable for listen connection remote -> local'''
        while 1:
            try:
                data = []
                while 1:
                    packet = conn.recv(FIXED_MSG_SIZE)
                    retry = 0
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
                if retry == CON_RETRY:
                    break
                print(f"{addr} => Disconnected!")
                retry += 1
                time.sleep(5)
            except OSError as err:
                print(err)
                break

    def connect_remote_node(self, host, port=5000):
        '''stay in contact with each existing node in network'''
        while 1:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))
                self.subscribers[host] = sock
                print(f"Add by contacting +{host}")
                while 1:
                    retry = 0
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
                    print(f'Command Received from {host}:\n{command}')

            except ConnectionResetError as err:
                if retry == CON_RETRY:
                    break
                print(f"{host} => Disconnected!")
                retry += 1
                time.sleep(5)
            except ConnectionRefusedError as err:
                if retry == CON_RETRY:
                    break
                print(f"Trying reconnection to {host}!")
                retry += 1
                time.sleep(5)
            except OSError as err:
                print(f'[ERROR] {err}')
                break

    def connect_to_network(self):
        '''method that creates all connection threads'''
        for link in self.network_nodes:
            print(link)
            if link not in self.subscribers.keys() and link is not self.host and link not in self.connection_thread.keys():
                print("CRIANDO THREAD")
                self.connection_thread[link] = Thread(target=self.connect_remote_node, name=link, args=[link, 5000])
                self.connection_thread[link].setDaemon(True)
                self.connection_thread[link].start()
                print(f"{link} Conected")

    def sync_data(self, data):
        '''Method to syncronize data across all nodes
        :data: {'type: ?', 'data: [(key,value),...]'}
        '''
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
        '''Method responsable for handle commands for network'''
        if not isinstance(command, dict) or 'type' not in command.keys():
            print("Impossible to complete command")
            return

        #SERVER->SERVER COMMUNICATION COMMANDS

        if command['type'] == 'updateNode':
            for ipv4 in command['nodes']:
                if ipv4 not in self.network_nodes and ipv4 != self.host:
                    print(f"Adding by update + {ipv4}")
                    self.network_nodes.append(ipv4)

            for key in command['data'].keys()[::-1]:
                self.local_cache.sync_key(command['data'][key])

            self.connect_to_network()

        elif command['type'] == 'getHost':
            print(f"HOST ==>{self.host}")
            self.subscribers[command['host']].send(self.host.encode())

        elif command['type'] == 'syncSetKey':
            self.local_cache.set_key(command['data'][0], command['data'][1])

        elif command['type'] == 'syncGetKey':
            return self.local_cache.get_key(command['data'])

    #CLIENT->SERVER COMMUNICATION COMMANDS

    def set_key(self, key, value):
        '''method for client write to lru'''
        self.local_cache.set_key(key, value)
        command = {'type':'syncSetKey', 'data':(key, value)}
        self.sync_data(command)

    def spy(self):
        '''method for client spy on lru without touch it'''
        return self.local_cache.spy()

    def get_key(self, key):
        '''method for client read from lru'''
        command = {'type':'syncGetKey', 'data':key}
        self.sync_data(command)
        return self.local_cache.get_key(key)

    # CONTROLER

    def start_network(self):
        '''Start a new network'''
        self.server_node_thread = Thread(target=self.local_node, name="Local Cache Node")
        self.server_node_thread.setDaemon(True)
        self.server_node_thread.start()
        print("Network Started!")

    def join_network(self, node_ip):
        '''Connect to an existing network'''
        print(f"Joining Network of Node {node_ip}")
        self.network_nodes.append(node_ip)
        self.connect_to_network()
        self.start_network()

    def stop(self):
        '''stop all sockets and threads'''
        _ = [conn.close() for conn in self.subscribers.values()]

    def cache_io(self, func):
        ''' Decorator for saving input and output from custom functions/methods to lru
            usage:
            @cache_io
            function_for_caching
        '''
        def io_to_lru(*args, **kwargs):
            key = f'{func.__name__},{args},{kwargs}'
            lru = self.get_key(key)
            if lru == -1:
                result = func(*args, **kwargs)
                self.set_key(key, result)
            else:
                return lru
            return result
        return io_to_lru


if __name__ == "__main__":
    if len(sys.argv) > 1:
        NODE = CacheNetwork(join=sys.argv[1])
    else:
        NODE = CacheNetwork()
    while 1:
        try:
            pass
        except KeyboardInterrupt:
            NODE.stop()
            print("Exiting Network")
            break
