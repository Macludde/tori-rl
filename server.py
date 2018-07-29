import socket               # Import socket module

socke = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 7051                 # Reserve a port for your service.
socket.bind((host, port))        # Bind to the port
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2

print("Server started. Listening on port", port)

socket.listen(5)                 # Now wait for client connection.
while True:
    client, addr = socket.accept()    # Establish connection with client.
    print('Got connection from', addr)
    client.send('Thank you for connecting'.encode('utf-8'))
    while True:
        data = client.recv(RECV_BUFFER)
        print(data)
        if data == 'exit':
            client.close()                # Close the connection
