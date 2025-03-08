import socket

host = '127.0.0.1'
port = 8080

s = socket.socket()
s.connect((host, port))

print("Connected to the server")

message = "Hello world!"
print('send:', message)
s.send(message.encode())

message = s.recv(1024).decode()
print('recv:', message)
