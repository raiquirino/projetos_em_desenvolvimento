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
        
        
def foriando(quantidade,acao):
    for _ in range(quantidade):
        py.press(acao)

py.click(x=10, y=10) 
imagem = 'tela dominio.png'        
localizar(imagem)        
        
with open('1 lista.txt', 'r') as file:
    for linha in file:
        empresas = linha.split(',')[0]
        datainicial = linha.split(',')[1]
        datafinal = linha.split(',')[2]
        historico = linha.split(',')[3]
        py.click(x=1250, y=110)   
          
        # Abrindo tela do balancete
        py.press('F8')
        py.write(empresas)
        py.press('Enter')                    
        py.hotkey('Alt','R')
        py.hotkey('A')
       
        # Inserindo dados no Balancete
        imagem = 'config balanco.png'       
        localizar(imagem)  
        py.press('Tab')
        sleep(1)
        py.write(datainicial)
        py.press('Tab')
        sleep(1)
        py.write(datafinal)
        
        py.hotkey('Alt','O')   
        imagem = 'Tela do balancete.png'
        localizar(imagem)
        
        # salvando PDF
        imagem = 'salvar em PDF.png'
        localizar(imagem)
        sleep(2)
        imagem = 'salvar na area de trabalho.png'
        localizar(imagem)
        sleep(2)
        py.write(historico)
        sleep(2)
        py.press('Enter')
        sleep(2)

        # salvando EXCEL
        imagem = 'salvar em Excel.png'
        localizar(imagem)
        sleep(2)
        imagem = 'salvar na area de trabalho.png'
        localizar(imagem)
        sleep(2)
        py.write(historico)
        sleep(2)
        py.press('Enter')
 
        sleep(1) 
        py.hotkey('Alt','F4')
        
        # Preparando para proxima ação
        imagem = 'dominio.png'
        localizar(imagem)
        foriando(3,'Esc')
    print(f'Balancete da empresa {empresas} salvo')
print("Balancetes salvos, obrigad pela preferencia, Raí Tec Solucions Agredece")