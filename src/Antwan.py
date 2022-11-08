from typing import List
from copy import deepcopy

from src.Board import Board, ROW_SIZE, COL_SIZE, BOT_PIECE, EMPTY
from src.Node import Node

def getScore(node: Node):
    
    print(node)
    if node.state.checkWin(node.lastMove):
        score = (ROW_SIZE * COL_SIZE - node.depth) // 2
        # get top row of current column
        row: int
        for row in range(COL_SIZE - 1, -1, -1):
            if node.state.getGrid()[row][node.lastMove] == EMPTY:
                row += 1
                break
            
        if node.state.getGrid()[row][node.lastMove] == BOT_PIECE:
            node.score = score
            return node.score
        else:
            node.score = score * -1
            return node.score
    if node.depth == ROW_SIZE * COL_SIZE:
        node.score = 0
        return node.score
        
    node.expand(node.piece)
    for child in node.children:
        getScore(child)
        
