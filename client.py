import argparse
import socket
from lib.Node import Node
from lib.Connection import Connection
from lib.Segment import Segment
from lib.Constant import *
from lib.Utils import *
from lib.Logger import Logger


class Client(Node):
    def __init__(self, connection: Connection, server_ip: str, server_port: str, folder_path: str):
        self.connection = connection
        self.server_ip = server_ip
        self.server_port = server_port
        self.folder_path = folder_path
        self.file_path = None
        self.file = []
        self.log = Logger("Client")
        self.buffer_size = 1024

    def run(self):
        self.three_way_handshake()
        self.listen_file()

    def handleMessageInfo(segment: Segment):
        pass

    def three_way_handshake(self):
        # Client kirim SYN
        syn = Segment()
        syn.set_flag([True, False, False])
        self.connection.send(self.server_ip, self.server_port, syn)

        # Client Terima Syn Ack
        while True:
            try:
                # self.connection.setTimeout(TIMEOUT_TIME)
                syn_ack, _ = self.connection.listen()
                flag = syn_ack.get_flag()
                if (flag.syn and flag.ack):
                    self.log.success_log("SYN-ACK Received")
                    break
                else:
                    self.log.warning_log("Not SYN-ACK")
                    return False

            except socket.timeout:
                self.log.alert_log("Connection timed out")

        # Client kirim ACK
        try:
            ack = Segment()
            ack.set_flag([False, True, False])
            # self.connection.setTimeout(TIMEOUT_TIME)
            self.connection.send(self.server_ip, self.server_port, ack)
        except socket.timeout:
            self.log.alert_log("Connection timed out")
            return False
        return True

    def listen_file(self):
        N = WINDOW_SIZE
        Rn = 0
        Sn = 0
        METADATA_SEQ = -1

        # Terima file, pengulangan hingga file selesai
        while True:
            # self.connection.setTimeout(TIMEOUT_TIME)
            try:
                self.log.alert_log("Receiving file...")
                file_segment, _ = self.connection.listen()
                self.log.success_log("File received")
                Sn = file_segment.get_header()['seqNumber']
                self.log.alert_log(f"Receiving segment {Sn}")
                flag = file_segment.get_flag()

                if (Sn == METADATA_SEQ):
                    self.log.success_log("Metadata received")
                    self.log.alert_log("Sending ACK Metadata")
                    ack = Segment()
                    ack.set_flag([False, True, False])
                    ack.set_ack_number(Sn)
                    self.connection.send(self.server_ip, self.server_port, ack)
                    self.log.alert_log(f"Sending ACK {Sn}")
                    self.file_path = file_segment.get_data().decode()
                    self.log.alert_log(f"File path: {self.file_path}")
                    METADATA_SEQ -= 1
                    continue

                # Jika FIN, maka kirim FIN ACK
                elif flag.fin:
                    self.log.success_log("FIN received")
                    # ack ke server
                    ack = Segment()
                    ack.set_flag([False, True, True])
                    self.connection.send(self.server_ip, self.server_port, ack)
                    self.log.alert_log("Sending ACK FIN")
                    break

                elif Sn == Rn:
                    data = file_segment.get_data()
                    if data:
                        file = open(self.folder_path + '/' +
                                    self.file_path, 'ab')
                        file.seek(Sn)
                        file.write(data)
                        Rn += 1

                    # Kirim ACK
                    ack = Segment()
                    ack.set_flag([False, True, False])
                    ack.set_ack_number(Sn)

                    self.connection.send(self.server_ip, self.server_port, ack)
                    self.log.alert_log(f"Sending ACK {Sn}")
                else:
                    if (Rn - Sn >= N):
                        self.log.warning_log(
                            f"Segment {Sn} is out of window, Resending ACK {Rn}")
                        self.connection.send(
                            self.server_ip, self.server_port, ack)
                    else:
                        self.log.warning_log(
                            f'Segment {Sn} is refused, expected {Rn}')

            except Exception as e:
                self.log.warning_log(e)
                break


def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-c', '--client', type=int, default=7331, help='port the client is on')
    arg.add_argument('-i', '--ip', type=str, default='localhost', help='ip to listen on')
    arg.add_argument('-p', '--port', type=int, default=1337, help='port to listen on')
    arg.add_argument('-f', '--folder', type=str, default='output', help='path to folder output')
    args = arg.parse_args()
    return args


if __name__ == "__main__":
    args = load_args()
    klien = Client(Connection(port=args.client), server_ip=args.ip,
                   server_port=args.port, folder_path=args.folder)
    klien.run()
