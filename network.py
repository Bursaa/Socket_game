import pickle
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.8.109"
        self.port = 5555
        self.addres = (self.server, self.port)
        self.p= self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addres)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)