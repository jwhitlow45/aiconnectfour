from typing import List

class Node:
    def __init__(self, boardState: List[List], children: List['Node']):
        self.boardState: List[List] = boardState
        self.children: List[Node] = children