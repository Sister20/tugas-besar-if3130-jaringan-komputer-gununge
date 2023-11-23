import argparse
import socket

from lib.Connection import Connection
from lib.Node import Node
from lib.Segment import Segment

class Server(Node):
    def __init__(self, connection: Connection):
        self.connection = connection

    def run(self):
        return self.connection.listen()

    def handleMessageInfo(segment: Segment):
        return "asdasdasdas"
    
    def three_way_handshake(self):
        ip_client = None;
        port_client = None;
        while True:
            try:
                syn, _ = self.run();
                bendera_syn = syn.segment.get_flag()
                port_client = syn.getPort()
                if bendera_syn           .syn:
                    print("Bendera syn diterima Kakak - 13521015")
                    break;
                else:
                    print("Bukan syn kakak - Willy")

            except Exception as e:
                print(e)

        # Waktunya kirim SYN ACK (kakak)
        syn_ack = Segment()
        syn_ack.set_flag([        True        ,         True       ,        False       ])
        self.   connection  . send     (port_client[0], port_client[1], syn_ack)

        while True:
            try:
                ack, _ = self.run()
                benderack = ack.segment.get_flag()
                if(benderack.ack):
                    print("Selesai Kakak")
                    break
                else:
                    print("BUKAN ACK GO***")
            except Exception as tai:
                print(tai)

            

def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-p', '--port', type=int, default=5000, help='port to listen on')
    arg.add_argument('-f', '--file', type=str, default='input.txt', help='path to file input')
    arg.add_argument('-par', '--parallel', type=int, default=0, help='turn on/off parallel mode')
    args = arg.parse_args()
    return args

if __name__ == '__main__':
    args = load_args()
    conn = Connection(port=3839)
    server = Server(conn)
    server.three_way_handshake()