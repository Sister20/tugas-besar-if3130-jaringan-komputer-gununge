class GameManager:
    def __init__(self, p1, p2):
        self.gamestate = [["" for i in range(3)] for j in range(3)]
        self.playerInfo = [[p1[0],p1[1]],[p2[0],p2[1]]]
        self.turn = 1
        self.pemain = 1
        self.menang = False
        self.winner = 0 # 1 = p1, 2 = p2, 3 = draw

    def newTurn(self):
        if self.pemain == 1:
            self.pemain = 2
        else:
            self.pemain = 1
        self.turn += 1

    def setState(self, move: tuple):
        row = move[0]
        col = move[1]
        if self.pemain == 1:
            self.gamestate[row-1][col-1] = "X"
        else:
            self.gamestate[row-1][col-1] = "O"
    
    def validate(self):
        if(not self.menang and self.turn == 10):
            self.winner = 3
            self.menang = True
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