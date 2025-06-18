import time
import pyautogui as py
from time import sleep

def localizar(imagem):   
    tentativas = 0
    procurar = 'sim'       
    while procurar == 'sim':
        try:
            img = py.locateCenterOnScreen(imagem, confidence=0.6)
            py.click(img.x, img.y) 
            procurar = 'não'
            print('Abrindo')
        except:
            tentativas += 1
            print(f'Procurando {imagem}...Tentativa, #{tentativas}')
        sleep(1)

time.sleep(0.5)
with open('2.0_Integar.txt', 'r') as file:
    for linha in file:
        empresas = linha.split(',')[0]       
        imagem = 'tela dominio fiscal.png'       
        localizar(imagem)      
        py.hotkey('F8')
        sleep(1)
        py.write(empresas)  
        sleep(1)
        py.press('Enter')
        py.hotkey('alt', 'M')
        py.press('c')      
        imagem = 'integracao.png'       
        localizar(imagem)                    
        py.write('04/2025')
        py.press('tab')
        py.write('04/2025')
        sleep(1)
        py.hotkey('Alt', 'G')
        imagem = 'lancamentos gerados.png'       
        localizar(imagem)        
        py.hotkey('Alt', 'G')        
        imagem = 'gravar.png'       
        localizar(imagem) 
        py.press('Enter')       
        for _ in range(2):
            py.press('Esc')
print('Acabou Carai')