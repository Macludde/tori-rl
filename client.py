import socket               # Import socket module
import time

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 7051                 # Reserve a port for your service.

s.connect((host, port))
while True:
	print("Sending data")
	s.send('Hello!'.encode('utf-8'))
	time.sleep(1)