import time
import pyautogui as py
from time import sleep


def localizar(imagem):   
    tentativas = 0
    procurar = 'sim'       
    while procurar == 'sim':
        try:
            img = py.locateCenterOnScreen(imagem, confidence=0.9)
            py.click(img.x, img.y) 
            procurar = 'não'
            print('Abrindo')
        except:
            tentativas += 1
            print(f'Procurando {imagem}...Tentativa, #{tentativas}')
        sleep(1)
        
        
imagem = 'NARUTO.png'       
localizar(imagem)