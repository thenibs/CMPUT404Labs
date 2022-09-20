#!/usr/bin/env python3
from multiprocessing import Process
import socket
import time

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)

        while True:
            conn, addr = s.accept()
            print("\n\nConnected by", addr, "\n", conn)
            p = Process(target=handle_echo, args={conn})
            p.daemon = True
            p.start()
            print("Started process ", p)

def handle_echo(conn):
    full_data = conn.recv(BUFFER_SIZE)
    print(full_data)
    time.sleep(0.5)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

if __name__ == "__main__":
    main()
