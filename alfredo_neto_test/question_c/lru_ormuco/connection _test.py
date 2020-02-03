# # import socket
# # import pickle
# # from time import sleep
# # HOST = socket.gethostbyname(socket.gethostname())
# # HOST = '192.168.27.253'
# # PORT = 5000

# # while 1:
# #     try:
# #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #         s.connect((HOST, PORT))
# #         while 1:
# #             data = s.recv(1024)
# #             data = {'teste': 2}
# #             s.send(pickle.dumps(data))
# #             print('Received', repr(data))
# #     except ConnectionResetError as err:
# #         print(f"Server Desconectado")
# #     except ConnectionRefusedError as err:
# #         print("Trying to reconnect!")
# #         sleep(1)
# #     except OSError as err:
# #         print(err)
# #         break

# import lru_cache_network
# import time
# n = lru_cache_network.CacheNetwork(max_size=1000)

# @n.cache_io
# def fibonacci(num):
#     if num == 0:
#         return 0
#     elif num == 1:
#         return 1
#     return fibonacci(num - 1) + fibonacci(num - 2)

# timer = time.time()
# fibonacci(10)
# print(time.time()-timer)
# # print(n.spy())

# timer = time.time()
# fibonacci(10)
# print(time.time()-timer)
# print(n.spy())
# # n.set_key(1,2)
# # lista = [key for key in n.spy().keys()]
# print('-----------------------')
# # print(n.spy())
# import json
# print(json.dumps(n.spy(), indent=4, separators=("  ↓", " -> ")))
# # print(lista[::-1])