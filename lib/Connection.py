import socket
from .Segment import Segment


class Connection:
    def __init__(self, ip: str = 'localhost', port: int = 6969):
        self.ip = ip
        self.port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((self.ip, self.port))
        self.__handler = None

    def send(self, ip_remote: str, port_remote: int, message: Segment):
        self.__socket.sendto(message.get_bytes(), (ip_remote, port_remote))

    def listen(self):
        data, addr = self.__socket.recvfrom(32768)
        message = Segment()
        message.set_from_bytes(data)
        # check checksum
        if not message.valid_checksum():
            raise Exception("Checksum not valid")
        if self.__handler:
            self.__handler(message)
        return message, addr

    def close(self):
        self.__socket.close()

    def setTimeout(self, timeout: int):
        self.__socket.settimeout(timeout)


if __name__ == "__main__":
    conn = Connection()
    conn.listen()
