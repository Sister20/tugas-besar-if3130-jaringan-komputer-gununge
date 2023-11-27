import argparse
import socket

from lib import *


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
        self.segment = Segment()

    def run(self):
        self.three_way_handshake()
        self.listen_file()

    def three_way_handshake(self):
        # Send initial connection
        self.log.alert_log(f"[!] Starting 3-way handshake with {self.server_ip}:{self.server_port}")
        # Initial Connection
        self.connection.send(self.server_ip, self.server_port, self.segment)

        while True:
            try:
                msg, _ = self.connection.listen(TIMEOUT_LISTEN)
                self.segment = msg
                # Send SYN-ACK
                if self.segment.is_syn_flag():
                    self.segment = Segment()
                    self.segment.set_flag([True, True, False])
                    self.log.alert_log(f"[!] Sending SYN-ACK to {self.server_ip}:{self.server_port}")
                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=self.segment)
                # Resend SYN-ACK
                elif self.segment.is_syn_ack_flag():
                    self.log.alert_log(f'[!] Resending SYN-ACK to {self.server_ip}:{self.server_port}')
                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=self.segment)
                # Complete
                elif self.segment.is_ack_flag():
                    self.log.alert_log(f"[!] ACK received from {self.server_ip}:{self.server_port}")
                    break
                # Received a segment with no flag (file)
                else:
                    self.log.warning_log(f"[!] Received a segment with no flag (file), resetting connection...")
                    # Send SYN-ACK
                    self.segment = Segment()
                    self.segment.set_flag([True, True, False])
                    self.log.alert_log(f"[!] Sending SYN-ACK to {self.server_ip}:{self.server_port}")
                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=self.segment)
            except socket.timeout:
                if self.segment.is_syn_ack_flag():
                    self.log.warning_log("[!] [TIMEOUT] ACK Response Timed out, retrying...")
                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=self.segment)
                else:
                    self.log.warning_log("[!] [TIMEOUT] SYN Response Timed out")
            except Exception as e:
                self.log.warning_log(f"[!] Error: {e}")
                return

    def listen_file(self):
        N = WINDOW_SIZE
        Rn = 0
        Sn = 0
        METADATA_SEQ = -1

        # Terima file, pengulangan hingga file selesai
        while True:
            try:
                self.log.alert_log("Receiving file...")
                file_segment, _ = self.connection.listen()
                self.log.success_log("File received")
                Sn = file_segment.get_header()['seqNumber']
                self.log.alert_log(f"Receiving segment {Sn}")
                flag = file_segment.get_flag()

                # if in the last send FIN ACK and break

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
                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=ack)
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

                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=ack)
                    self.log.alert_log(f"Sending ACK {Sn}")
                else:
                    if (Rn - Sn >= N):
                        self.log.warning_log(f"Segment {Sn} is out of window, Resending ACK {Rn}")
                        self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=ack)
                    else:
                        self.log.warning_log(f'Segment {Sn} is refused, expected {Rn}')
                        ack = Segment()
                        ack.set_flag([False, True, False])
                        ack.set_ack_number(Rn)
                        self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=ack)
                        self.log.alert_log(f"Sending ACK {Rn}")
                        
            except socket.timeout:
                self.log.warning_log("[!] [TIMEOUT] Response Timed out, retrying...")

            except Exception as e:
                self.log.warning_log(e)
                break


def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-ci', '--clientip', type=str, default='localhost', help='ip the client is on')
    arg.add_argument('-cp', '--clientport', type=int, default=7331, help='port the client is on')
    arg.add_argument('-i', '--ip', type=str, default='localhost', help='ip to listen on')
    arg.add_argument('-p', '--port', type=int, default=1337, help='port to listen on')
    arg.add_argument('-f', '--folder', type=str, default='output', help='path to folder output')
    args = arg.parse_args()
    return args


if __name__ == "__main__":
    args = load_args()
    print(args.clientip, args.clientport)
    klien = Client(Connection(ip = args.clientip, port=args.clientport), server_ip=args.ip, server_port=args.port, folder_path=args.folder)
    klien.run()
