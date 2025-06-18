import tkinter as tk
from tkinter import messagebox
import requests
import re
import locale
from datetime import datetime

# Definindo a localidade para formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_cnpj(cnpj):
    """Remove caracteres especiais do CNPJ."""
    return re.sub(r'\D', '', cnpj)

def formatar_valor(valor):
    """Formata o valor para o padrão brasileiro."""
    try:
        return locale.currency(float(valor), grouping=True)
    except ValueError:
        return 'Não disponível'

def formatar_data(data):
    """Formata a data para o padrão brasileiro (DD/MM/YYYY)."""
    if not data:
        return 'Não disponível'
    
    try:
        # Tentando o formato comum (YYYY-MM-DD)
        return datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
    except ValueError:
        try:
            # Tentando o formato alternativo (DD/MM/YYYY)
            return datetime.strptime(data, '%d/%m/%Y').strftime('%d/%m/%Y')
        except ValueError:
            return 'Não disponível'

def consultar_cnpj():
    cnpj = formatar_cnpj(entry_cnpj.get())
    if len(cnpj) != 14:
        messagebox.showerror("Erro", "CNPJ inválido. Por favor, insira um CNPJ válido.")
        return

    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        campos = {
            "EMPRESA": data.get('nome', 'Não disponível'),
            "CAPITAL SOCIAL": formatar_valor(data.get('capital_social', 'Não disponível')),
            "DATA DE ABERTURA": formatar_data(data.get('abertura', '')),  # Aqui ajustamos o campo 'abertura'
            "SITUAÇÃO CADASTRAL": data.get('situacao', 'Não disponível'),
            "EMAIL": data.get('email', 'Não disponível'),
            "TELEFONE": data.get('telefone', 'Não disponível'),
            "ATIVIDADE PRINCIPAL": data.get('atividade_principal', [{}])[0].get('text', 'Não disponível')
        }

        # Atualizar as informações no GUI
        for chave, valor in campos.items():
            atualizar_texto(chave, valor)

        # Atualizar a lista de sócios e atividades secundárias
        atualizar_lista('QUADRO SOCIETARIO', [socio.get('nome', 'Não disponível') for socio in data.get('qsa', [])])
        atualizar_lista('ATIVIDADES SECUNDÁRIAS', [atividade.get('text', 'Não disponível') for atividade in data.get('atividades_secundarias', [])])

    else:
        messagebox.showerror("Erro", "CNPJ não encontrado ou inválido.")

def atualizar_texto(campo, valor):
    """Atualiza o texto nos widgets de texto de acordo com o campo."""
    text_dict = {
        "EMPRESA": text_nome,
        "CAPITAL SOCIAL": text_capital,
        "DATA DE ABERTURA": text_data_abertura,
        "SITUAÇÃO CADASTRAL": text_situacao,
        "EMAIL": text_email,
        "TELEFONE": text_telefone,
        "ATIVIDADE PRINCIPAL": text_atividade_principal
    }
    if campo in text_dict:
        text_dict[campo].delete(1.0, tk.END)
        text_dict[campo].insert(tk.END, valor)

def atualizar_lista(campo, lista):
    """Atualiza as listas de sócios ou atividades secundárias."""
    listbox_dict = {
        'QUADRO SOCIETARIO': socios_listbox,
        'ATIVIDADES SECUNDÁRIAS': atividades_listbox
    }
    if campo in listbox_dict:
        listbox = listbox_dict[campo]
        listbox.delete(0, tk.END)
        for item in lista:
            listbox.insert(tk.END, item)

def resetar_campos():
    """Reseta todos os campos de entrada e saída."""
    entry_cnpj.delete(0, tk.END)
    for text_widget in [text_nome, text_capital, text_data_abertura, text_situacao, text_email, text_telefone, text_atividade_principal]:
        text_widget.delete(1.0, tk.END)
    for listbox in [socios_listbox, atividades_listbox]:
        listbox.delete(0, tk.END)

def copiar_nome():
    """Copia o nome da empresa para a área de transferência.""" 
    root.clipboard_clear()
    root.clipboard_append(text_nome.get(1.0, tk.END).strip())

# Configuração da janela principal
root = tk.Tk()
root.title("Consulta de CNPJ")
root.geometry("1000x1000")  # Aumenta o tamanho da janela

# Função para criar Labels e Texts
def criar_label_e_texto(campo, linha):
    tk.Label(root, text=campo).grid(row=linha, column=0, padx=10, pady=10, sticky='e')
    texto = tk.Text(root, height=2, width=80, font=('Helvetica', 11))
    texto.grid(row=linha, column=1, columnspan=2, padx=10, pady=10, sticky='w')
    return texto

# Campo de entrada para CNPJ
tk.Label(root, text="CNPJ:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
entry_cnpj = tk.Entry(root, width=30)
entry_cnpj.grid(row=3, column=1, padx=10, pady=10, sticky='w')

# Botões
tk.Button(root, text="Buscar", command=consultar_cnpj).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Resetar Campos", command=resetar_campos).grid(row=4, column=1, padx=10, pady=10)

# Widgets de texto
text_nome = criar_label_e_texto("EMPRESA", 5)
text_capital = criar_label_e_texto("CAPITAL SOCIAL", 7)
text_data_abertura = criar_label_e_texto("DATA DE ABERTURA", 8)
text_situacao = criar_label_e_texto("SITUAÇÃO CADASTRAL", 9)
text_email = criar_label_e_texto("EMAIL", 10)
text_telefone = criar_label_e_texto("TELEFONE", 11)
text_atividade_principal = criar_label_e_texto("ATIVIDADE PRINCIPAL", 13)

# Lista de sócios e atividades secundárias
tk.Label(root, text="QUADRO SOCIETARIO:").grid(row=12, column=0, padx=10, pady=10, sticky='e')
socios_listbox = tk.Listbox(root, height=6, width=80, font=('Helvetica', 11))
socios_listbox.grid(row=12, column=1, columnspan=2, padx=10, pady=10, sticky='w')

tk.Label(root, text="ATIVIDADES SECUNDÁRIAS:").grid(row=14, column=0, padx=10, pady=10, sticky='e')
atividades_listbox = tk.Listbox(root, height=6, width=80, font=('Helvetica', 11))
atividades_listbox.grid(row=14, column=1, columnspan=2, padx=10, pady=10, sticky='w')

# Rodapé
rodape = tk.Label(root, text="Raí Tech Solutions")
rodape.grid(row=15, column=0, columnspan=3, padx=10, pady=10, sticky='we')

root.mainloop()
