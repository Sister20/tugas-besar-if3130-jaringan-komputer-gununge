import argparse

def load_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('-p', '--port', type=int, default=5000, help='port to listen on')
    arg.add_argument('-f', '--file', type=str, default='input.txt', help='path to file input')
    arg.add_argument('-par', '--parallel', type=int, default=0, help='turn on/off parallel mode')
    args = arg.parse_args()
    return args

def main():
    args = load_args()
    print(args)

if __name__ == '__main__':
    main()
