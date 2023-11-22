# Constant Values
SYN_FLAG = 0x02
ACK_FLAG = 0x08
FIN_FLAG = 0x01
DEFAULT_FLAG = 0x00

class SegmentFlag:
    def __init__(self, flag: bytes) -> None:
        # Flag init
        self.syn = False
        self.ack = False
        self.fin = False

        # Init flag from flag variable
        if flag & SYN_FLAG:
            self.syn = True
        if flag & ACK_FLAG:
            self.ack = True
        if flag & FIN_FLAG:
            self.fin = True

    def get_flag_bytes(self) -> bytes:
        flag = DEFAULT_FLAG
        if self.syn:
            flag |= SYN_FLAG
        if self.ack:
            flag |= ACK_FLAG
        if self.fin:
            flag |= FIN_FLAG

        return flag
