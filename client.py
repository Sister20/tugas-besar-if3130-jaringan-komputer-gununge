import argparse

def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-c', '--client', type=int, default=8000, help='port the client is on')
    arg.add_argument('-p', '--port', type=int, default=8080, help='port to listen on')
    arg.add_argument('-f', '--file', type=str, default='input.txt', help='path to file input')
    args = arg.parse_args()
    return args

def main():
    args = load_args()
    print(args)

if __name__ == '__main__':
    main()
