import pyautogui as py
from time import sleep
    
def localizar_erro(imagem,imagem_erro):   
    tentativas = 0
    procurar = 'sim'       
    while procurar == 'sim':
        try:
            img = py.locateCenterOnScreen(imagem, confidence=0.8)
            py.click(img.x, img.y) 
            procurar = 'não'
            print(f'Abrindo {imagem}')
        except:
            tentativas += 1
            print(f'Procurando {imagem}...Tentativa, #{tentativas}')
        sleep(1)
        
        try:
            img = py.locateCenterOnScreen(imagem_erro, confidence=0.8)
            py.click(img.x, img.y) 
            procurar = 'não'
            print(f'Abrindo {imagem_erro}')
        except:
            tentativas += 1
            print(f'Procurando {imagem_erro}...Tentativa, #{tentativas}')
        sleep(1)
            
imagem = 'Integracao_com_sucesso.png'
imagem_erro = 'avisos.png'
localizar_erro(imagem,imagem_erro)