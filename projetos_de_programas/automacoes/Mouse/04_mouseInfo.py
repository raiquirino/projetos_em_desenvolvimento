import pyautogui
from time import sleep
pyautogui.PAUSE = 0.5
pyautogui.press('win')
pyautogui.write('cmd')
pyautogui.press('Enter')
pyautogui.write('python')
pyautogui.press('Enter')
pyautogui.write('from mouseinfo import mouseInfo')
pyautogui.press('Enter')
pyautogui.write('mouseInfo()')
pyautogui.press('Enter')
