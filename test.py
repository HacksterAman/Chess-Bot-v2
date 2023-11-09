import pyautogui as py
py.FAILSAFE=False
from stockfish import Stockfish
from PIL import Image,ImageGrab
import numpy as np
import time as T
import keyboard as key

S=Stockfish(path='.\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe',parameters={"Threads": 4})

S.make_moves_from_current_position(["e2e4"])
while True:
    print(S.get_board_visual())
    move=S.get_best_move_time(1000)
    S.make_moves_from_current_position([move])

'''

key.wait('1')
while True:
    print(py.locateCenterOnScreen('Black.png',confidence=0.8))

'''