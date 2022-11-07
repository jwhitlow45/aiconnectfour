from typing import List
from copy import deepcopy

from src.Board import Board, ROW_SIZE

class Node:
    def __init__(self, state: Board, children: List['Node'], moveCol: int, piece: int, score: int = 0, depth:int = 0, parent:'Node' = None):
        self.state: Board = state
        self.children: List[Node] = children
        self.moveCol = moveCol
        self.piece = piece
        self.score: bool = score
        self.parent = parent
        self.depth = depth
        
    def __repr__(self) -> str:
        outstr: str = ''
        outstr += f'Score: {self.score}\n'
        outstr += f'State:\n{self.state}'
        return outstr
    
    def expand(self, symbol: int) -> 'Node':
        
        tempStates = [Board(deepcopy(self.state.getGrid())) for i in range(ROW_SIZE)]
        indexStates = [(tempStates[i], i) for i in range(ROW_SIZE) if tempStates[i].move(symbol, i)]
        
        finalNodes = []
        for state, index in indexStates:
            finalNodes.append(Node(state, None, index, self.piece*-1, 0, self.depth + 1, self))
                
        self.children = finalNodes
        
