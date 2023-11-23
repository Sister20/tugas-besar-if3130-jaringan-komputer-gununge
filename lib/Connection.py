from MessageInfo import MessageInfo
# from typing import Callable
import socket


class Connection:
    def __init__(self, ip: str = None, port: int = None):
        self.ip = ip
        self.port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__handler= callable(message=MessageInfo())
        print(self.__handler)
        
if __name__ == "__main__":
    conn = Connection()