from typing import List
from copy import deepcopy

from src.Board import Board, ROW_SIZE, COL_SIZE, BOT_PIECE, EMPTY
from src.Node import Node

def getScore(node: Node):
    
    print(node.depth)
    if node.state.isWin(node.lastMove): #isWin() returns a bool
        score = (ROW_SIZE * COL_SIZE - node.depth) // 2 # doesnt account for other player in tree
        # get top row of current column
        row: int
        # traverse down lastMove until you find the spot where the last move was made
        for row in range(COL_SIZE - 1, -1, -1):
            if node.state.getGrid()[row][node.lastMove] == EMPTY:
                row += 1
                break
            
        #then assign the (+) score if bot is alpha (max) and the (-) if bot is beta (min)
        if node.state.getGrid()[row][node.lastMove] == BOT_PIECE:
            node.score = score
            return node.score
        else:
            node.score = score * -1
            return node.score

     #draw, i think?       
    if node.depth == ROW_SIZE * COL_SIZE:
        node.score = 0
        return node.score
        
    node.expand(node.piece)
    for child in node.children:
        getScore(child)
        
