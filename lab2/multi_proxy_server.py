#!/usr/bin/env python3
import socket
import time
import sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_send(conn, proxy_end):
    # send data
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending data {send_full_data} to Google")
    proxy_end.sendall(send_full_data)

    proxy_end.shutdown(socket.SHUT_WR)

    #recieve data, wait a bit, then send it back to client
    data = proxy_end.recv(BUFFER_SIZE)
    time.sleep(0.5)
    print(f"Sending received data {data} back to client")
    conn.sendall(data)

def main():
    #define address & buffer size
    host = "www.google.com"
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Proxy start")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(5)
        
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Google connecting..")
                remote_ip = get_remote_ip(host)

                proxy_end.connect((remote_ip, port))

                p = Process(target=handle_send, args={conn, proxy_end})
                p.daemon = True
                p.start()
                print("Started process ", p)

            conn.close()

if __name__ == "__main__":
    main()
