from typing import Callable
import socket
from .MessageInfo import MessageInfo
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
        message = MessageInfo(data, addr)
        message.segment.set_from_bytes(data)
        if self.__handler:
            self.__handler(message)
        return message, addr;

    def close(self):
        self.__socket.close()

    def register_handler(self, handler: Callable[[MessageInfo], None]):
        self.__handler = handler

    def notify(self, message: MessageInfo):
        if self.__handler:
            self.__handler(message)

    def setTimeout(self, timeout: int):
        self.__socket.settimeout(timeout)

if __name__ == "__main__":
    conn = Connection()
    conn.register_handler(lambda msg: print(msg))
    conn.listen()
