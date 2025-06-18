import time
import pyautogui as py
from time import sleep

# Abrir o arquivo TXT
with open('lista.txt', 'r', encoding='utf-8') as file:
    for linha in file:
        # Extrair a conta (primeira coluna) e a ação (segunda coluna)
        conta = linha.split()[0]
        # Simular cliques e teclas
        py.click(x=1000, y=10) 

        py.hotkey('Alt', 'E')
        sleep(1)
        py.write(conta)
        py.press('Enter')
        sleep(0.5) 
        
        for _ in range(7):
            py.press('tab')

        py.press('D')
        sleep(0.5)
        py.press('D')
        
        sleep(0.5) 
        py.hotkey('Alt', 'G')

print('FIM')