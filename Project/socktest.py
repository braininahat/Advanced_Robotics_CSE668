import socket

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(("pranavs-mbp", 5000))

for i in range(1000):
    client_socket.send(str(i))

client_socket.close()
