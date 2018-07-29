import socket               # Import socket module

<<<<<<< HEAD
s = socket.socket()         # Create a socket object
host = "localhost" # Get local machine name
port = 7051                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
=======
socke = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 7051                 # Reserve a port for your service.
socket.bind((host, port))        # Bind to the port
>>>>>>> 8b33d3155415979817fdc20feb722fd18ff9cc94
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2

print("Server started. Listening on port", port)

socket.listen(5)                 # Now wait for client connection.
while True:
<<<<<<< HEAD
	c, addr = s.accept()     # Establish connection with client.
	print('Got connection from', addr)
	c.send('Thank you for connecting'.encode('utf-8'))
	while True:
		data = c.recv(RECV_BUFFER)
		if data != b'':
			print(data)
		if data=='exit':
			c.close()              # Close the connection
s.close()
=======
    client, addr = socket.accept()    # Establish connection with client.
    print('Got connection from', addr)
    client.send('Thank you for connecting'.encode('utf-8'))
    while True:
        data = client.recv(RECV_BUFFER)
        print(data)
        if data == 'exit':
            client.close()                # Close the connection
>>>>>>> 8b33d3155415979817fdc20feb722fd18ff9cc94
