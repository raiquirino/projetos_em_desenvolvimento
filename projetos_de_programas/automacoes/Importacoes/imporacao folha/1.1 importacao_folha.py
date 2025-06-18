import pyautogui as py
from time import sleep

# Lista para armazenar as empresas que tiveram erro de débito ou crédito
diferenca_debitoxcredito = []
erro_contador = 0  # Declarar contador de erro global

def localizar(imagem):   
    tentativas = 0
    procurar = 'sim'       
    while procurar == 'sim':
        try:
            img = py.locateCenterOnScreen(imagem, confidence=0.6)
            py.click(img.x, img.y) 
            procurar = 'não'
            print(f'Abrindo {imagem}')
        except:
            tentativas += 1
            print(f'Procurando {imagem}...Tentativa, #{tentativas}')
            sleep(1)

#---------------------------------------------------------------------             
def localizar_erro(imagem, imagem_erro1, imagem_erro2, acao1, acao2, empresas):   
    global diferenca_debitoxcredito, erro_contador  # Tornar variáveis globais acessíveis
    tentativas = 0
    procurar = 'sim'       
    while procurar == 'sim':
        try:
            img = py.locateCenterOnScreen(imagem, confidence=0.7)
            py.click(img.x, img.y) 
            procurar = 'não'
            print(f'Abrindo {imagem}')
        except:
            tentativas += 1
            print(f'Procurando {imagem}... Tentativa #{tentativas}')
        
        sleep(1)
        # Verificar se já existem lançamentos
        try:
            img = py.locateCenterOnScreen(imagem_erro1, confidence=0.7)
            py.click(img.x, img.y) 
            procurar = 'não'
            print(f'Abrindo {imagem_erro1}')
            py.hotkey(acao1)


            # Verifica a imagem após executar a ação 1
            try:
                img = py.locateCenterOnScreen(imagem, confidence=0.7)
                py.click(img.x, img.y) 
                procurar = 'não'
                print(f'Abrindo {imagem}')
                py.press('Enter')
            except:
                tentativas += 1
                print(f'{imagem}, Tentativa #{tentativas}')
            sleep(1)
        except:
            tentativas += 1
            print(f'Procurando {imagem_erro1}... Tentativa #{tentativas}')
        
        # Verificar diferença de débito/crédito
        try:
            img = py.locateCenterOnScreen(imagem_erro2, confidence=0.7)
            py.click(img.x, img.y) 
            procurar = 'não'
            print(f'Abrindo {imagem_erro2}')
            py.hotkey(acao2)
            erro_contador += 1  # Incrementar contador de erro
            diferenca_debitoxcredito.append(empresas)  # Adicionar nome da empresa à lista
            print(f"Erro encontrado para a empresa: {empresas}. Contador de erros: {erro_contador}")
        except:
            print(f'Procurando {imagem_erro2}... Tentativa #{tentativas}')
        
        sleep(1)

#---------------------------------------------------------------------         
with open('1.0 Lista_folha.txt', 'r') as file:
    for linha in file:
        empresas = linha.split(',')[0]  # Obter o nome da empresa
        print(f'Processando empresa: {empresas}') 
        imagem = 'tela_dominio.png'       
        localizar(imagem)
        py.hotkey('F8')  
        sleep(1)
        py.write(empresas)  
        sleep(1)
        py.press('Enter')
        py.hotkey('Alt', 'P')
        py.press(['I', 'i', 'Enter'], interval=1)
        imagem = 'integracao_contabil.png'
        localizar(imagem)   
        py.write('04/2025')
        py.press('Tab')
        sleep(1)
        py.press('Tab')
        py.write('04/2025')
        sleep(1)
        py.hotkey('Alt', 'G')
        
        imagem = 'rubricas itens nao consigurados.png'       
        localizar(imagem)
        py.hotkey('Alt', 'O')
        
        imagem = 'integracao_com a contabilidade.png'
        localizar(imagem)
        sleep(2)
        py.hotkey('Alt', 'G')
        
        print('A parte que quero ver...............................................................')
        
        imagem = 'Integracao_com_sucesso.png'  # Caso esteja tudo ok, segue o bonde
        imagem_erro1 = 'periodo_com_lancamento_gravado.png'  # Verifica se já existem lançamentos gravados
        imagem_erro2 = 'diferenca.png'  # Verifica lançamentos com diferenças de crédito ou débito
        acao1 = 'Alt', 'C'
        acao2 = 'Alt', 'S'
        localizar_erro(imagem, imagem_erro1, imagem_erro2, acao1, acao2, empresas)  # Passar o nome da empresa atual

        for _ in range(6):
            py.press('Esc')
            
    print(f'{empresas} finalizada')  

# Mostrar as empresas que apresentaram erro ao final
print('Empresas que apresentaram erro:')
for empresas in diferenca_debitoxcredito:
    print(f'- {empresas}')

# Mostrar o contador de erros ao final
print(f'Total de erros identificados: {erro_contador}')

print('Acabou Carai!!! Peguei as manhas')