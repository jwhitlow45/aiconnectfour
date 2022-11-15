import numpy as np
from math import inf
from copy import deepcopy

from src.Board import Board, ROW_SIZE, COL_SIZE, P1_PIECE, P2_PIECE
from src.Node import Node

def buildDecisionTree():
    grid = np.zeros((COL_SIZE,ROW_SIZE))
    board = Board(grid)
    root = Node(board, [], None)
    recursiveABMinMax(root)
    

def recursiveABMinMax(node: Node):

    # base case
    if node.state.countEmpty() == 0: # score is 0 given a draw
        node.score = 0
        return
    
    if node.depth == 11:
        node.score = 0
        return
    
    # base case
    leafNode = False
    winner = None
    for i in range(ROW_SIZE):
        if result := node.state.isWin(i):
            leafNode, winner = result
            break

    if leafNode:
        if winner == P1_PIECE:
            node.score = node.state.countEmpty()
            return
        elif winner == P2_PIECE:
            node.score = -1 * node.state.countEmpty()
            return

    # recursive case
    if node.depth % 2 == 0: # max node
        value = -inf
        
        # create a child states from valid moves
        childStates = [Board(deepcopy(node.state.getGrid())) for i in range(ROW_SIZE)]
        childStates = [childStates[i] for i in range(ROW_SIZE) if childStates[i].move(P1_PIECE, i)]
        
        for state in childStates:
            cNode = Node(state, [], node, None, node.depth + 1, node.alpha, node.beta)
            node.children.append(cNode)
            
            recursiveABMinMax(cNode)
            
            value = max(value, cNode.score)
            if value >= node.beta:
                break
            node.alpha = max(node.alpha, value)
        
        node.score = node.children[0].score
        for c in node.children[1:]:
            node.score = max(node.score, c.score)
    else: # min node
        value = inf
        
        # create a child states from valid moves
        childStates = [Board(deepcopy(node.state.getGrid())) for i in range(ROW_SIZE)]
        childStates = [childStates[i] for i in range(ROW_SIZE) if childStates[i].move(P2_PIECE, i)]
        
        for state in childStates:
            cNode = Node(state, [], node, None, node.depth + 1, node.alpha, node.beta)
            node.children.append(cNode)
            
            recursiveABMinMax(cNode)
            
            value = min(value, cNode.score)
            if value <= node.alpha:
                break
            node.beta = min(node.beta, value)
            
        node.score = node.children[0].score
        for c in node.children[1:]:
            node.score = min(node.score, c.score)