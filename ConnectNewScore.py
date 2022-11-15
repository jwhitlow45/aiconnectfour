import numpy as np
import pygame
import sys
import math
import random

from typing import List

SQUARE_SIZE = 100 #individual Squares on board Drawn

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YEL = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

RADIUS = int(SQUARE_SIZE/2 - 5) #size of circle spaces

EMPTY = 0
STATES = set()

def createBoard(): #creates board structure
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def dropPiece(board, row, col, piece): #assign board coordinate with peice value
    board[row][col] = piece

def isValidLoc(board, col): # checks if placing space is valid
    return board[ROW_COUNT-1][col] == 0

def getNextOpenRow(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i

def printBoard(board):
    print(np.flip(board, 0))

def isInBounds(row, col):
    return not (row < 0 or col < 0 or row >= ROW_COUNT or col >= COLUMN_COUNT)

def winMove(board, piece): #checks all possible move locations
    board = np.flip(board, 0)
    
    for col in range(COLUMN_COUNT):
    
        # get top row of current column
        i: int
        for i in range(ROW_COUNT - 1, -1, -1):
            if board[i][col] == EMPTY:
                i += 1
                break
        
        # out of bound value will be returned if column is empty, in this case
        # we can just return false as there are no tiles in the current column
        if i >= ROW_COUNT:
            continue
        
        # check every direction for player win
        moves: List[List] = [[0,1], [1,0], [1,1], [1,-1]]
        player: str = board[i][col]
        
        if player != piece:
            continue
        
        for move in moves:
            count: int = 1
            
            # check in one direction for win, then opposite direction while
            # tracking the number of tiles for current player
            for dir in [-1,1]:
                rowcur: int = i
                colcur: int = col
                rowdir: int = move[0] * dir
                coldir: int = move[1] * dir
                
                while isInBounds(rowcur + rowdir, colcur + coldir):
                    rowcur += rowdir
                    colcur += coldir
                    
                    if board[rowcur][colcur] == player:
                        count += 1
                    else:
                        break
                    
            if count >= 4:
                return True
          
    return False

def drawBoard(board): #draws the board to make it easier to play
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col*SQUARE_SIZE, row*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (col*SQUARE_SIZE+SQUARE_SIZE/2, row*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2), RADIUS)
    
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (col*SQUARE_SIZE+SQUARE_SIZE/2, height - (row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[row][col] == AI_PIECE:
                pygame.draw.circle(screen, YEL, (col*SQUARE_SIZE+SQUARE_SIZE/2, height - (row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
    pygame.display.update()

def evaluateWindow(window, piece): # Looks at possible spaces and scores it depending on position
    score = 0
    opponentPiece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponentPiece = AI_PIECE

    if window.count(piece) == 4:
        score += float('inf') # 4 in a row
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10 # 3 in a row
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5 # 2 in a row
        
    if window.count(opponentPiece) == 3 and window.count(EMPTY) == 1:
        score -= float('inf') #Block Value
    
    return score

def countEmptySpaces(board):
    empties = 0
    for row in board:
        for piece in row:
            if piece == EMPTY:
                empties += 1
    return empties

# 1.0
def scorePosition(board, piece): #applying score to state
    if winMove(board, AI_PIECE):
        return float('inf')
    if winMove(board, PLAYER_PIECE):
        return -float('inf')

    score = 0

    # Center Position Score
    centerArray = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    centerCount = centerArray.count(piece)
    score += centerCount * 6

    # Horizontal Score
    for row in range(ROW_COUNT):
        rowArray = [int(i) for i in list(board[row,:])]
        for col in range(COLUMN_COUNT - 3):
            window = rowArray[col:col + WINDOW_LENGTH]

            score += evaluateWindow(window, piece)

    # Vertical Score
    for col in range(COLUMN_COUNT):
        colArray = [int(i) for i in list(board[:,col])]
        for row in range(ROW_COUNT - 3):
            window = colArray[row:row + WINDOW_LENGTH]

            score += evaluateWindow(window, piece)

    # Pos slope Diagonal
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row + i][col + i] for i in range(WINDOW_LENGTH)]

            score += evaluateWindow(window, piece)
            
    # Neg Slope Diagonal 
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row + 3 - i][col + i] for i in range(WINDOW_LENGTH)]

            score += evaluateWindow(window, piece)

    return score

def isTerminalNode(board): #Finds child or Leaf Nodes
    return (winMove(board, PLAYER_PIECE), PLAYER_PIECE) or (winMove(board, AI_PIECE), AI_PIECE) or (len(getValidLoc(board)) == 0, None)


def minMAX(board, depth, alpha, beta, maxingPlayer): #Recursive minmax function with alpha beta Pruning
    hashboard = tuple(map(tuple, board))
    if hashboard in STATES:
        return (None, scorePosition(board, AI_PIECE)) # terminate tree early and dont explore again
    if depth <= 1:
        STATES.add(hashboard)
    
    validLocations = getValidLoc(board)
    isTerm, winner = isTerminalNode(board)
    if isTerm:
        if winner == AI_PIECE:
            return (None, 10000000000000000)
        elif winner == PLAYER_PIECE:                
            return (None, -10000000000000000)
        else: # No valid move
            return (None, 0)
    elif depth == 0: #depth is zero
        return (None, scorePosition(board, AI_PIECE))

    if maxingPlayer:
        value = -math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getNextOpenRow(board, col)
            temp = board.copy()
            dropPiece(temp, row, col, AI_PIECE)
            newScore = minMAX(temp, depth - 1, alpha, beta, False)[1]
            if newScore > value:
                value = newScore
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: # min player
        value = math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getNextOpenRow(board, col)
            temp = board.copy()
            dropPiece(temp, row, col, PLAYER_PIECE)
            newScore = minMAX(temp, depth - 1, alpha, beta, True)[1]
            if newScore < value:
                value = newScore
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def getValidLoc(board): #creates a list of valid locations to place
    validLocations = []
    for col in range(COLUMN_COUNT):
        if isValidLoc(board, col):
            validLocations.append(col)
    return validLocations


board = createBoard()
print(board)
gameOver = False

pygame.init()

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

turn = AI #random.randint(PLAYER, AI) #Randomly picks who goes First

while not gameOver:

    for event in pygame.event.get(): #Player move
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, ( 0,0, width, SQUARE_SIZE))
            posX = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posX, SQUARE_SIZE/2), RADIUS)
            ''' Used for Second Non AI PLayer
            else:
                pygame.draw.circle(screen, YEL, (posX, SQUARE_SIZE/2), RADIUS)
            '''
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, ( 0,0, width, SQUARE_SIZE))

            if turn == PLAYER:
                posX = event.pos[0]
                column = math.floor(posX/SQUARE_SIZE)

                if isValidLoc(board, column):
                    row = getNextOpenRow(board, column)
                    dropPiece(board, row, column, PLAYER_PIECE)

                    if winMove(board, PLAYER_PIECE):
                        print("Player 1 Wins")
                        label = myFont.render("PLAYER 1 WINS!!!", 1, RED)
                        screen.blit(label, (40,10))
                        gameOver = True

                    turn += 1
                    turn = turn % 2

                    printBoard(board)
                    drawBoard(board)

                        
    #player 2 move
    if turn == AI and not gameOver:
        STATES = set()
        
        #column = random.randint(0, COLUMN_COUNT - 1)
        #column = pickBestMove(board, AI_PIECE)
        column, Ascore = minMAX(board, 7, -math.inf, math.inf, True)

        print("Bot Choose: " + str(column))
        if isValidLoc(board, column):
            row = getNextOpenRow(board, column)
            dropPiece(board, row, column, AI_PIECE)
            if winMove(board, AI_PIECE):
                print("Player 2 Wins")
                label = myFont.render("PLAYER 2 WINS!!!", 1, YEL)
                screen.blit(label, (40,10))
                gameOver = True

            printBoard(board)
            drawBoard(board)

            turn += 1
            turn = turn % 2

    if gameOver:
        pygame.time.wait(10000)
           