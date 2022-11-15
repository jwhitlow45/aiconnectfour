from typing import List, Tuple

ROW_SIZE = 7
COL_SIZE = 6
P1_PIECE = 1
P2_PIECE = 2
EMPTY = 0

class Board:
    
    def __init__(self, grid: List[List] = None) -> None:
        self.__grid = grid
       
    def __repr__(self) -> None:
        outstr: str = '\n'
        for i in range(COL_SIZE):
            for j in range(ROW_SIZE):
                outstr += str(int(self.__grid[i][j])) + ' '
            outstr += '\n'
        outstr += '0 1 2 3 4 5 6\n'
        return outstr
         
    def getGrid(self) -> List[List]:
        return self.__grid
    
    def countEmpty(self) -> int:
        empties = 0
        for i in range(COL_SIZE):
            for j in range(ROW_SIZE):
                if self.__grid[i][j] == EMPTY:
                    empties += 1
        return empties
            
    def move(self, player: int, col: int) -> bool:
        for i in range(COL_SIZE - 1, -1, -1):
            if self.__grid[i][col] == EMPTY:
                self.__grid[i][col] = player
                return True
            
        return False
    
    def isInBounds(self, row: int, col: int) -> bool:
        return not (row < 0 or col < 0 or row >= COL_SIZE or col >= ROW_SIZE)
    
    def isWin(self, col: int) -> Tuple[bool, int]:
        # get top row of current column
        i: int
        for i in range(COL_SIZE - 1, -1, -1):
            if self.__grid[i][col] == EMPTY:
                i += 1
                break
        
        # out of bound value will be returned if column is empty, in this case
        # we can just return false as there are no tiles in the current column
        if i >= COL_SIZE:
            return (False, None)
        
        # check every direction for player win
        moves: List[List] = [[0,1], [1,0], [1,1], [1,-1]]
        player: str = self.__grid[i][col]
        
        for move in moves:
            count: int = 1
            
            # check in one direction for win, then opposite direction while
            # tracking the number of tiles for current player
            for dir in [-1,1]:
                rowcur: int = i
                colcur: int = col
                rowdir: int = move[0] * dir
                coldir: int = move[1] * dir
                
                while self.isInBounds(rowcur + rowdir, colcur + coldir):
                    rowcur += rowdir
                    colcur += coldir
                    
                    if self.__grid[rowcur][colcur] == player:
                        count += 1
                    else:
                        break
                    
            if count >= 4:
                return (True, player)
            
        return (False, None)
         