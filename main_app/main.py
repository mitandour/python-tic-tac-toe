from flask import Flask, flash, redirect, url_for, request, Response 
from flask_api import status

app = Flask(__name__) 

#Play by marking o at a position in the board
def play(board,position):
    return board[:position]+"o"+ board[position+1:]


#check all cases where there is a possibility to win
def checkIfWinState(board, c):
    case1 = hasTwoInRow(board, 0,1,2,c)
    case2 = hasTwoInRow(board, 3,4,5,c)
    case3 = hasTwoInRow(board, 6,7,8,c)
    case4 = hasTwoInRow(board, 0,3,6,c)
    case5 = hasTwoInRow(board, 1,4,7,c)
    case6 = hasTwoInRow(board, 2,5,8,c)
    case7 = hasTwoInRow(board, 2,4,6,c)
    case8 = hasTwoInRow(board, 0,4,8,c)
    all_cases = [case1, case2, case3, case4, case5, case6, case7, case8]
    return all_cases
    

def hasTwoInRow(board, i1, i2, i3, c):
    b = board
    text = b[i1]+b[i2]+b[i3]
    if text == c+c+'_':
        return i3
    if text == '_'+c+c:
        return i1
    if text == c+'_'+c:
        return i2
    return -1


def create_fork(board):
    corners = [0, 2, 6, 8]
    if board[4] == "x":
        for x in corners:
            if board[x] == "o":
                i = getOppositeCorner(x)
                return play(board,i)
    return -1
                

def block_fork(board):
    b = board
    case1 = b[0]+b[4]+b[6]
    case2 = b[2]+b[4]+b[6]
    if case1 == "xox" or case2 == "xox" :
        return playEmptyCorner(board)
    return -1
    

def isTieState(board):
	if(isBoardCorrect(board) and (" " not in board)):
		return True
	return False	


def isBoardCorrect(board):
    for x in board:
         if (x != " " and x != "x" and x != "o"):
            								return False
    m = board.count("x")
    n = board.count("o")
    if(m > n+ 1 or n > m+ 1):
        return False
    return True                                    

def canOPlay(board):    
    #if o can play the board is valid                                    
    if board.count("x") == board.count("o") + 1 or  board.count("x") == board.count("o"):
        return True		
    else:
        return False

def isFirstMove(board):
	b = board.replace("_", "")
	if(len(b) == 1):
		return True
	return False

def isCornerOpening(board):
	index = board.index('x')
	if(isFirstMove(board) and index % 2 == 0):
		return True
	return False	

def isCenterOpening(board):
	if(isFirstMove(board) and board[4] == "x"):
		return True
	return False	


def isEdgeOpening(board):
	index = board.index('x')
	if(isFirstMove(board) and index % 2 != 0):
		return True
	return False


def playCenter(board):
	if board[4] == "_":
         return play(board, 4)


def playOppositeCorner(board, index):
	return play(board, index)

def getOppositeCorner(index):
	if(index == 0):
		return int(2)
	if(index == 2):
		return int(0)
	if(index == 6):
		return int(8)
	if(index == 8):
		return int(6)	


def playEmptyCorner(board):
	indexes = [0, 2, 6, 8]
	for i in indexes:
		if(board[i] == "_"):
			board = play(board, i)
			break
		else: 
			i=i+1
	return board


def playEmptySide(board):
	indexes = [1, 3, 5,7]
	for i in indexes:
		if(board[i] == "_"):
			board = play(board, i)
			break
		else: 
			i=i+1
	return board


def playGame(board):
    corners = [0,2,6,8]
    edges = [1,3,5,7]
    #If first Move, play optimally
    if isFirstMove(board) :
        if isCenterOpening(board):
            return playEmptyCorner(board)
        if isEdgeOpening(board):
            return playEmptySide(board)	
        if isCornerOpening(board):
            return playCenter(board)
    else:
        #Win
        win_state = checkIfWinState(board, 'o')
        for x in win_state:
             if x != -1:
                 return play(board, x) + " I won !"
        #Block
        block_state = checkIfWinState(board, 'x')
        for x in block_state:
              if x != -1:
                  return play(board, x)
        #Fork
        if create_fork(board) != -1:
            return create_fork(board)
        #Blocking an opponent's fork
        if block_fork(board) != -1:
            return block_fork(board)
        #Play in opposite corner
        for x in corners:
            i = getOppositeCorner(x)
            if (board[x] == "x") and (board[i] == "_"):
                return play(board,i)
        #Play on empty corner
        for x in corners:
            if board[x] == "_":
                return play(board, x)
        #Play on empty side
        for x in edges:
            if board[x] == "_":
                return play(board, x)
        #If we get there, then we tied!!
        return ("We tied !")
        



@app.route('/', methods=['GET'])
def api_id():
    if 'board' in request.args:
        board = request.args['board']
        if board == "":
            return "____o____"
        if len(board) < 9:
            while(len(board) < 9):
                board = board + ' '
        if isBoardCorrect(board):
            if canOPlay(board):
                board = board.replace(" ", "_")
                board = playGame(board)
                board = board.replace("_"," ")
                content = {'Board': board }
                return content, status.HTTP_200_OK
            else:
                content = {'Please try again': 'It\' not O\'s turn' }
                return content, status.HTTP_400_BAD_REQUEST
        else:
            content = {'Please try again': 'This board doesn\'t represent a valid tic-tac-toe board' }
            return content, status.HTTP_400_BAD_REQUEST
    else:
        content = {'ERROR': 'No board parameter provided. Please specify a string as the board.' }
        return content, status.HTTP_400_BAD_REQUEST

