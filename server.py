import argparse
import socket
import os
import threading
import time
from typing import Dict, List, Tuple

from lib import *

class Server(Node):
    def __init__(self, connection: Connection, file_path: str):
        self.log = Logger("Server")
        self.connection = connection
        self.segment = Segment()
        self.file_path = file_path
        self.file = open(self.file_path, 'rb').read()
        self.file_segment = breakdown_file(self.file)
        self.file_name, self.file_extension = os.path.splitext(os.path.basename(file_path))
        self.port_clients = []
        self.client_list = []
        self.parallel = False

        # prompt user for parallel mode
        while True:
            parallel = input(f'{"\033[93m"}[Server]{"\033[0m"} {"Turn on parallel mode? (y/n): "}')
            if parallel.lower() == 'y':
                self.parallel = True
                break
            elif parallel.lower() == 'n':
                self.parallel = False
                break
            else:
                self.log.warning_log("[!] Invalid prompt input")

    def run(self):
        while True:
            self.client_list = []
            self.listen_for_clients()
            if not self.parallel:
                self.start_connection()

    def listen_for_clients(self):
        while True:
            if (self.parallel):
                self.parallel_listen()
            else:
                try:
                    self.log.alert_log(f"[!] Broadcasting {self.file_name}{self.file_extension} to {self.connection.ip}:{self.connection.port}")
                    _, (client_ip, client_port) = self.connection.listen(TIMEOUT_LISTEN)
                    if (client_ip, client_port) not in self.client_list:
                        self.client_list.append((client_ip, client_port))
                    self.log.alert_log(f"[!] Client {client_ip}:{client_port} connected")
                    self.log.alert_log(f"[!] Total client connected: {len(self.client_list)}")
                    # input to listen for more clients
                    while True:
                        prompt = input(f'{"\033[93m"}[Server]{"\033[0m"} {"Listen for more clients? (y/n): "}')
                        if prompt.lower() == 'y':
                            break
                        elif prompt.lower() == 'n':
                            return
                        else:
                            self.log.warning_log("[!] Invalid prompt input")
                except socket.timeout:
                    self.log.alert_log("[!] Timeout, no more clients connected")
                    return
                except Exception as e:
                    self.log.warning_log(f"[!] Error: {e}")
                    exit()

    def connection_handler(self, ip: str, port: int):
        self.three_way_handshake(ip_client=ip, port_client=port)
        self.send_file(ip_client=ip, port_client=port)

    def parallel_listen(self):
        self.parallel_client_list: Dict[Tuple[str, int], List[Segment]] = {}
        while True:
            try:
                self.log.alert_log(f"[!] Listening for clients on {self.connection.ip}:{self.connection.port}")
                msg, addr = self.connection.listen(TIMEOUT_LISTEN)
                if addr not in self.parallel_client_list: # Make sure client is not already connected
                    self.log.alert_log(f"[!] Client {addr[0]}:{addr[1]} connected")
                    self.log.alert_log(f"[!] Total client connected: {len(self.parallel_client_list) + 1}")
                    self.parallel_client_list[addr] = []
                    process = threading.Thread(target=self.start_connection, kwargs={'ip': addr[0], 'port': addr[1]})
                    process.start()
                else: # If client is already connected, append message to client's message list
                    self.parallel_client_list[addr].append(msg)
                    
            except socket.timeout:
                self.log.alert_log("[!] Timeout, no more clients connected")
                break
            except Exception as e:
                self.log.warning_log(f"[!] Error: {e}")
                break
    
    def get_response(self, ip_client: str, port_client: int):
        if (self.parallel):
            timeout = time.time() + 1
            while True:
                if time.time() > timeout:
                    raise socket.timeout
                if len(self.parallel_client_list[(ip_client, port_client)]) > 0:
                    return self.parallel_client_list[(ip_client, port_client)].pop(0), (ip_client, port_client)
        else:
            return self.connection.listen(TIMEOUT_TIME)

    def start_connection(self, ip: str = None, port: int = None):
        if not self.parallel:
            for client in self.client_list:
                self.three_way_handshake(ip_client=client[0], port_client=client[1])
                self.send_file(ip_client=client[0], port_client=client[1])
        else:
            self.three_way_handshake(ip_client=ip, port_client=port)
            self.send_file(ip_client=ip, port_client=port)

    def three_way_handshake(self, ip_client: str, port_client: int):
        self.log.alert_log(f"[!] Starting 3-way handshake with {ip_client}:{port_client}")
        self.segment.set_flag([True, False, False])
        while True:
            # Send SYN
            if self.segment.is_syn_flag():
                self.log.alert_log(f"[!] Sending SYN to {ip_client}:{port_client}")
                self.connection.send(ip_remote=ip_client, port_remote=port_client, message=self.segment)

                try:
                    msg, _ = self.get_response(ip_client, port_client)
                    self.segment = msg

                except socket.timeout:
                    self.log.warning_log("[!] [TIMEOUT] SYN Timed out, retrying...")
            # Send ACK
            elif self.segment.is_syn_ack_flag():
                self.log.alert_log(f"[!] SYN-ACK received from {ip_client}:{port_client}")
                self.log.alert_log(f"[!] Sending ACK to {ip_client}:{port_client}")
                self.segment = Segment()
                self.segment.set_flag([False, True, False])
                self.connection.send(ip_remote=ip_client, port_remote=port_client, message=self.segment)
                break
            else:
                self.log.warning_log("[!] Not SYN or SYN-ACK, client already connected")
                break
        self.log.success_log(f"[!] 3-way handshake with {ip_client}:{port_client} complete")

    # KIRIM FILE
    def send_file(self, ip_client: str, port_client: int):
        # INISIALISASI SEGMENT
        N = WINDOW_SIZE
        Rn = 0
        Sb = 0
        Sm = N - 1
        SegmentCount = len(self.file_segment)
        self.log.alert_log(f"[!] Segment count: {SegmentCount}")
        isMetaData = True
        METADATA_SEQ = -1

        while True:
            if (isMetaData):
                segment = Segment()
                segment.set_seq_number(METADATA_SEQ)
                segment.set_data(self.file_name.encode() + self.file_extension.encode())
                self.connection.send(ip_client, port_client, segment)
                self.log.alert_log(f"[!] Sending Metadata to {ip_client}:{port_client}")
                isMetaData = False
            else:
                while (Sb <= Rn <= Sm and Rn < SegmentCount):
                    segment = Segment()
                    segment.set_seq_number(Rn)
                    if Rn >= len(self.file_segment):
                        break
                    segment.set_data(self.file_segment[Rn])
                    self.connection.send(ip_client, port_client, segment)
                    self.log.alert_log(f"[!] Sending segment {Rn}/{SegmentCount - 1} to {ip_client}:{port_client}")
                    Rn += 1
            try:
                msg, addr = self.connection.listen()
                if msg.is_syn_ack_flag():
                    # Reset connection
                    try:
                        self.log.warning_log(f'[!] Resetting connection with {ip_client}:{port_client}')
                        self.three_way_handshake(ip_client, port_client)
                        self.send_file(ip_client, port_client)
                    except Exception as e:
                        self.log.warning_log(f"[!] Error: {e}")
                    return
                if addr != (ip_client, port_client):
                    # if the address haven't been registered in the client list, register it and start connection
                    if addr not in self.parallel_client_list:
                        self.log.alert_log(f"[!] Client {addr[0]}:{addr[1]} connected")
                        self.parallel_client_list[addr] = []
                        process = threading.Thread(target=self.start_connection, kwargs={'ip': addr[0], 'port': addr[1]})
                        process.start()
                    else: 
                        self.log.warning_log(f"[!] Received message from unknown address {addr}, ignoring...")
                    continue
                ack_number = msg.get_header()['ackNumber']
                self.log.success_log(f"[!] ACK {ack_number} received from {ip_client}:{port_client}")
                if ack_number >= SegmentCount - 1:
                    self.close_connection(ip_client, port_client)
                    return
                Sb = ack_number
                Sm = Sb + (N - 1)
            except socket.timeout:
                Rn = Sb
                self.log.warning_log(f"[!] [TIMEOUT] ACK Response Timed out with {ip_client}:{port_client}")
            except Exception as e:
                self.log.warning_log(f"[!] Error: {e}")
                return

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
                bendera_fin = fin.get_flag()
                if bendera_fin.fin and bendera_fin.ack:
                    self.log.success_log(f"[!] FIN ACK received from {ip_client}:{port_client}")
                    break
                else:
                    self.log.warning_log("[!] Not FIN ACK")
            except Exception as e:
                self.log.warning_log("[!] Connection timed out while waiting for FIN ACK")
                break
        # Tutup koneksi
        if (self.parallel):
            self.parallel_client_list.pop((ip_client, port_client))
        self.log.success_log(f'Connection with {ip_client}:{port_client} closed')


def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-i', '--ip', type=str, default='localhost', help='ip to listen on')
    arg.add_argument('-p', '--port', type=int, default=1337, help='port to listen on')
    arg.add_argument('-f', '--file', type=str, default='input.txt', help='path to file input')
    arg.add_argument('-par', '--parallel', type=int, default=0, help='turn on/off parallel mode')
    args = arg.parse_args()
    return args


if __name__ == '__main__':
    while True:
        args = load_args()
        server = Server(Connection(ip=args.ip, port=args.port),file_path=args.file)
        server.run()
