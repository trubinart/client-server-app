from socket import *
import select


def read_requests(r_clients, w_clients, all_clients):
    for r_sock in r_clients:
        try:
            message = r_sock.recv(1024)
        except:
            pass

        for sock in w_clients:
            try:
                sock.send(message)
            except:
                all_clients.remove(sock)

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 7978))
s.listen(5)
s.settimeout(0.2)

all_clients = []

while True:
    try:
        client, addr = s.accept()
        all_clients.append(client)
    except OSError as e:
        print(e)

    try:
        r, w, e = select.select(all_clients, all_clients, [], 0)
    except:
        pass

    read_requests(r, w, all_clients)

