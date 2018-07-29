import socket
import select
import sys

server = socket.socket()
host = "172.16.0.127" 
port = 7051
server.bind((host, port))
RECV_BUFFER = 4096 

print("Server started. Listening on port", port)

server.listen(5)
while True:
	client, addr = server.accept()
	print('Got connection from', addr)
	while True:
		if False:
			data = client.recv(RECV_BUFFER)
			if data != b'':
				print(data)
			if data == 'exit':
				client.close()
			if data == 'close-server':
				server.close()
				exit()
		msg = input("message: ")
		if len(msg) == 21:
			client.send((msg + "\n").encode('utf-8'))
