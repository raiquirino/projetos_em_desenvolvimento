import subprocess
import sys

def rodar_script(arquivo):
    try:
        subprocess.run([sys.executable, arquivo], check=True)
    except subprocess.CalledProcessError:
        print(f"⚠️ Erro ao executar o script: {arquivo}")

bancos = {
    '1': ('Banco do Brasil - Bipolar da peste', 'z) 1 bb_total_flex.py'),
    '2': ('Caixa Econômica Federal - só o osso', 'z) 1 Cef.py'),
    '3': ('BRB - pra que essa merda', 'Z) 4 BRB.py'),
    '4': ('Bradesco - Outro só pra convênio', 'Z) 5 Bradesco.py'),
    '5': ('Sicoob - Banco Arrombado', 'z) 6 sicoob_FE.py'),
    '6': ('Inter - Outro arrombando nem terminei', 'z) 1 INTER.py'),
    '7': ('Unicred - Outro Arrombado', 'z) unicred.py'),
    '8': ('Santander', 'z) 3 Santander.py'),
}

while True:
    print("\nEscolha um banco:")
    for chave, (descricao, _) in bancos.items():
        print(f"{chave} - {descricao}")

    escolha = input('\nDigita a porra do banco: ').strip()

    if escolha in bancos:
        nome_banco, script = bancos[escolha]
        print(f'\nVocê escolheu: {nome_banco}')
        rodar_script(script)
    else:
        print('❌ Não tem essa merda')

    repetir = input('\nDeseja fazer outra conversão, preguiçoso da peste? (s/n): ').strip().lower()
    if repetir != 's':
        print('Até a próxima! Besta fera 👋')
        break