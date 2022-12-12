import socket
import threading
import queue

from msg_encoding_decoding import recv_msg, send_msg

def prepare_socket_9090():
    # Create a TCP/IP socket
    socket_threads_9090 = []
    q_9090 = queue.Queue()
    for i in range(3):
        t = threading.Thread(target = sql_db_request, args = [q_9090], daemon=True)
        socket_threads_9090.append(t)
        t.start()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('', 9090)
        print ('connecting to %s port %s' % server_address)
        sock.bind(server_address)
        while True:
            # Listen for incoming connections
            sock.listen(1)

            # Wait for a connection
            print ('waiting for a connection')
            connection, client_address = sock.accept()

            # Receive the data in small chunks and retransmit it
            src_address, src_port = sock.getsockname()
            print ('connection from', client_address)
            print ('coonection port', src_port)
            try:
                q_9090.put(connection)
            except Exception as e:
                print (e)
                break
    except KeyboardInterrupt:
        print ('Closing')
        sock.close()
    finally:
        print ('joining threads')
        for t in socket_threads_9090:
            t.join()

def sql_db_request(q):
    # Receive the data in small chunks and retransmit it
    while True:
        connection = q.get()
        print ('---->', threading.currentThread().getName())
        while True:
            data = recv_msg(connection)
            print ('received "%s"' % data)
            if data != None:
                print ('sending data back to the client')
                connection.sendall(data)
            else:
                print ('no more data from client')
                break
        q.task_done()