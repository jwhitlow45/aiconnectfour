from typing import List

ROW_SIZE = 5
COL_SIZE = 6
EMPTY = 'x'

class Board:
    
    def __init__(self, grid: List[List] = None) -> None:
        self.__grid: List[List]
        if not grid:
            # create empty board to play on if board state not provided
            self.__grid = [[EMPTY]*COL_SIZE for i in range(ROW_SIZE)]
        else:
            self.__grid = grid
        
    def printGrid(self) -> None:
        for i in range(ROW_SIZE):
            for j in range(COL_SIZE):
                print(self.__grid[i][j], end=' ')
            print('')
            
    def move(self, player: int, col: int) -> bool:
        for i in range(ROW_SIZE - 1, -1, -1):
            if self.__grid[i][col] == EMPTY:
                self.__grid[i][col] = str(player)
                return True
            
        return False