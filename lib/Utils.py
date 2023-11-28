from .Constant import *
from .Hamming import *

def breakdown_file(data: bytes) -> list:
    list_data = []
    hamming = Hamming()
    halfPayload = PAYLOAD_SIZE // 2
    
    while (len(data) > 0):
        if (len(data)) > halfPayload:
            encodedData = hamming.breakdownDataToBytes(data[:halfPayload])
            
            list_data.append(encodedData)
            data = data[halfPayload:]
        else:
            encodedData = hamming.breakdownDataToBytes(data)
            list_data.append(encodedData)
            data = b''
    return list_data

def merge_file(list_data: list) -> bytes:
    data = b''
    for i in list_data:
        data += i
    return data

def encode_metadata(data: bytes) -> bytes:
    hamming = Hamming()
    encodedData = hamming.breakdownDataToBytes(data)
    return encodedData

def decode_metadata(data: bytes) -> bytes:
    hamming = Hamming()
    decodedData = hamming.breakdownBytes(data)
    return decodedData