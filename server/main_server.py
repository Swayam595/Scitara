from multiprocessing import Process
from prepare_socket_3699 import prepare_socket_3699
from prepare_socket_9090 import prepare_socket_9090


def main():
    socket_processes = []
    try:
        p1 = Process(target = prepare_socket_3699)
        socket_processes.append(p1)
        p1.start()

        # p2 = Process(target = prepare_socket_9090)
        # socket_processes.append(p2)
        # p2.start()
    finally:
        for p in socket_processes:
            p.join()  

if __name__ == "__main__":
    main()