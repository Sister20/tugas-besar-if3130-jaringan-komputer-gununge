class GameState:
    def __init__(self, clientNumber,board):
        self.clientNumber = clientNumber
        self.board = board        

    def printBoard(self):
        for row in range (3):
            if row != 2:
                print(f"   {self.board[row][0]} | {self.board[row][1]} | {self.board[row][2]}   ")
                print("-------------")
            else:
                print(f"   {self.board[row][0]} | {self.board[row][1]} | {self.board[row][2]}   ")
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