import termios
import time
import sys
import tty
import os

def readchar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def readkey():
	c1 = readchar()
	if ord(c1) != 0x1b:
		return c1
	c2 = readchar()
	if ord(c2) != 0x5b:
		return c1 + c2
	c3 = readchar()
	if ord(c3) != 0x33:
		return c1 + c2 + c3
	c4 = readchar()
	return c1 + c2 + c3 + c4

opts1 = ["   ⚪                               ", "       ⚪                           ", "           ⚪                       ", "               ⚪                   ", "                   ⚪               ", "                       ⚪           ", "                           ⚪       ", "                               ⚪   "]
opts2 = ["   🔴                               ", "       🔴                           ", "           🔴                       ", "               🔴                   ", "                   🔴               ", "                       🔴           ", "                           🔴       ", "                               🔴   "]
opts3 = ["   🟡                               ", "       🟡                           ", "           🟡                       ", "               🟡                   ", "                   🟡               ", "                       🟡           ", "                           🟡       ", "                               🟡   "]

def processPiece(num):
  if num == ' ':
    return '⚪'
  elif num == '0':
    return '🔴'
  else:
    return '🟡'

def printBoard(board):
  numofstuff = ((list(os.get_terminal_size())[1]-13) // 2)-3
  spaces = ((list(os.get_terminal_size())[0]-36) // 2)
  print(" "*spaces, end="")
  print()
  print(f"\033[38;2;255;255;255m" + " "*spaces, end="\033[0m")
  print(f"\033[40m                                    \033[m")
  print(" "*spaces, end="")
  temp1 = "  ".join([processPiece(p) for p in board[0]])
  print(f"\033[40m   " + temp1 + "   \033[m")
  print(" "*spaces, end="")
  print(f"\033[40m                                    \033[m")
  print(" "*spaces, end="")
  temp2 = "  ".join([processPiece(p) for p in board[1]])
  print(f"\033[40m   " + temp2 + "   \033[m")
  print(" "*spaces, end="")
  print(f"\033[40m                                    \033[m")
  print(" "*spaces, end="")
  temp3 = "  ".join([processPiece(p) for p in board[2]])
  print(f"\033[40m   " + temp3 + "   \033[m")
  print(" "*spaces, end="")
  print(f"\033[40m                                    \033[m")
  print(" "*spaces, end="")
  temp4 = "  ".join([processPiece(p) for p in board[3]])
  print(f"\033[40m   " + temp4 + "   \033[m")
  print(" "*spaces, end="")
  print(f"\033[40m                                    \033[m")
  print(" "*spaces, end="")
  temp5 = "  ".join([processPiece(p) for p in board[4]])
  print(f"\033[40m   " + temp5 + "   \033[m")
  print(" "*spaces, end="")
  print(f"\033[40m                                    \033[m")
  print(" "*spaces, end="")
  temp6 = "  ".join([processPiece(p) for p in board[5]])
  print(f"\033[40m   " + temp6 + "   \033[m")
  print(" "*spaces, end="")
  print(f"\033[40m                                    \033[m")
  print(" "*spaces, end="")
  print("\n"*numofstuff)

board = [[' ' for x in range(8)] for i in range(6)]

def getDiagonals():
  diagonals = []
  for i in range(13):
    diagonals.append([])
    for j in range(max(i - 7, 0), min(i + 1, 6)):
      diagonals[i].append(board[6 - i + j - 1][j])
  for i in range(13):
    diagonals.append([])
    for j in range(max(i - 6 + 1, 0), min(i + 1, 6)):
      diagonals[i].append(board[i - j][j])
  return diagonals

def makeMove(team, col):
  try:
    col = int(col) - 1
  except:
    return False
  if (col+1) not in [1, 2, 3, 4, 5, 6, 7, 8]:
    return False
  if ' ' not in [i[col] for i in board]:
    return False
  i = 5
  while board[i][col] != ' ':
    i -= 1
  board[i][col] = team
  return board

def checkWin():
  fourInARow = [['0', '0', '0', '0'], ['1', '1', '1', '1']]
  for row in range(6):
    for col in range(5):
      if board[row][col:(col+4)] in fourInARow:
        return [True, board[row][col:(col+4)]]
  for row in range(8):
    for col in range(3):
      if [x[row] for x in board][col:(col+4)] in fourInARow:
        return [True, [x[row] for x in board][col:(col+4)]]
  for row in getDiagonals():
    for col, _ in enumerate(row):
      if row[col:(col+4)] in fourInARow:
        return [True, row[col:(col+4)]]
  return [False, None]

permabad = []
rowstocheck = [1, 2, 3, 4, 5, 6, 7, 8]
while True:
  print("\033[?25l", end="")
  if checkWin()[0]:
    break
  index1 = 0
  while True:
    os.system('clear')
    if ' ' in [i[index1] for i in board]:
      print("\n"*(((list(os.get_terminal_size())[1]-13) // 2)-3))
      print(" "*((list(os.get_terminal_size())[0]-36) // 2), end="")
      print(opts2[index1])
      printBoard(board)
      char = readkey()
      if char == "\x1b\x5b\x44":
        if index1-1 >= 0 and index1-1 <= 7:
          index1 -= 1
      elif char == "\x1b\x5b\x43":
        if index1+1 >= 0 and index1+1 <= 7:
          index1 += 1
      elif char == "\x0d":
        makeMove('0', index1+1)
        break
    else:
      index1 += 1
  if checkWin()[0]:
    break
  index2 = 0
  while True:
    os.system('clear')
    if ' ' in [i[index2] for i in board]:
      print("\n"*(((list(os.get_terminal_size())[1]-13) // 2)-3))
      print(" "*((list(os.get_terminal_size())[0]-36) // 2), end="")
      print(opts3[index2])
      printBoard(board)
      char = readkey()
      if char == "\x1b\x5b\x44":
        if index2-1 >= 0 and index2-1 <= 7:
          index2 -= 1
      elif char == "\x1b\x5b\x43":
        if index2+1 >= 0 and index2+1 <= 7:
          index2 += 1
      elif char == "\x0d":
        makeMove('1', index2+1)
        break
    else:
      index2 += 1

os.system('clear')
print("\n"*(((list(os.get_terminal_size())[1]-13) // 2)-3))
print()
printBoard(board)
print('\033[4mGame Over\033[0m')
while True:
  readkey()