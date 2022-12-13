import socket
import json
import time

def prepare_socket(port, request_data):
    request_data_json = json.dumps(request_data)
    request_data_in_bytes = bytes(request_data_json, encoding="utf-8")
    
    # Create a TCP/IPv4 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('13.235.33.137', port)
    print ('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        
        # Send data
        print ('sending data to server')
        sock.sendall(request_data_in_bytes)

        # Look for the response
        data_recived = sock.recv(1024)
        data = data_recived.decode("utf-8")
        print (data)
    finally:
        print ('closing socket')
        sock.close()