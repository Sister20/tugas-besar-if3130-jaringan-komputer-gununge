import argparse
import socket
from lib.MessageInfo import MessageInfo
from lib.Node import Node
from lib.Connection import Connection
from lib.Segment import Segment
from lib.Constant import*
from lib.Utils import*

class Client(Node):
    def __init__(self, connection: Connection, server_ip: str, server_port: str, file_path: str):
        self.connection = connection
        self.server_ip = server_ip
        self.server_port = server_port
        self.file_path = file_path
        self.file = []

    def run(self):
        return self.connection.listen()

    def handleMessageInfo(segment: Segment):
        pass

    def three_way_handshake(self, msg: MessageInfo):
        # Client kirim SYN
        syn = Segment()
        syn.set_flag([True, False, False])
        self.connection.setTimeout(TIMEOUT_TIME)
        self.connection.send(self.server_ip, self.server_port, syn)

        # Client Terima Syn Ack
        while True:
            try:
                syn_ack, _ = self.run()
                pataka_syn_ack = syn_ack.segment.get_flag()
                if(pataka_syn_ack.syn and pataka_syn_ack.ack):
                    print("SYN ACK Keterima Kakak")
                    break
                else:
                    print("Wah ini mah kena otaknya")
                    return False

            except socket.timeout:
                print("Timeout Kakak")

        # Client kirim ACK
        ack = Segment()
        ack.set_flag([False, True, False])
        self.connection.setTimeout(TIMEOUT_TIME)
        self.connection.send(self.server_ip, self.server_port, ack)
        
        self.listen_file()
        return True

    def listen_file(self):
        N = WINDOW_SIZE
        Rn = 0
        Sb = 0

        # Terima file, pengulangan hingga file selesai
        while True:
            try:
                print("Menerima file")
                file_segment, _ = self.run()
                print("File diterima kakak")
                Sb = file_segment.segment.get_header()['seqNumber']
                flag = file_segment.segment.get_flag()

                # Jika FIN, maka kirim FIN ACK
                if flag.fin:
                    print("FIN diterima kakak")
                    bytearray = merge_file(self.file)
                    file = open(self.file_path, 'wb')
                    file.write(bytearray)
                    file.close()
                    # ack ke server
                    ack = Segment()
                    ack.set_flag([False, False, True])
                    self.connection.send(self.server_ip, self.server_port, ack)
                    print("Kirim ACK")
                    break
                
                elif Sb == Rn:
                    last = len(self.file)
                    print(last)
                    if last == Sb:
                        self.file.append(file_segment.segment.get_data())
                        Rn += 1

                    # Kirim ACK
                    ack = Segment()
                    ack.set_flag([False, True, False])
                    ack.set_ack_number(Sb)
                    self.connection.send(self.server_ip, self.server_port, ack)
                    print("Kirim ACK")
                else :
                    print(Sb,Rn)
                    if (Rn - Sb >= N):
                        self.connection.send(self.server_ip, self.server_port, ack)
                    else:
                        print("Tolak segment")

            except Exception as e:
                print(e)
                break


def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-c', '--client', type=int, default=8000, help='port the client is on')
    arg.add_argument('-p', '--port', type=int, default=8080, help='port to listen on')
    arg.add_argument('-f', '--file', type=str, default='output.mp4', help='path to file input')
    args = arg.parse_args()
    return args

if __name__ == "__main__":
    args = load_args()
    conn = Connection(port=3939)
    informasiPesan = MessageInfo("localhost", 50)
    klien = Client(conn, server_ip="localhost", server_port=3839, file_path=args.file)
    klien.three_way_handshake(informasiPesan)