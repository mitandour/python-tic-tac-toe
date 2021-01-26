from flask import Flask, redirect, url_for, request 

app = Flask(__name__) 

def play(board,position, character):
    return board[:position] + character + board[position+1:]


#if the player has two in a row
def checkIfWinState(board, c):
    case1 = hasTwoInRow(board, 0,1,2,c)
    case2 = hasTwoInRow(board, 3,4,5,c)
    case3 = hasTwoInRow(board, 6,7,8,c)
    case4 = hasTwoInRow(board, 0,3,6,c)
    case5 = hasTwoInRow(board, 1,4,7,c)
    case6 = hasTwoInRow(board, 2,5,8,c)
    case7 = hasTwoInRow(board, 2,4,6,c)
    case8 = hasTwoInRow(board, 0,4,8,c)
    all_cases = [case1, case2, case3, case4, case5, case6, case7]
    return all_cases
    

def hasTwoInRow(board, i1, i2, i3, c):
    b = board
    text = b[i1]+b[i2]+b[i3]
    if text == c+c+' ':
        return i3
    if text == ' '+c+c:
        return i1
    if text == c+' '+c:
        return i3
    return -1

def isTieState(board):
	if(isBoardCorrect(board) and (" " not in board)):
		return True
	return False	


def isBoardCorrect(board):
	if(len(board) != 9):
          return False
	for x in board:
		if (x != " " and x != "x" and x != "o"):
            								return False	
	return True		

def isFirstMove(board):
	b = board.replace(" ", "")
	if(len(b) == 1):
		return True
	return False

def IsCornerOpening(board):
	index = board.index('x')
	if(isFirstMove(board) and index % 2 == 0):
		return True
	return False	

def IsCenterOpening(board):
	if(isFirstMove(board) and board[4] == "x"):
		return True
	return False	


def IsEdgeOpening(board):
	index = board.index('x')
	if(isFirstMove(board) and index % 2 != 0):
		return True
	return False


def PlayCenter(board):
	if(board[4] == " "):
         return play(board, 4, "o")


def playOppositeCorner(board, index):
	return play(board, index, "o")

def getOppositeCorner(board, index):
	if(index == 0):
		return 2
	if(index == 2):
		return 0
	if(index == 6):
		return 9
	if(index == 9):
		return 6			


def playEmptyCorner(board):
	indexes = [0, 2, 6, 8]
	for i in indexes:
		if(board[i] == " "):
			board = play(board, i, "o")
			break
		else: 
			i=i+1
	return board


def playEmptySide(board):
	indexes = [1, 3, 5,7]
	for i in indexes:
		if(board[i] == " "):
			board = play(board, i, "o")
			break
		else: 
			i=i+1
	return board


def playGame(board):
    if isFirstMove(board) :
        if IsCenterOpening(board):
            return playEmptyCorner(board)
        if IsEdgeOpening(board):
            return playEmptySide(board)	
        if IsCornerOpening(board):
            return PlayCenter(board)
    else:
        win_state = checkIfWinState(board, 'o')
        for x in win_state:
             if x != -1:
                 print("I won")
                 return play(board, x, "o")
        block_state = checkIfWinState(board, 'x')
        for x in block_state:
              if x != -1:
                  return play(board, x, "o")
              
        
        
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name



@app.route('/', methods=['GET'])
def api_id():
    if 'board' in request.args:
        board = request.args['board']
        if(len(board) < 9):
            position = len(board)
            while(len(board) < 9):
                board = board[:position] + " " + board[position+1:]
        if isBoardCorrect(board):
            board = playGame(board)
            return "board is correct  " +board 
        else:
            return "BOARD IS INCORRECT"
    else:
        return "Error: No board field provided. Please specify a string as the board."
    return board

