from typing import List

from src.Board import Board

class Node:
    def __init__(self, state: Board, children: List['Node'], score: int = 0):
        self.score: bool = score
        self.state: Board = state
        self.children: List[Node] = children
        
    def __repr__(self) -> str:
        outstr: str = ''
        outstr += f'Score: {self.score}\n'
        outstr += f'State:\n{self.state}'
        return outstr