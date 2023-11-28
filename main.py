# make a caller for server or client
import os
from server import Server
from client import Client
from lib import *


if __name__ == '__main__':
    while True:
        print("1. Server")
        print("2. Client")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            input_file = input("Enter file name: ")
            ip = input("Enter ip: ")
            port = input("Enter port: ")
            # paralel = int(input("Enter paralel: "))
            if (not os.path.isfile(input_file)):
                print("File not found")
                continue
            if (input_file == ''):
                print("File name cannot be empty")
                continue
            if (ip == ''):
                ip = 'localhost'
            if (port == ''):
                port = 8080
            server = Server(Connection(ip=ip, port=int(port)),file_path=input_file)
            server.run()
        elif choice == '2':
            client_ip = input("Enter client ip: ")
            if (client_ip == ''):
                client_ip = 'localhost'
            client_port = input("Enter client port: ")
            if (client_port == ''):
                client_port = 6000
            ip = input("Enter ip server: ")
            if (ip == ''):
                ip = 'localhost'
            port = input("Enter port: ")
            if (port == ''):
                port = 8080
            folder = input("Enter folder: ")
            if (folder == ''):
                folder = 'output'
            client = Client(Connection(ip=client_ip, port=int(client_port)), server_ip=ip, server_port=int(port), folder_path=folder)
            client.run()
        elif choice == '3':
            break
        else:
            print("Invalid choice")