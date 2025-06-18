import subprocess
import sys
import time
import pyautogui as py
from time import sleep

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_libraries():
    required_libraries = [
        "Pillow",
        "opencv-python",
        "numpy",
        "pygetwindow",
        "pyscreeze",
        "pytweening"
    ]
    
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"A biblioteca {lib} está faltando. Instalando-a agora...")
            install(lib)

check_and_install_libraries()

# Função adicional
time.sleep(1)

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

# Segundo script com a verificação das bibliotecas
with open('lista.txt', 'r') as file:
    for linha in file:
        empresas = linha.split(',')[0]
        py.click(x=1085, y=195, duration=2)      # Click 
        py.press('F8')
        sleep(1)
        py.write(empresas)
        py.press('Enter')  
        sleep(2)                   
        py.hotkey('Alt','C')
        py.hotkey('F')
        imagem = 'fechamento.png'
        localizar(imagem)
        py.write('12/2024')
        py.press('Enter')
        py.press('Enter')      
print('FIM')
