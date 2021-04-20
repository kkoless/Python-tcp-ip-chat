import socket
import threading

host = socket.gethostbyname(socket.gethostname())
port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    nicknames_list = '\n'.join(nicknames)
    for client in clients:
        client.send(message)
        client.send(f'[USERS]{nicknames_list}'.encode("utf-8"))


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            # print(f"{nicknames[clients.index(client)]} сказал: {message.decode('utf-8')}")
            broadcast(message)
        except:
            index = clients.index(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            clients.remove(client)
            client.close()
            broadcast(f"{nickname} покинул сервер!\n".encode("utf-8"))
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Соединение с {str(address)}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"Никнейм клиента: {nickname}")
        broadcast(f"{nickname} подключился к серверу!\n".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()


print("Server is running...")
receive()
