#!/usr/bin/env python3
import socket, sys

def main():
    #define address info, payload, and buffer size
    addr = ("127.0.0.1", 8001)

    host = 'localhost'
    port = 8001
    buffer_size = 1024
    payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'

    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)

        full_data = s.recv(buffer_size)
        print(full_data)

    except Exception as e:
        print(e)
        sys.exit()
    finally:
        s.close()

if __name__ == "__main__":
    main()
