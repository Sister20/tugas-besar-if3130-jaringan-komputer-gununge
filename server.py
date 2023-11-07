import argparse
import socket

def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-p', '--port', type=int, default=5000, help='port to listen on')
    arg.add_argument('-f', '--file', type=str, default='input.txt', help='path to file input')
    arg.add_argument('-par', '--parallel', type=int, default=0, help='turn on/off parallel mode')
    args = arg.parse_args()
    return args

def listen(port):
    # create a socket object and connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)
    print('Listening on port', port)
    return s

def main():
    args = load_args()
    print(args)

    s = listen(args.port)
    while True:
        # establish connection with client
        c, addr = s.accept()
        print('Got connection from', addr)
        # receive data from client
        data = c.recv(1024)
        print('Received', repr(data))
        # send data to client
        c.send(data)
        # close the connection
        c.close()

if __name__ == '__main__':
    main()
