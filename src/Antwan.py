from typing import List
from copy import deepcopy
import math

from src.Board import Board, ROW_SIZE, COL_SIZE, BOT_PIECE , EMPTY
from src.Node import Node

def abPruning(node: Node, alpha = -math.inf, beta = math.inf):
    score = (ROW_SIZE * COL_SIZE - node.depth)
    print(node)
    print(score)

    #gets score of current node
    if ((node.depth == 0 )or (node.children == None)):
        #if at depth 0 or if node is a leaf return score
        print("Base score:", score)
        return score

    if(BOT_PIECE == node.piece):
        #if the current piece was played by the bot
        value = -math.inf

        for kid in node.children:
            value = max(value, abPruning(kid, node.parent, alpha, beta))
            if (value >= beta):
                break
            alpha = max(alpha, value)
        print("Bot value: ", value)
        return value

    else:
        value = math.inf
        for kid in node.children:
            value = min(value, abPruning(kid, node.parent, alpha, beta))
            if (value <= alpha):
                break
            beta = min(beta, value)
    print("Not bot value: ", value)
    return value

def getScore(node: Node):
    
    print(node.depth)
    if node.state.isWin(node.lastMove): #isWin() returns a bool
        score = (ROW_SIZE * COL_SIZE - node.depth) // 2  + 7 #should calculate correct score given depth
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
        