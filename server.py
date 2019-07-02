import socket
import time
from _thread import *

addr = "192.168.2.62"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket succesfully created")
s.bind((addr, port))
print("Succesfully bound to, ", (addr, port))
s.listen(1)
print("Listening for connection...")


def clientthread(conn):
    welcomeMessage = ("Welcome to the server. Type something and hit enter\n")
    conn.send(welcomeMessage.encode())

    while True:
        data = conn.recv(8096)
        reply = ("Message of the client:" + data.decode())
        if not data:
            break;
        print(reply)
        conn.sendall(reply.encode())
    conn.close()


while True:
    conn, address = s.accept()
    print(f"Connection from {address} has been established")
    start_new_thread(clientthread, (conn,))

s.close()



