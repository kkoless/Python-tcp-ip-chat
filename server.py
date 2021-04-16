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
    for client in clients:
        client.send(message)
        client.send(f"[USERS]{str(nicknames)}".encode("utf-8"))


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            clients.remove(client)
            client.close()
            broadcast(f"{nickname} left chat!\n".encode("utf-8"))
            break


def receive():
    while True:
        client, address = server.accept()
        print(address)
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()


print("Server is running...")
receive()

