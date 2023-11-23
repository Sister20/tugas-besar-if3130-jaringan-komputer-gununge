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
                ip_client = syn.getIP()
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
        self.   connection  . send     (ip_client, port_client, syn_ack)

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

def listen(port):
    # create a socket object and connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)
    print('Listening on port', port)
    return s

def main():
    args = load_args()
    print(args)

    s = listen(args.port)
    while True:
        # establish connection with client
        c, addr = s.accept()
        print('Got connection from', addr)
        # receive data from client
        data = c.recv(1024)
        print('Received', repr(data))
        # send data to client
        c.send(data)
        # close the connection
        c.close()

if __name__ == '__main__':
    main()
