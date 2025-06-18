import subprocess

def banco(nome):
    if nome == '1':
        print('Banco do Brasil')
        subprocess.run(['python', 'z) 1 bb_total_flex.py'])
    elif nome == '2':
        print('Caixa Econômica Federal')
        subprocess.run(['python', 'z) 1 Cef.py'])
    elif nome == '3':
        print('BRB')
        subprocess.run(['python', 'Z) 4 BRB.py'])
    elif nome == '4':
        print('Bradesco')
        subprocess.run(['python', 'Z) 5 Bradesco.py'])
    elif nome == '5':
        print('Sicoob')  
        subprocess.run(['python', 'z) 6 sicoob_FE.py'])      
    elif nome == '6':
        print('Inter')   
        subprocess.run(['python', 'z) 1 INTER.py']) 
    elif nome == '7':
        print('Unicred')
        subprocess.run(['python', 'z) unicred.py'])
        
    elif nome == '8':
        print('Santander')
        subprocess.run(['python', 'z) 3 Santander.py'])
    else:
        print('Não tem essa merda')

while True:
    print("\nEscolha um banco:")
    print("1 - Banco do Brasil - Bipolar da peste")
    print("2 - Caixa Econômica Federal - só o osso")
    print("3 - BRB - pra que essa merda")
    print("4 - Bradesco - Outro só pra convenio")
    print("5 - Sicoob - Banco Arrombado")
    print("6 - Inter -Outro arrombando nem terminei")
    print("7 - Unicred - Outro Arrombado")
    print("7 - Santander")

    escolha = input('Digita a porra do banco: ')
    banco(escolha)

    repetir = input('\nDeseja fazer outra conversão preguiçoso da peste? (s/n): ').strip().lower()
    if repetir != 's':
        print('Até a próxima! Besta fera')
        break