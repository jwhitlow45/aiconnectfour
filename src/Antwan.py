from typing import List
from copy import deepcopy

from src.Board import Board, ROW_SIZE
from src.Node import Node

class Antwan:
    
    def dfs():
        pass
        
    def expand(self, expNode: Node, symbol: int, winScore: int) -> Node:
        
        tempStates = [Board(deepcopy(expNode.state.getGrid())) for i in range(ROW_SIZE)]
        indexStates = [(tempStates[i], i) for i in range(ROW_SIZE) if tempStates[i].move(symbol, i)]
        
        finalNodes = []
        for state, index in indexStates:
            if state.checkWin(index):
                finalNodes.append(Node(state, None, winScore))
            else:
                finalNodes.append(Node(state, None, 0))
                
        return Node(deepcopy(expNode.state), finalNodes, deepcopy(expNode.score))