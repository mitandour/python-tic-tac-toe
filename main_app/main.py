from flask import Flask, redirect, url_for, request 
import game

app = Flask(__name__) 

#if the player has two in a row
def isWinState(board):
	b = board
	return (b[0] == b[1] == b[2]) or (b[3] == b[4] == b[5]) or (b[6] == b[7] == b[8]) or (b[0] == b[3] == b[6]) or (b[1] == b[4] == b[7]) or (b[2] == b[5] == b[8]) or (b[0] == b[4] == b[8]) or (b[2] == b[4] == b[6])


def hasTwoInRow(board, index1, index2, index3):
	b = board
	return 

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
		board[4] = "o"
	return board


def playOppositeCorner(board, index):
	indexes = [0, 2, 6, 8]
	return board


def playEmptyCorner(board):
	indexes = [0, 2, 6, 8]
	for i in indexes:
		if(board[i] == " "):
			board[i] == "o"
			break
		else: 
			i=i+1
	return board


def playEmptySide(board):
	indexes = [1, 3, 5,7]
	for i in indexes:
		if(board[i] == " "):
			board[i] == "o"
			break
		else: 
			i=i+1
	return board

@app.route("/") 
def home_view(): 
	return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/board',methods = ['GET'])
def play():
   if request.method == 'GET':
      board = request.args.get['board']
      return redirect(url_for('success',name = board))
   else:
      user = "haha"
      return redirect(url_for('success',name = user))

