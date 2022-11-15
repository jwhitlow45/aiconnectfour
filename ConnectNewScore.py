import numpy as np
import pygame
import sys
import math
import random

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

def winMove(board, piece): #checks all possible move locations
    # Horizontal Locations
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True
    # Vertical Wins
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    # Check positive slope diagnol
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    # Check negative slope diagnol
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True

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
        score += 100 # 4 in a row
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10 # 3 in a row
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5 # 2 in a row
        
    if window.count(opponentPiece) == 3 and window.count(EMPTY) == 1:
        score -= 10 #Block Value
    
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
    return winMove(board, PLAYER_PIECE) or winMove(board, AI_PIECE) or len(getValidLoc(board)) == 0

def minMAX(board, depth, alpha, beta, maxingPlayer): #Recursive minmax function with alpha beta Pruning
    validLocations = getValidLoc(board)
    isTerm = isTerminalNode(board)
    if depth == 0 or isTerm:
        if isTerm:
            if winMove(board, AI_PIECE): # Win for AI
                return (None, 10000000000000000)
            elif winMove(board, PLAYER_PIECE): # win for Oppenent
                return (None, -10000000000000000)
            else: # No valid move
                return (None, 0)
        else: #depth is zero
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

def pickBestMove(board, piece):
    
    validLocations = getValidLoc(board)
    bestScore = -1000000
    bestCol = random.choice(validLocations)
    for col in validLocations:
        row = getNextOpenRow(board, col)
        temp = board.copy()
        dropPiece(temp, row, col, piece)
        score = scorePosition(temp, piece)
        if score > bestScore:
            bestScore = score
            bestCol = col

    return bestCol


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

turn = PLAYER #random.randint(PLAYER, AI) #Randomly picks who goes First

moves = 0

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
                    
                    moves += 1

                    printBoard(board)
                    drawBoard(board)

                        
    #player 2 move
    if turn == AI and not gameOver:
        
        #column = random.randint(0, COLUMN_COUNT - 1)
        #column = pickBestMove(board, AI_PIECE)
        column, Ascore = minMAX(board, 6 + moves//10, -math.inf, math.inf, True)
        pygame.time.wait(100)

        print("Bot Choose: " + str(column))
        if isValidLoc(board, column):
            row = getNextOpenRow(board, column)
            dropPiece(board, row, column, AI_PIECE)
            if winMove(board, AI_PIECE):
                print("Player 2 Wins")
                label = myFont.render("PLAYER 2 WINS!!!", 1, YEL)
                screen.blit(label, (40,10))
                gameOver = True
            moves += 1

            printBoard(board)
            drawBoard(board)

            turn += 1
            turn = turn % 2

    if gameOver:
        pygame.time.wait(100000)
           