import argparse
import socket
from lib.MessageInfo import MessageInfo
from lib.Node import Node
from lib.Connection import Connection
from lib.Segment import Segment
from lib.Constant import*
from lib.Utils import*
from lib.Logger import Logger

class Client(Node):
    def __init__(self, connection: Connection, server_ip: str, server_port: str, file_path: str):
        self.connection = connection
        self.server_ip = server_ip
        self.server_port = server_port
        self.file_path = file_path
        self.file = []
        self.log = Logger("Client")
        self.receivedFile = 0
        self.BUFFER_SIZE = 1024

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
                    self.log.success_log("SYN-ACK Received")
                    break
                else:
                    self.log.warning_log("Not SYN-ACK")
                    return False

            except socket.timeout:
                self.log.alert_log("Connection timed out")

        # Client kirim ACK
        ack = Segment()
        ack.set_flag([False, True, False])
        self.connection.setTimeout(TIMEOUT_TIME)
        self.connection.send(self.server_ip, self.server_port, ack)
        
        self.listen_file()
        return True

    def listen_file(self):

        while True:
            try:
                self.log.alert_log("Receiving file...")
                file_segment, _ = self.run()
                self.log.success_log("File received")
                seq_number = file_segment.segment.get_header()['seqNumber']
                flag = file_segment.segment.get_flag()

                with open(self.file_path, 'ab') as file:
                    # Jika FIN, maka kirim FIN ACK
                    if flag.fin:
                        self.log.success_log("FIN received")
                        ack = Segment()
                        ack.set_flag([False, False, True])
                        self.connection.send(self.server_ip, self.server_port, ack)
                        self.log.alert_log("Sending ACK")
                        break
                    else:
                        data = file_segment.segment.get_data()
                        file.seek(seq_number * self.BUFFER_SIZE)
                        file.write(data)
                        
                        # Kirim ACK
                        ack = Segment()
                        ack.set_flag([False, True, False])
                        ack.set_ack_number(seq_number)
                        self.connection.send(self.server_ip, self.server_port, ack)
                        self.log.alert_log("Sending ACK")

            except Exception as e:
                self.log.warning_log(e)
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