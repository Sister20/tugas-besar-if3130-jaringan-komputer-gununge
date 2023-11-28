import socket
from .Segment import Segment
from .Constant import *

class Connection:
    def __init__(self, ip: str = 'localhost', port: int = 6969):
        self.ip = ip
        self.port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((self.ip, self.port))

    def send(self, ip_remote: str, port_remote: int, message: Segment):
        self.__socket.sendto(message.get_bytes(), (ip_remote, port_remote))

    def listen(self, timeout = TIMEOUT_TIME):
            self.__socket.settimeout(timeout)
            data, addr = self.__socket.recvfrom(32768)
            message = Segment()
            message.set_from_bytes(data)
            # check checksum
            if not message.valid_checksum():
                raise Exception("Checksum not valid")
            return message, addr

    def close(self):
        self.__socket.close()

    def setTimeout(self, timeout: int):
        self.__socket.settimeout(timeout)


if __name__ == "__main__":
    conn = Connection()
    conn.listen()
