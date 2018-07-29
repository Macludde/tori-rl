import socket
import select
import sys

server = socket.socket()
host = "localhost" 
port = 7051
server.bind((host, port))
RECV_BUFFER = 4096 

print("Server started. Listening on port", port)

server.listen(5)
while True:
	client, addr = server.accept()
	print('Got connection from', addr)
	client.send('Thank you for connecting'.encode('utf-8'))
	while True:
		data = client.recv(RECV_BUFFER)
		if data != b'':
			print(data)
		if data=='exit':
			client.close()
server.close()
