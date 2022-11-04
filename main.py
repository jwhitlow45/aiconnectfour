from src.Board import Board

def main():
    
    
    grid = [
        ['x','x','x','x','x','0'],
        ['x','x','x','x','0','x'],
        ['x','x','x','0','x','x'],
        ['x','x','0','x','x','x'],
        ['x','x','1','1','1','0']
    ]
    
    test = Board(grid)
    
    print(test.checkWin(2))
    pass

if __name__ == '__main__':
    main()