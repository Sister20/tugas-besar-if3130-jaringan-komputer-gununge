# Constant Values
SYN_FLAG = 0x02
ACK_FLAG = 0x08
FIN_FLAG = 0x01
DEFAULT_FLAG = 0x00

class SegmentFlag:
    def __init__(self, flag: bytes) -> None:
        # Flag init
        self.syn = True if flag & SYN_FLAG else False
        self.ack = True if flag & ACK_FLAG else False
        self.fin = True if flag & FIN_FLAG else False

    def get_flag_bytes(self) -> bytes:
        # Return flag bytes
        flag = DEFAULT_FLAG
        flag |= (SYN_FLAG if self.syn else DEFAULT_FLAG)
        flag |= (ACK_FLAG if self.ack else DEFAULT_FLAG)
        flag |= (FIN_FLAG if self.fin else DEFAULT_FLAG)
        return flag
