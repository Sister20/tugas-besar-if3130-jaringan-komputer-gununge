import argparse
import json
import socket

from lib import *
from lib.GameState import GameState


class Client(Node):
    def __init__(self, connection: Connection, server_ip: str, server_port: str, folder_path: str = None):
        self.connection = connection
        self.server_ip = server_ip
        self.server_port = server_port
        self.folder_path = folder_path
        self.file_path = None
        self.file = []
        self.log = Logger("Client")
        self.buffer_size = 1024
        self.segment = Segment()
        self.gameState = None

    def run(self):
        self.three_way_handshake()
        self.listen_file()

    def run_game(self):
        self.three_way_handshake()
        while True : 
            # listen for client number
            client_number, _ = self.connection.listen()
            self.log.success_log(f"Received segment {client_number.get_header()['seqNumber']} from {self.server_ip}:{self.server_port} with data {client_number.get_data().decode()}")
            break
        # initialize game state
        while True : 
            try:
                board, _ = self.connection.listen(TIMEOUT_LISTEN)
                self.gameState = GameState(client_number.get_data().decode(), json.loads(board.get_data().decode()))
                break
            except socket.timeout:
                self.log.warning_log("[!] [TIMEOUT] Response Timed out, retrying...")
                continue
        if (self.gameState.clientNumber == "2"):
            self.gameState.printBoard()
        while True:
            try:
                board, _ = self.connection.listen(TIMEOUT_LISTEN)
                if(not board.is_fin_flag()):
                    self.log.success_log(f"[!] Your turn")
                    self.gameState.board = json.loads(board.get_data().decode())
                    self.gameState.printBoard()

                    # input mark
                    move = self.gameState.input_mark()
                    seg = Segment()
                    seg.set_data(json.dumps(move).encode())
                    self.connection.send(self.server_ip, self.server_port, seg)
                    # listen for board
                    board, _ = self.connection.listen(TIMEOUT_LISTEN)
                    self.gameState.board = json.loads(board.get_data().decode())
                    self.log.success_log("[!] Board Updated")
                    self.gameState.printBoard()
                    self.log.alert_log("[!] Waiting for opponent...")
                else:
                    # PRINT THE MESSAGE
                    print(board.get_data().decode())
                    break
            except socket.timeout:
                self.log.warning_log("[!] [TIMEOUT] Response Timed out, retrying...")
                continue
            # except Exception as e:
            #     self.log.warning_log(e)
            #     break


        
        # Game

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
        hamming = Hamming()

        # Terima file, pengulangan hingga file selesai
        while True:
            try:
                file_segment, _ = self.connection.listen()
                Sn = file_segment.get_header()['seqNumber']
                self.log.success_log(f"Received segment {Sn} from {self.server_ip}:{self.server_port}")
                flag = file_segment.get_flag()

                # if in the last send FIN ACK and break

                if (Sn == METADATA_SEQ):
                    self.file_path = (Utils.decode_metadata(file_segment.get_data())).decode('UTF-8')
                    self.log.success_log(f"[!] Receiving file {self.file_path}")
                    ack = Segment()
                    ack.set_flag([False, True, False])
                    ack.set_ack_number(Sn)
                    self.log.alert_log(f"[!] Sending metadata ACK to {self.server_ip}:{self.server_port}")
                    self.connection.send(self.server_ip, self.server_port, ack)
                    METADATA_SEQ -= 1
                    continue

                # Jika FIN, maka kirim FIN ACK
                elif flag.fin:
                    self.log.success_log(f"[!] FIN received from {self.server_ip}:{self.server_port}")
                    # ack ke server
                    ack = Segment()
                    ack.set_flag([False, True, True])
                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=ack)
                    self.log.alert_log(f"[!] Sending ACK FIN to {self.server_ip}:{self.server_port}") 
                    filePath = self.folder_path + '/' + self.file_path
                    md5 = Utils.printmd5(filePath)
                    self.log.success_log(f"MD5 Hash: {md5}")
                    break

                elif Sn == Rn:
                    data = file_segment.get_data()
                    if data:
                        decodedData = hamming.breakdownBytes(data)
                        file = open(self.folder_path + '/' +
                                    self.file_path, 'ab')
                        file.seek(Sn)
                        file.write(decodedData)
                        file.close()
                        Rn += 1

                    # Kirim ACK
                    ack = Segment()
                    ack.set_flag([False, True, False])
                    ack.set_ack_number(Sn)

                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=ack)
                    self.log.alert_log(f"[!] Sending ACK {Sn} to {self.server_ip}:{self.server_port}")
                else:
                    self.log.warning_log(f'[!] Segment {Sn} is refused, expected {Rn}, timing out...')
                    self.connection.send(ip_remote=self.server_ip, port_remote=self.server_port, message=ack)
                        
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
    arg.add_argument('-g', '--game', type=str, default='0', help='turn on or off game')
    args = arg.parse_args()
    return args


if __name__ == "__main__":
    args = load_args()
    print(args.clientip, args.clientport)
    if args.game == '0':
        klien = Client(Connection(ip = args.clientip, port=args.clientport), server_ip=args.ip, server_port=args.port, folder_path=args.folder)
        klien.run()
    else : 
        klien = Client(Connection(ip = args.clientip, port=args.clientport), server_ip=args.ip, server_port=args.port)
        klien.run_game()
