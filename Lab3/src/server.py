from concurrent.futures import ThreadPoolExecutor

import socket
import threading
import time
import sys

MAX_PACKET = 32768

def recv_all(sock):
    r'''Receive everything from `sock`, until timeout occurs, meaning sender
    is exhausted, return result as string.'''
    
    # dirty hack to simplify this stuff - you should really use zero timeout,
    # deal with async socket and implement finite automata to handle incoming data

    prev_timeout = sock.gettimeout()
    try:
        sock.settimeout(0.01)
    
        rdata = b""
        while True:
            try:
                rdata += sock.recv(MAX_PACKET)
            except socket.timeout:
                return rdata
    finally:
        sock.settimeout(prev_timeout)

def handle_client(conn, addr):
    print("[thread] starting")

    # recv message
    message = recv_all(conn).decode()

    if message:
        lines = message.splitlines()
        type, url, http_type = lines[0].split()

        params = {}
        url_split = url.split("?", 1)

        if len(url_split) == 2:
            for param in url_split[1].split("&"):
                if param:
                    key, value = param.split("=")
                    params[key] = value

        headers = {}
        for line in lines[1:]:
            if line:
                key, value = line.split(": ", 1)
                headers[key] = value

        print("[thread] client:", addr, "type:", type)
        print("[thread] client:", addr, "http_type:", http_type)
        for (k, v) in params.items():
            print("[thread] client:", addr, "params:", k, ":", v)
        for (k, v) in headers.items():
            print("[thread] client:", addr, "headers:", k, ":", v)

        if type == "GET":
            if "file" in params.keys():
                file = params["file"]

                with open(file, 'r', encoding='utf-8') as infile:
                    response_body = [
                        '<html><body>',
                        '<h1>Hello, world!</h1>',
                    ]


                    for line in infile.readlines():
                        response_body.append(f'<p>{line}</p>')

                    response_body.append('</body></html>')
                
                
                response_body_raw = ''.join(response_body)

                # Clearly state that connection will be closed after this response,
                # and specify length of response body
                response_headers = {
                    'Content-Type': 'text/html; encoding=utf8',
                    'Content-Length': len(response_body_raw),
                    'Connection': 'close',
                }
            
                response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.items())

                # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
                response_proto = 'HTTP/1.1'
                response_status = '200'
                response_status_text = 'OK' # this can be random

                # sending all this stuff
                message = f"{response_proto} {response_status} {response_status_text}" + "\r\n" \
                    + response_headers_raw + "\r\n" \
                    + response_body_raw
                conn.send(message.encode())

    conn.close()
    print("[thread] ending")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid arguments")
        exit(1)

    _, server_port, concurrency_level = sys.argv
    server_host = '127.0.0.1'
    server_port = int(server_port)
    concurrency_level = int(concurrency_level)

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((server_host, server_port))
    s.listen(1)

    all_threads = []
    with ThreadPoolExecutor(max_workers=concurrency_level) as executor:
        try:
            while True:
                print("Waiting for client")
                conn, addr = s.accept()
                executor.submit(handle_client, conn, addr)
        except KeyboardInterrupt:
            print("Stopped by Ctrl+C")
