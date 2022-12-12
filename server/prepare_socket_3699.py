import socket
import threading
import queue
import json
import time

from dynamodb_ops import insert, read, update

insert_lock = threading.Lock()
read_lock = threading.Lock()
update_lock = threading.Lock()

def prepare_socket_3699():
    # Create a TCP/IP socket
    socket_threads_3699 = []
    q_3699 = queue.Queue()
    for i in range(3):
        t = threading.Thread(target = nosql_db_request, args = [q_3699], daemon=True)
        socket_threads_3699.append(t)
        t.start()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('', 3699)
        print ('connecting to %s port %s' % server_address)
        sock.bind(server_address)

        while True:
            # Listen for incoming connections
            sock.listen(1)
            # Wait for a connection
            print ('waiting for a connection')
            connection, client_address = sock.accept()

            src_address, src_port = sock.getsockname()
            print ('connection from', client_address)
            print ('coonection port', src_port)
            try:
                q_3699.put(connection)
            except Exception as e:
                print (e)
                break
    except KeyboardInterrupt:
        print ('Closing')
        sock.close()
    finally:
        print ('joining threads')
        for t in socket_threads_3699:
            t.join()


def nosql_db_request(q):
    # Receive the data in small chunks and retransmit it
    while True:
        connection = q.get()
        print ('---->', threading.currentThread().getName(), 'Started <----')
        #time.sleep(30)
        data_recived = connection.recv(1024)
        data = data_recived.decode("utf-8")
        data = json.loads(data)
        print (data)
        if data['op'] == 'r':
            response = read_from_db(data)
        elif data['op'] == 'i':
            response = insert_to_db(data)
        elif data['op'] == 'u':
            response = update_to_db(data)
        else:
            response = {'Status':'Failed', 'Message' : 'Wrong Operation Requested.'}
        print ('sending data back to the client')
        response = json.dumps(response, default = default_json)
        print (response)
        response = bytes(response, encoding="utf-8")
        connection.sendall(response)
        q.task_done()
        print ('---->', threading.currentThread().getName(), 'Finished <----')
    
def read_from_db(data):
    while True:
        if not update_lock.locked():
            read_lock.acquire()
            print ('reading from db')
            response = read(data)
            read_lock.release()
            break
    return response

def insert_to_db(data):
    while True:
        if not insert_lock.locked():
            insert_lock.acquire()
            print ('writing to db')
            response = insert(data)
            insert_lock.release()
            break
    return response

def update_to_db(data):
    while True:
        if not insert_lock.locked() and not update_lock.locked() and not read_lock.locked():
            update_lock.acquire()
            print ('updating to db')
            response = update(data)
            update_lock.release()
            break
    return response

def default_json(val):
    return str(val)
