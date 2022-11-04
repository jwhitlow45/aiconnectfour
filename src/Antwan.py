from typing import List
from copy import deepcopy

from src.Board import Board, ROW_SIZE
from src.Node import Node

class Antwan:
    
    def dfs():
        pass
        
    def expand(self, boardState: Board, symbol: int, winScore: int) -> Node:
        grid = [
            ['x','x','x','x','x','x'],
            ['x','x','x','x','0','x'],
            ['x','x','x','x','0','x'],
            ['x','x','x','x','0','x'],
            ['x','x','x','x','1','x']
        ]
        
        boardState = Board(grid)
        
        tempStates = [Board(deepcopy(boardState.getGrid())) for i in range(ROW_SIZE)]
        expandedStates = [tempStates[i] for i in range(ROW_SIZE) if tempStates[i].move(symbol, i)]
        
        isWin: bool = False
        for state in expandedStates:
            if state.checkWin():
                if winScore == 1:
                    isWin = True
                elif winScore == -1:
                    return None
        
        # return node with score 1 if win is possible
        if isWin:
            return Node(expandedStates, 1)
        return Node(expandedStates, 0)
            
            
                