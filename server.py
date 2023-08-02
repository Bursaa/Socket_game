import socket
from _thread import *
from game import Game
import pickle

server = "192.168.8.109"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        data = conn.recv(4096).decode()

        try:
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()

                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("LOST CONNECTION")
    try:
        del games[gameId]
        print("CLOSING GAME", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    connected, addres = s.accept()
    print("Connected to:", addres)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (connected, p, gameId))
