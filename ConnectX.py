import numpy as np
import pygame
import sys
import math
import random

from kaggle_environments import make

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 2
AI_PIECE = 1

WINDOW_LENGTH = 4
EMPTY = 0

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
        score -= 6 #Block Value
    
    return score

def countEmptySpaces(board):
    empties = 0
    for row in board:
        for piece in row:
            if piece == EMPTY:
                empties += 1
    return empties

def scorePosition(board, piece): #applying score to state
    empties = countEmptySpaces(board)
    if winMove(board, AI_PIECE):
        return empties
    if winMove(board, PLAYER_PIECE):
        return -empties

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
                return (None, float('inf'))
            elif winMove(board, PLAYER_PIECE): # win for Oppenent
                return (None, float('-inf'))
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
    bestScore = float('-inf')
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

def min_max_agent_0(observation, config):
    board = np.array(observation['board'])
    board = board.reshape((ROW_COUNT,COLUMN_COUNT))
    print(board)
    board = np.flip(board, 0)
    print('  0 1 2 3 4 5 6')
    print()
    column, Ascore = minMAX(board, 5, -math.inf, math.inf, True)
    return column

def min_max_agent_1(observation, config):
    board = np.array(observation['board'])
    board = board.reshape((ROW_COUNT,COLUMN_COUNT))
    print(board)
    board = np.flip(board, 0)
    print('  0 1 2 3 4 5 6')
    print()
    column, Ascore = minMAX(board, 5, -math.inf, math.inf, True)
    return column
    
env = make('connectx', debug=True)
env.reset()
env.run([min_max_agent_0, 'negamax'])
output = env.render(mode="html",width=500,height=500)
with open('game.html', 'w') as FILE:
    FILE.write(output)
           