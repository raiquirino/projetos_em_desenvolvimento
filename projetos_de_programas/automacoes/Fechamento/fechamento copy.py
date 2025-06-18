import os
import subprocess

# Diretório onde o código está localizado
diretorio_codigo = os.path.dirname(os.path.abspath(__file__))

# Define os comandos
comando_criar_venv = f"python -m venv {diretorio_codigo}\\venv"

# Executa a criação do ambiente virtual
os.system(comando_criar_venv)

# Comando para ativar o ambiente virtual e executar o script Python
activate_command = f"{diretorio_codigo}\\venv\\Scripts\\activate.bat && python {diretorio_codigo}\\fechamento_copy.py"

# Executa o comando de ativação e o script Python
subprocess.call(activate_command, shell=True)
