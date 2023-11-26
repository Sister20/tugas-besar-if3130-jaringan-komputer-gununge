import argparse
import socket

from lib.Connection import Connection
from lib.Node import Node
from lib.Segment import Segment
from lib.Constant import *
from lib.Utils import *
from lib.Logger import Logger


class Server(Node):
    def __init__(self, connection: Connection, file_path: str):
        self.connection = connection
        self.file_path = file_path
        self.file = open(self.file_path, 'rb').read()
        self.port_clients = []
        self.file_segment = breakdown_file(self.file)
        self.log = Logger("Server")

    def run(self):
        # three way handshake and send file
        self.three_way_handshake()
        self.send_file(self.port_clients[0], self.port_clients[1])

    def handleMessageInfo(segment: Segment):
        return "asdasdasdas"

    def three_way_handshake(self):
        ip_client = None
        while True:
            syn, _ = self.connection.listen()
            bendera_syn = syn.segment.get_flag()
            self.port_clients = syn.getPort()
            if bendera_syn.syn:
                self.log.success_log("SYN received")
                break
            else:
                self.log.warning_log("Not SYN")

        # Waktunya kirim SYN ACK (kakak)
        syn_ack = Segment()
        syn_ack.set_flag([True, True, False])
        self.connection.send(
            self.port_clients[0], self.port_clients[1], syn_ack)

        # Waktunya terima ACK (kakak)
        while True:
            try:
                self.connection.setTimeout(TIMEOUT_TIME)
                ack, _ = self.connection.listen()
                benderack = ack.segment.get_flag()
                if (benderack.ack and not benderack.syn and not benderack.fin):
                    self.log.success_log("ACK received")
                    self.log.alert_log("Sending file...")
                    break
                else:
                    self.log.warning_log("Not ACK")
            except socket.timeout:
                self.log.warning_log("Connection timed out")
                self.connection.send(
                    self.port_clients[0], self.port_clients[1], syn_ack)
                self.log.alert_log("Sending SYN ACK again...")

    # KIRIM FILE
    def send_file(self, ip_client: str, port_client: int):
        # INISIALISASI SEGMENT
        N = WINDOW_SIZE
        Rn = 0
        Sb = 0
        Sm = N - 1
        SegmentCount = len(self.file_segment)
        self.log.alert_log(f"Segment count: {SegmentCount}")

        while True:
            # Kirim segmen jika dan hanya jika Sb <= Rn < Sm
            while (Sb <= Rn <= Sm and Rn < SegmentCount):
                segment = Segment()
                segment.set_seq_number(Rn)
                if Rn >= len(self.file_segment):
                    break
                segment.set_data(self.file_segment[Rn])
                self.connection.send(ip_client, port_client, segment)
                self.log.alert_log(f"Sending segment {Rn}/{SegmentCount - 1}")
                Rn += 1
            # Terima ACK
            self.connection.setTimeout(TIMEOUT_TIME)
            try:
                ack, _ = self.connection.listen()
                ack_number = ack.segment.get_header()['ackNumber']
                self.log.success_log(f"ACK {ack_number} received")
                if ack_number == SegmentCount - 1:
                    break
                Sb = ack_number
                Sm = Sb + (N - 1)
            except socket.timeout:
                Rn = Sb
                self.log.warning_log("Connection timed out")
        # Tutup koneksi
        self.close_connection(ip_client, port_client)

    def close_connection(self, ip_client: str, port_client: int):
        # Kirim FIN
        fin = Segment()
        fin.set_flag([False, False, True])
        self.connection.send(ip_client, port_client, fin)
        self.log.alert_log("Sending FIN")
        # Terima FIN ACK
        while True:
            try:
                fin, _ = self.connection.listen()
                bendera_fin = fin.segment.get_flag()
                if bendera_fin.fin and bendera_fin.ack:
                    self.log.success_log("FIN ACK received")
                    break
                else:
                    self.log.warning_log("Not FIN ACK")
            except Exception as e:
                self.log.warning_log("Connection timed out")
                print(e)
                break
        # Tutup koneksi
        self.log.success_log("Connection closed")
        self.connection.close()


def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-p', '--port', type=int,default=5000, help='port to listen on')
    arg.add_argument('-f', '--file', type=str,default='input.txt', help='path to file input')
    arg.add_argument('-par', '--parallel', type=int,default=0, help='turn on/off parallel mode')
    args = arg.parse_args()
    return args


if __name__ == '__main__':
    while True:
        args = load_args()
        conn = Connection(port=3839)
        server = Server(conn, file_path=args.file)
        server.run()
