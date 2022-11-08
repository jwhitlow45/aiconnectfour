from typing import List
from copy import deepcopy

from src.Board import Board, ROW_SIZE

class Node:
    def __init__(self, state: Board, children: List['Node'], lastMove: int, piece: int, score: int = 0, depth:int = 0, parent:'Node' = None):
        """constructor

        Args:
            state (Board): state of the connect four game
            children (List[Node]): list of child nodes, populated by expand()
            lastMove (int): most recent move which lead to current state
            piece (int): piece used by current node
            score (int, optional): score of current node in minimax tree. Defaults to 0.
            depth (int, optional): depth of current node in minimax tree. Defaults to 0.
            parent (Node, optional): parent node of current node. Defaults to None.
        """
        
        self.state: Board = state
        self.children: List[Node] = children
        self.lastMove = lastMove #col that the last move was made in
        self.piece = piece
        self.score: int = score
        self.parent = parent
        self.depth = depth
        
    def __repr__(self) -> str:
        outstr: str = ''
        outstr += f'Score: {self.score}\n'
        outstr += f'State:\n{self.state}'
        return outstr
    
    def expand(self, piece: int):
        """expands node, populating list of children with possible children from current state

        Args:
            piece (int): piece which will be placed in expanded states
        """
        
        tempStates = [Board(deepcopy(self.state.getGrid())) for i in range(ROW_SIZE)]
        indexStates = [(tempStates[i], i) for i in range(ROW_SIZE) if tempStates[i].move(piece, i)]
        
        finalNodes = []
        for state, index in indexStates:
            finalNodes.append(Node(state, None, index, self.piece*-1, 0, self.depth + 1, self))
                
        self.children = finalNodes
        
