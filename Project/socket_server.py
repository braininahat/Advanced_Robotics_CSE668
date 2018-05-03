import socket
from thread import *

 
def rec(conn, addr):
    while True:
        data = conn.recv(1028)
        if data:
            print data

HOST = ''                
PORT = 5000             
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    start_new_thread(rec,(conn, addr))

conn.close()
