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
with open('1.0_regerar.txt', 'r') as file:
    for linha in file:
        empresas = linha.split(',')[0]
        inicio = linha.split(',')[1]
        fim = linha.split(',')[2]   
        print(empresas) 
        imagem = 'tela dominio fiscal web.png'       
        localizar(imagem)
        py.hotkey('F8')  
        sleep(1)
        py.write(empresas)  
        sleep(1)
        py.press('Enter')
        py.hotkey('alt', 'u')
        py.press('a')
        py.press('a')
        py.press('Enter')
        py.press('c')            
        imagem = 'Regerar lancamentos contabeis web.png'
        localizar(imagem)
        py.write('01/04/2025')
        py.press('Tab')
        py.write('30/04/2025')
        sleep(1)        
        py.press('Tab')
        py.press('+')   #ENTRADAS
        py.press('+') # + PARA MARCAR
        py.press('Tab') # SAIDA
        py.press('+') # + PARA MARCAR
        py.press('Tab') # SERVICOS
        py.press('+') # + PARA MARCAR              
        py.press('R')
        imagem = 'final do processo web.png'
        localizar(imagem)
        py.press('Enter')
        py.press('G')   
        imagem = 'aviso.png'
        localizar(imagem)
        py.press('Enter')
        py.press('Esc')
        py.press('Esc')
print("ACABOU FILA DA PUTA")
     

