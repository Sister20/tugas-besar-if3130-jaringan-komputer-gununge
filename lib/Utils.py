from .Constant import *


def breakdown_file(data: bytes) -> list:
    list_data = []
    while (len(data) > 0):
        if (len(data)) > PAYLOAD_SIZE:
            list_data.append(data[:PAYLOAD_SIZE])
            data = data[PAYLOAD_SIZE:]
        else:
            list_data.append(data)
            data = b''
    print("Breakdown file done")
    return list_data

def merge_file(list_data: list) -> bytes:
    data = b''
    for i in list_data:
        data += i
    return data