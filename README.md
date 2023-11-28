# IF3130 - Jaringan Komputer 2023
> Tugas Besar - IF3130 Jaringan Komputer 2023

## About
This is a simple file transfer program using UDP protocol. The program is written in Python 3.10 and tested on Windows 11 and MacOS.

## Contributors
Kelompok 1 K03 - GunungE

| NIM | Nama |
| --- | --- |
| 13521004 | Henry Anand Septian Radityo (Manusia Rasis) |
| 13521007 | Matthew Mahendra (Si Bucin ke Bandung Mulu) |
| 13521015 | Hidayatullah Wildan Ghaly (Manusia Penggali) |
| 13521024 | Ahmad Nadil (yg paling homo bisex lgbt) |

![Kelompok 1 K03](input/penampakan.jpg)

## Features
### Main Features
- Reliable data transfer using UDP protocol and sliding window protocol
- Handle data transfer in bad network condition (Tested using Clumsy)

### Bonus Features
- Streaming process using Seek()
- Metadata transfer (file name and extension)
- Peer to Peer file transfer
- Parallel processing for handshake and data transfer in server
- Error Correcting Codes (ECC) using Hamming Code
- End to End device communication
- TicTacToe game using UDP protocol

## How to Run
1. Run the server
```bash
python server.py -i <server_ip> -p <server_port> -f <file_input_path>
```

2. Run the client
```bash
python client.py -ci <client_ip> -cp <client_port> -i <server_ip> -p <server_port> -f <file_output_path>
```

*There is default value for each argument, so you can run the program without any argument*

Alternatively, you can run the main program to switch between server and client mode
```bash
python main.py
```

## Folder Structure
```bash
┣ 📂.github
┃ ┗ 📜.keep
┣ 📂lib
┃ ┣ 📜__init__.py
┃ ┣ 📜Connection.py
┃ ┣ 📜Constant.py
┃ ┣ 📜Hamming.py
┃ ┣ 📜Logger.py
┃ ┣ 📜Node.py
┃ ┣ 📜Segment.py
┃ ┣ 📜SegmentFlag.py
┃ ┗ 📜Utils.py
┣ 📂output
┃ ┗ 📜.gitkeep
┣ 📜.gitignore
┣ 📜client.py
┣ 📜main.py
┣ 📜README.md
┗ 📜server.py
```

## References
- [Hamming Code](https://www.geeksforgeeks.org/hamming-code-implementation-in-python/)
- [CRC](https://www.geeksforgeeks.org/cyclic-redundancy-check-python/)
- [UDP Socket](https://www.geeksforgeeks.org/udp-server-client-implementation-c/)
