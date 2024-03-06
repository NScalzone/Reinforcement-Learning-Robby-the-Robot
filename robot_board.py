from random import randint
class Square:
    def __init__(self, x, y, has_can, has_robby):
        self.x = x
        self.y = y
        self.has_can = False
        self.has_robby = False

    def setCan(self):
        canDice = randint(0, 1)
        if canDice == 1:
            self.has_can = True
        else:
            self.has_can = False

    def setRobby(self):
        self.has_robby = True
        
            
    def displaySquare(self):
        if self.has_can and self.has_robby:
            return "RC"
        elif self.has_can:
            return "C"
        elif self.has_robby:
            return "R"
        else:
            return "O"

class GridWorld:
    def __init__(self, rows, cols, robby_row, robby_col):
        self.rows = rows
        self.cols = cols
        self.robby_row = robby_row
        self.robby_col = robby_col
        self.board = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            for j in range(cols):
                self.board[i][j] = Square(i, j, False, False)
                self.board[i][j].setCan()
        self.start_robby(self.robby_row, self.robby_col)

    def display_grid_world(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.board[i][j].displaySquare(), ' ', end = "")
            print()
            
    def start_robby(self, robby_row, robby_col):
        self.board[robby_row][robby_col].setRobby()
        
    def moveRobby(self, new_row, new_col):
        if new_row < 0 or new_row >= self.rows or new_col < 0 or new_col >= self.cols:
            return False
        else:
            self.board[self.robby_row][self.robby_col].has_robby = False
            self.robby_row = new_row
            self.robby_col = new_col
            self.board[self.robby_row][self.robby_col].has_robby = True
            return True
       
