from src.Board import Board

def main():
    
    GameBoard = Board()
    win = False
    turn = 0
    GameBoard.printGrid()
    
    
    while True:
        movecol = input()
        if len(movecol) != 1:
            print('invalid move')
            continue
            
        if not movecol.isdigit():
            print('invalid move')
            continue
        
        movecol = int(movecol)
        
        if not GameBoard.move(turn, movecol):
            print('invalid move')
            continue
        
        GameBoard.printGrid()
        win = GameBoard.checkWin(movecol)
        if win:
            break
        
        turn = int(not turn)
    
    print(f'player {turn} won!')
    
    pass

if __name__ == '__main__':
    main()