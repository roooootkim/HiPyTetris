import socket
import pickle

class Network:
    def __init__(self, address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = address
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getp(self):
        return self.p

    def connect(self):
        self.client.connect(self.addr)
        return pickle.loads(self.client.recv(2048 * 3))

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))  # 서버에 정보를 보내고 받은 정보 리턴
            return pickle.loads(self.client.recv(2048 * 3))
        except socket.error as e:
            print(e)

