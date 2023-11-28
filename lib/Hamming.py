import struct
from .Logger import *
from concurrent.futures import ThreadPoolExecutor

class Hamming:

    def __init__(self) -> None:
        self.log = Logger("Hamming")

    def calcRedundantBits(self, m):
        for i in range(m):
            if(2**i >= m + i + 1):
                return i

    def posRedundantBits(self, data, r):
        # asumsi r = 3
        return ((data & 0b1110) << 3) | ((data & 0b0001) << 2)

    def calcParityBits(self, data, r):
        p1 = ((data >> 2) & 1) ^ ((data >> 4) & 1) ^ ((data >> 6) & 1)
        p2 = ((data >> 1) & 2) ^ ((data >> 4) & 2) ^ ((data >> 5) & 2)
        p3 = ((data >> 1) & 8) ^ ((data >> 2) & 8) ^ ((data >> 3) & 8)
        p4 = 128
        return data | p1 | p2 | p3 | p4
        
    def removeParityBits(self, binary_number, bit_length):
        """Remove bits 0, 1, and 3 from a binary number."""
        
        binary_number = binary_number & 0b01111111
        
        result = 0
        shift = 0

        for i in range(bit_length):
            if i in [0, 1, 3]:
                continue
            current_bit = (binary_number >> i) & 1
            result |= current_bit << shift
            shift += 1
        return result

    def detectError(self, binErr, nr):
        n = binErr.bit_length()
        res = 0
        for i in range(nr):
            val = 0
            for j in range(1, n + 1):
                if j & (1 << i):
                    val ^= (binErr >> (j-1)) & 1
            res += val * (1 << i)
        return res

    def int_to_4bit_chunks(self, num):
        binary = bin(num)[2:]
        if len(binary) % 4:
            binary = binary.zfill(len(binary) + 4 - (len(binary) % 4))
        return [int(binary[i:i+4], 2) for i in range(0, len(binary), 4)]

    def breakdownData(self, data):
        if isinstance(data, int):
            return self.int_to_4bit_chunks(data)
        elif isinstance(data, str):
            return [chunk for char in data for chunk in self.int_to_4bit_chunks(ord(char))]
        elif isinstance(data, bytes):        
            return [
                self.calcParityBits(self.posRedundantBits(chunk, 3), 3) 
                # chunk
                for b in data for chunk in self.int_to_4bit_chunks(b)
            ]
        else:
            raise TypeError("Unsupported data type")

    def breakdownDataToBytes(self, data):
        if not isinstance(data, bytes):
            raise TypeError("Unsupported data type")

        result = b''
        for byte in data:
            high_nibble = byte >> 4
            low_nibble = byte & 0x0F

            encoded_high = self.hammingEncode(high_nibble)
            encoded_low = self.hammingEncode(low_nibble)

            result += struct.pack('B', encoded_high)
            result += struct.pack('B', encoded_low)

        return result


    def hammingEncode(self, data, r:int = 3):
        return self.calcParityBits(self.posRedundantBits(data, r), r)

    def hammingRecovery(self, data, r:int = 3):
        correction = self.detectError(data, r)
        finalResult = data
        if correction != 0:
            bit_position_to_flip =  correction - 1
            finalResult = data ^ (1 << bit_position_to_flip)
            self.log.warning_log(f"Error detected at bit position {bit_position_to_flip}")
            
        res = self.removeParityBits(finalResult, 7)
        return res

    def hammingDecode(self, data, r:int = 3):
        return self.hammingRecovery(data, r)

    def breakdownBytes(self, data):
        final = b''
        if len(data) % 2 != 0:
            raise ValueError("Panjang data harus genap untuk dekode Hamming 4-bit.")

        for i in range(0, len(data), 2):
            byte1, byte2 = data[i], data[i + 1]
            bin_value1 = format(byte1, '08b')
            bin_value2 = format(byte2, '08b')
            decoded_value1 = self.hammingDecode(int(bin_value1, 2))
            decoded_value2 = self.hammingDecode(int(bin_value2, 2))
            combined_byte = (decoded_value1 << 4) | decoded_value2
            final += struct.pack('B', combined_byte)
        
        return final
    

if __name__ == "__main__":
    with open("test.txt", 'rb') as file:
        file_content = file.read()
        
        hamming = Hamming()
        
        # example encode
        splitData = hamming.breakdownDataToBytes(file_content)
        print(splitData)
        
        # example decode
        finals = hamming.breakdownBytes(splitData)
        print(finals)
    