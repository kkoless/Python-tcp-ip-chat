import socket
import threading

host = "127.0.0.1"
port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(client)
        print(address[1])
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode("utf-8"))
        client.send("Connected to the server\n".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()


print("Server is running...")
receive()



# while not flag:
#     try:
#         data, address = server.recvfrom(1024)
#         if address not in clients:
#             clients.append(address)
#
#         print(f"[{address[0]}] --- [{str(address[1])}]  //  ", end="")
#         print(data.decode("utf-8"))
#
#         for client in clients:
#             if address != client:
#                 server.sendto(data, client)
#     except:
#         print("\nServer stopped!")
#         flag = True

