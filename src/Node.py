from typing import List
from copy import deepcopy
from math import inf

from src.Board import Board, ROW_SIZE, COL_SIZE, P1_PIECE, P2_PIECE

class Node:
    def __init__(self, state: Board, children: List['Node'], parent: 'Node', score: int = None, depth:int = 0, alpha: float = -inf, beta: float = inf):
        """constructor

        Args:
            state (Board): state of the connect four game
            children (List[Node]): list of child nodes, populated by expand()
            piece (int): piece used by current node
            score (int, optional): score of current node in minimax tree. Defaults to 0.
            depth (int, optional): depth of current node in minimax tree. Defaults to 0.
        """
        
        self.state: Board = state
        self.children: List[Node] = children
        self.parent = parent
        self.score: int = score
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        
    def __repr__(self) -> str:
        outstr: str = ''
        outstr += f'Score: {self.score}\n'
        outstr += f'State:\n{self.state}'
        return outstr
    