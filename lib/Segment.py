import struct
from .Constant import *
from .SegmentFlag import *

class Segment:
    # -- Internal Function --
    def __init__(self):
        # Initalize segment
        self.header = {}
        self.header['seqNumber']        = 0
        self.header['ackNumber']        = 0
        self.header['flag']             = DEFAULT_FLAG
        # self.header['emptyPadding']     = 0
        self.header['checksum']         = 0
        
        self.data                       = b"" # apa ini kak? payload tapi isinya apa?

    def __str__(self):
        # Optional, override this method for easier print(segmentA)
        output = ""
        output += f"{'Sequence number':24} | {self.header['seqNumber']}\n"
        output += f"{'Acknowledgement number':24} | {self.header['ackNumber']}\n"
        output += f"{'Checksum':24} | {self.header['checksum']}\n"
        output += f"{'Flag':24} | {self.header['flag']}\n"
        output += f"{'Payload':24} | {self.data}\n"
        return output

    # -- Setter --
    def set_header(self, header : dict):
        # Set header from dictionary
        self.header = header
        self.update_checksum()

    def set_data(self, data : bytes):
        # Set payload from bytes
        self.data = data
        self.update_checksum()
    
    def set_seq_number(self, seq_number : int):
        # Set sequence number
        self.header['seqNumber'] = seq_number
        self.update_checksum()
    
    def set_ack_number(self, ack_number : int):
        # Set acknowledgement number
        self.header['ackNumber'] = ack_number
        self.update_checksum()

    def set_flag(self, flag_list : list):
        # Set flag from list of flag (SYN, ACK, FIN)
        initial_flag = DEFAULT_FLAG
        if flag_list[0]:
            initial_flag |= SYN_FLAG
        if flag_list[1]:
            initial_flag |= ACK_FLAG
        if flag_list[2]:
            initial_flag |= FIN_FLAG
        self.header['flag'] = initial_flag
        self.update_checksum()


    # -- Getter --
    def get_flag(self) -> SegmentFlag:
        # return flag in segmentflag
        return SegmentFlag(self.header['flag'])

    def get_header(self) -> dict:
        # Return header in dictionary form
        return self.header

    def get_data(self) -> bytes:
        # Return payload in bytes
        return self.data

    # -- Marshalling --
    def set_from_bytes(self, src : bytes):
        # From pure bytes, unpack() and set into python variable
        # 44112: iibbh
        header_bytes = src[:12]
        header_tup = struct.unpack('iibbh', header_bytes)
        header = {
            'seqNumber': header_tup[0],
            'ackNumber': header_tup[1],
            'flag': header_tup[2],
            'checksum': header_tup[4]
        }
        self.header = header
        self.data = src[12:]
        self.update_checksum()

    def get_bytes(self) -> bytes:
        # Convert this object to pure bytes
        print(self.header)
        header_bytes = struct.pack('iibbH', self.header['seqNumber'], self.header['ackNumber'], self.header['flag'], self.header['checksum'], DEFAULT_FLAG)
        return header_bytes + self.data

    def get_bytes_no_checksum(self) -> bytes:
        # Get bytes without checksum
        header_bytes = struct.pack('iibb', self.header['seqNumber'], self.header['ackNumber'], self.header['flag'], DEFAULT_FLAG)
        print(header_bytes)
        return header_bytes + self.data

    # -- Checksum --
    def valid_checksum(self) -> bool:
        # Use __calculate_checksum() and check integrity of this object
        return self.calculate_checksum() == self.header['checksum']
    
    def calculate_checksum(self) -> int:
        # Calculate checksum here, return checksum result
        sum = 0
        data_bytes = self.get_bytes_no_checksum()

        if (len(data_bytes) % 2 != 0):
            data_bytes = b'\x00' + data_bytes
            
        for i in range(0, len(data_bytes), 2):
            sum += int.from_bytes(data_bytes[i:i+2], byteorder='big')
        while sum >> 16:
            sum = (sum & 0xffff) + (sum >> 16)
        return ~sum & 0xffff

    def update_checksum(self):
        # Update checksum value
        self.header['checksum'] = self.calculate_checksum()
        
if __name__ == '__main__':
    segment = Segment()
    segment.header['seqNumber'] = 1
    segment.header['ackNumber'] = 2
    segment.header['flag'] = SYN_FLAG
    segment.data = b"Hello World"
    segment.update_checksum()
    print(segment.calculate_checksum())
    if segment.valid_checksum():
        print("Checksum valid")
    else:
        print("Checksum invalid")
    print(segment.get_bytes_no_checksum().hex())
    print(segment.get_bytes().hex())