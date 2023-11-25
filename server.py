import argparse
import socket

from lib.Connection import Connection
from lib.Node import Node
from lib.Segment import Segment
from lib.Constant import*
from lib.Utils import*

class Server(Node):
    def __init__(self, connection: Connection, file_path: str):
        self.connection = connection
        self.file_path = file_path
        self.file = open(self.file_path, 'rb').read()
        self.file_segment = breakdown_file(self.file)

    def run(self):
        return self.connection.listen()

    def handleMessageInfo(segment: Segment):
        return "asdasdasdas"
    
    def three_way_handshake(self):
        ip_client = None
        port_client = None
        while True:
            try:
                syn, _ = self.run();
                bendera_syn = syn.segment.get_flag()
                port_client = syn.getPort()
                if bendera_syn.syn:
                    print("Bendera syn diterima Kakak - 13521015")
                    break
                else:
                    print("Bukan syn kakak - Willy")

            except socket.timeout:
                print("Timeout kakak - Willy")

        # Waktunya kirim SYN ACK (kakak)
        syn_ack = Segment()
        syn_ack.set_flag([True,True,False])
        self.connection.setTimeout(TIMEOUT_TIME)
        self.connection.send(port_client[0], port_client[1], syn_ack)

        # Waktunya terima ACK (kakak)
        while True:
            try:
                ack, _ = self.run()
                benderack = ack.segment.get_flag()
                if(benderack.ack and not benderack.syn and not benderack.fin):
                    print("ACK diterima kakak")
                    print("Kirim file")
                    self.send_file(port_client[0], port_client[1])
                    break
                else:
                    print("BUKAN ACK GO***")
            except socket.timeout:
                print("Timeout kakak")

    # KIRIM FILE
    def send_file(self,ip_client: str, port_client: int):
        # INISIALISASI SEGMENT
        N = WINDOW_SIZE
        Rn = 0
        Sb = 0
        Sm = N + 1
        SegmentCount = len(self.file_segment)
        print(f"Segment count: {SegmentCount}")

        while True:
            # Kirim segmen jika dan hanya jika Sb <= Rn < Sm
            while (Sb <= Rn <= Sm and Rn < SegmentCount):
                segment = Segment()
                segment.set_seq_number(Rn)
                if Rn >= len(self.file_segment):
                    break
                segment.set_data(self.file_segment[Rn])
                self.connection.send(ip_client, port_client, segment)
                print(f"Kirim segmen {Rn}")
                Rn += 1
            # Terima ACK
            try:
                ack, _ = self.run()
                ack_number = ack.segment.get_header()['ackNumber']
                print(f"Terima ACK {ack_number}")
                if ack_number == SegmentCount - 1:
                    break
                Sb = ack_number
                Sm = Sb + N + 1
            except Exception as e:
                print(e)
                break
        # Tutup koneksi
        self.close_connection(ip_client, port_client)

    def close_connection(self, ip_client: str, port_client: int):
        # Kirim FIN
        fin = Segment()
        fin.set_flag([False, False, True])
        self.connection.send(ip_client, port_client, fin)
        print("Kirim FIN")
        # Terima FIN ACK
        while True:
            try:
                fin, _ = self.run()
                bendera_fin = fin.segment.get_flag()
                print("bendera ack : ", bendera_fin.ack)
                print("bendera fin : ", bendera_fin.fin)
                if bendera_fin.fin:
                    print("FIN diterima kakak")
                    break
                else:
                    print("Bukan FIN ACK kakak")
            except Exception as e:
                print("Timeout kakak")
                print(e)
        # Tutup koneksi
        print("Tutup koneksi")
        self.connection.close()

def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-p', '--port', type=int, default=5000, help='port to listen on')
    arg.add_argument('-f', '--file', type=str, default='input.txt', help='path to file input')
    arg.add_argument('-par', '--parallel', type=int, default=0, help='turn on/off parallel mode')
    args = arg.parse_args()
    return args

if __name__ == '__main__':
    while True:
        args = load_args()
        conn = Connection(port=3839)
        server = Server(conn, file_path=args.file)
        server.three_way_handshake()
        print("Selesai")