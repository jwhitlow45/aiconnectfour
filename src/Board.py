ROW_SIZE = 5
COL_SIZE = 6

class Board:
    
    def __init__(self):
        self.__grid = [['0']*COL_SIZE for i in range(ROW_SIZE)]
        
        self.__grid[0][0] = '1'
        self.__grid[0][1] = '1'
        self.printGrid()
        
    def printGrid(self):
        for i in range(ROW_SIZE):
            for j in range(COL_SIZE):
                print(self.__grid[i][j], end=' ')
            print('')