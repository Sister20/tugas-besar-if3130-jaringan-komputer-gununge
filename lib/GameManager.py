class GameManager:
    def __init__(self, p1, p2):
        self.gamestate = [["" for i in range(3)] for j in range(3)]
        self.playerInfo = [[p1[0],p1[1]],[p2[0],p2[1]]]
        self.turn = 1
        self.pemain = 1
        self.menang = False
        self.winner = 0 # 1 = p1, 2 = p2, 3 = draw

    def newTurn(self):
        self.turn += 1

    def setState(self):
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
            elif self.gamestate[row-1][col-1] == "X" or self.gamestate[row-1][col-1]=="O":
                print("Tempat itu sudah diisi")
                row = int(input("Masukkan baris Anda "))
                col = int(input("Masukkan kolom Anda "))
            else:
                state = True
        
        if self.turn == 1:
            self.gamestate[row-1][col-1] = "X"
        else:
            self.gamestate[row-1][col-1] = "O"

        return
    
    def validate(self):
        if(self.turn == 10 and not self.menang and self.winner == 0):
            self.winner = 3
        else:
            #cek jawaban untuk pemain 1
            for i in range(3): #cek untuk setiap baris
                if (self.gamestate[i][0] == "X" and self.gamestate[i][1] == "X" and self.gamestate[i][2] == "X"):
                    self.turn = 10
                    self.menang = True
                    self.winner = 1
            for i in range(3): #cek untuk setiap kolom
                if (self.gamestate[0][i] == "X" and self.gamestate[1][i]=="X" and self.gamestate[2][i]=="X"):
                    self.turn = 10
                    self.menang = True
                    self.winner = 1
            if (self.gamestate[0][0] == "X" and self.gamestate[1][1] == "X" and self.gamestate[2][2] == "X") or (self.gamestate[2][0] == "X" and self.gamestate[1][1] == "X" and self.gamestate[0][2] == "X"): #cek untuk menyilang
                self.turn = 10
                self.menang = True
                self.winner = 1

            #cek jawaban untuk pemain 2
            for i in range(3):#cek untuk setiap baris
                if (self.gamestate[i][0] == "O" and self.gamestate[i][1] == "O" and self.gamestate[i][2] == "O"):
                    self.turn = 10
                    self.menang = True
                    self.winner = 2
            for i in range(3):#cek untuk setiap kolom
                if (self.gamestate[0][i] == "O" and self.gamestate[1][i]=="O" and self.gamestate[2][i]=="O"):
                    self.turn = 10
                    self.menang = True
                    self.winner = 2
            if (self.gamestate[0][0] == "O" and self.gamestate[1][1] == "O" and self.gamestate[2][2] == "O") or (self.gamestate[2][0] == "O" and self.gamestate[1][1] == "O" and self.gamestate[0][2] == "O"): #cek untuk menyilang
                self.turn = 10
                self.menang = True
                self.winner = 2