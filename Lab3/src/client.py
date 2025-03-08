import socket
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


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Invalid parameters")
		exit(1)

	_, server_host, server_port, filename = sys.argv
	server_port = int(server_port)

	s = socket.socket()
	s.connect((server_host, server_port))

	print("Connected to the server")

	s.send(f"GET {server_host}:{server_port}/?file={filename} HTTP/1.1\r\nConnection: keep-alive".encode())

	message = b""
	while True:
		got = s.recv(1024)

		if len(got):
			message += got
		else:
			break;
	print('recv:', message.decode())

	s.close()
