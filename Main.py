import pyautogui as py
py.FAILSAFE=False
from stockfish import Stockfish
from PIL import Image,ImageGrab
import numpy as np
import time as T
import keyboard as key

S=Stockfish(path='.\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe',parameters={"Threads": 3})

#Board 368x368
#py.displayMousePosition()

X=784
Y=324
size=368 #46x8
gap=size/8

arrayX=None
arrayY=None
board=None
move=None
whiteColor=(250, 250, 250)

offset0=gap/2 # Center 23
offset1=(38,10) # Top Right
offset2=(23,30) # Bottom Center

def newGame():
    global arrayX,arrayY,move
    arrayX=np.array(['a','b','c','d','e','f','g','h'])
    arrayY=np.array(['1','2','3','4','5','6','7','8'])
    move=None
    while py.locateOnScreen("Max.png",confidence=0.9)==None:
        print("Maximize the screen first !!!")
    print('New Game')
    takeSS()
    if py.locateCenterOnScreen('Black.png',confidence=0.8)[1]>540:
        arrayX=np.flip(arrayX)
        print("White\n  |\n  |\nBlack")
        getNewMove()
    else:
        arrayY=np.flip(arrayY)
        print("Black\n  |\n  |\nWhite")
    while True:
        setNewMove()
        getNewMove()

def pos(i,j):
    return arrayX[i]+arrayY[j]

def loc(pos):
    return (np.where(arrayX == pos[0])[0][0]*gap+offset0+X,np.where(arrayY == pos[1])[0][0]*gap+offset0+Y)

def match(pix):
    if pix==(227, 244, 129) or pix==(180, 214,  59):
        return True

def takeSS():
    global board
    screenshot = ImageGrab.grab(bbox=(X, Y, X+size, Y+size))
    board=screenshot.load()
    
def getMove():
    while True:
        takeSS()
        startPos=None
        endPos=None
        for j in range(8):
            for i in range(8):
                if not startPos or not endPos:
                    if match(board[i*gap+offset1[0],j*gap+offset1[1]]):
                        if match(board[i*gap+offset2[0],j*gap+offset2[1]]): 
                            startPos=pos(i,j)
                        else:
                            endPos=pos(i,j)
                else:
                    return startPos+endPos
                    
def getNewMove():
    global move
    while True:
        newMove=getMove()
        if newMove!=move:
            S.make_moves_from_current_position([newMove])
            move=newMove
            print('Opponent:',move)
            return

def setMove():
    py.click(loc(move[:2]))
    T.sleep(0.1)
    py.click(loc(move[2:]))

def setNewMove():
    global move
    move=S.get_best_move_time(2000)
    print('Computer:',move)
    setMove()
    S.make_moves_from_current_position([move])

key.wait('1')
newGame()

