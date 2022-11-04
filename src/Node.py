from typing import List

class Node:
    def __init__(self, children: List['Node'], score: int = 0):
        self.score: bool = score
        self.children: List[Node] = children