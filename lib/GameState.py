class GameState:
    def __init__(self, clientNumber,board):
        self.clientNumber = clientNumber
        self.board = board        

    def printBoard(self):
        row = self.board
        # fill the empty board with 3 blank spaces
        row = [[" " + cell + " " if cell != "" else "   " for cell in row[i]] for i in range(3)]

        print(row[0][0] + '|' + row[0][1] + '|' + row[0][2])
        print('---+---+---')
        print(row[1][0] + '|' + row[1][1] + '|' + row[1][2])
        print('---+---+---')
        print(row[2][0] + '|' + row[2][1] + '|' + row[2][2])
        
    def input_mark(self):
        row = int(input("Masukkan baris Anda "))
        col = int(input("Masukkan kolom Anda "))

        state = False
        while state == False:
            if str(row) == "" or str(col) =="":
                print("Input baris dan kolom tidak boleh kosong")
                row = int(input("Masukkan baris Anda "))
                col = int(input("Masukkan kolom Anda "))
            if (row > 3 or row <=0) or (col <=0 or col > 3):
                print("Input baris dan kolom salah! Baris dan kolom harus dalam rentang 1...3")
                row = int(input("Masukkan baris Anda "))
                col = int(input("Masukkan kolom Anda "))
            elif self.board[row-1][col-1] == "X" or self.board[row-1][col-1]=="O":
                print("Tempat itu sudah diisi")
                row = int(input("Masukkan baris Anda "))
                col = int(input("Masukkan kolom Anda "))
            else:
                state = True
        return row, col