from src.Board import Board
from src.Node import Node
from src.Antwan import *

def main():

    grid = [
        ['x','x','x','x','x','x'],
        ['x','x','x','x','x','x'],
        ['x','x','x','x','x','x'],
        ['x','x','1','1','1','x'],
        ['x','x','-1','-1','-1','x']
    ]
    boardState = Board(grid)
    myNode = Node(boardState, None, 0, 1)

    buildDecisionTree()
    
    # GameBoard = Board()
    # win = False
    # turn = 0
    # GameBoard.printGrid()
    
    
    # while True:
    #     movecol = input()
    #     if len(movecol) != 1:
    #         print('invalid move')
    #         continue
            
    #     if not movecol.isdigit():
    #         print('invalid move')
    #         continue
        
    #     movecol = int(movecol)
        
    #     if not GameBoard.move(turn, movecol):
    #         print('invalid move')
    #         continue
        
    #     GameBoard.printGrid()
    #     win = GameBoard.isWin(movecol)
    #     if win:
    #         break
        
    #     turn = int(not turn)
    
    # print(f'player {turn} won!')
    
    # pass

if __name__ == '__main__':
    main()