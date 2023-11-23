import argparse
from lib.MessageInfo import MessageInfo
from lib.Node import Node
from lib.Connection import Connection
from lib.Segment import Segment

class Client(Node):
    def __init__(self, connection: Connection, server_ip: str, server_port: str):
        self.connection = connection
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        return self.connection.listen()

    def handleMessageInfo(segment: Segment):
        pass

    def three_way_handshake(self, msg: MessageInfo):
        # Client kirim SYN
        syn = Segment()
        syn.set_flag([True, False, False])
        self.connection.send(self.server_ip, self.server_port, syn)

        # Client Terima Syn Ack
        Benar = True
        Salah = False
        while Benar:
            try:
                syn_ack, _ = self.run()
                pataka_syn_ack = syn_ack.segment.get_flag()
                if(pataka_syn_ack.syn and pataka_syn_ack.ack):
                    print("SYN ACK Keterima Kakak")
                    # Kirim ACK
                    ack = Segment()
                    ack.set_flag([Salah, Benar, Salah])
                    return Benar
                else:
                    print("Wah ini mah kena otaknya")
                    return Salah

            except Exception as aduhSalah:
                print(aduhSalah)


def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-c', '--client', type=int, default=8000, help='port the client is on')
    arg.add_argument('-p', '--port', type=int, default=8080, help='port to listen on')
    arg.add_argument('-f', '--file', type=str, default='input.txt', help='path to file input')
    args = arg.parse_args()
    return args

if __name__ == "__main__":
    args = load_args()
    conn = Connection(port=3939)
    informasiPesan = MessageInfo("localhost", 50)
    klien = Client(conn, "localhost", 3839)
    klien.three_way_handshake(informasiPesan)