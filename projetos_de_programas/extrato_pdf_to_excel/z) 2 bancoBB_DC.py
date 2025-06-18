import pdfplumber
import pandas as pd
import os
from datetime import datetime
import re
import unicodedata

# Função para listar arquivos PDF na pasta
def list_pdf_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]

# Função para extrair dados do PDF
def extract_data_from_pdf(pdf_path):
    data = []
    current_row = None  # Armazena a transação atual
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                parts = line.split()
                
                # Verificar se a linha é uma transação nova (tem uma data válida)
                if len(parts) > 1:
                    date_str = parts[0]
                    try:
                        # Verificar formatos de data
                        if len(date_str) == 8:  # Formato dd/mm/aa
                            date = datetime.strptime(date_str, '%d/%m/%y').strftime('%d/%m/%Y')
                        elif len(date_str) == 10:  # Formato dd/mm/aaaa
                            date = datetime.strptime(date_str, '%d/%m/%Y').strftime('%d/%m/%Y')
                        else:
                            raise ValueError

                        # Separar valor e histórico
                        match_valor = re.search(r'\d{1,3}(?:\.\d{3})*,\d{2} [CD]', line)
                        value = match_valor.group() if match_valor else ""
                        description = line.replace(value, "").strip() if value else line.strip()

                        # Salvar a transação atual no conjunto de dados
                        if current_row:
                            data.append(current_row)  # Adiciona a linha anterior
                        current_row = [date, description, value]

                    except ValueError:
                        # Caso a linha não tenha uma data válida, tratar como complemento do histórico
                        if current_row:
                            current_row[1] += f" {line.strip()}"  # Adiciona a linha ao histórico da transação atual
                        continue

    # Adicionar a última transação pendente
    if current_row:
        data.append(current_row)

    return data

# Função para remover acentos das strings
def remove_accents(input_str):
    normalized = unicodedata.normalize('NFD', input_str)
    return ''.join([char for char in normalized if not unicodedata.combining(char)])

# Função para criar o DataFrame com ajustes na coluna Histórico e Valor
def create_dataframe(data):
    df = pd.DataFrame(data, columns=['Data', 'Histórico', 'Valor'])
    
    # Substituir todos os números e caracteres especiais na coluna Histórico por espaços
    df['Histórico'] = df['Histórico'].str.replace(r'[^\w\s]', ' ', regex=True)  # Remove caracteres especiais
    df['Histórico'] = df['Histórico'].str.replace(r'\d', ' ', regex=True)  # Remove números
    
    # Remover acentuações
    df['Histórico'] = df['Histórico'].apply(remove_accents)
    
    # Deixar tudo em maiúsculo
    df['Histórico'] = df['Histórico'].str.upper()
    
    # Substituir espaços duplos (ou múltiplos) por espaço simples
    df['Histórico'] = df['Histórico'].str.replace(r'\s+', ' ', regex=True)
    
    # Remover espaços no início do texto
    df['Histórico'] = df['Histórico'].str.lstrip()
    
    # Remover palavras específicas
    words_to_remove = ['C RENDE FACIL',
                       'BBSEG OURO MAQUINAS',
                       'HTTPS',
                       'AUTOATENDIMENTO',
                       'BB COM BR',
                       'APF APJ',
                       'AUTOATENDIMENTO',
                       'INDEX',
                       'HTML',
                       'V TEMPLATE',
                       'FCONSULTAS F',
                       'BB FH',
                       'SIM AVALIE SIM BANCO DO BRASIL',
                       'A CONTA NAO FOI MOVIMENTADA O SEU CARTAO JA ESTA DISPONIVEL EM SUA',
                       'AGENCIA TRANSACAO EFETUADA COM SUCESSO',
                       'POR J FREDERICO FENELON GUIMARAES',
                       'SIM AVALIE SIM',
                       'LIMITE OURO EMPRESARIAL C TAXA CH OURO EMPRESARIAL AO MES TAXA CH OURO EMPRESARIAL AO ANO CUSTO EFETIVO TOTAL CET AO MES CUSTO EFETIVO TOTAL CET AO ANO DATA VENCIMENTO CHEQUE ESPECIAL INFORMACOES COMPLEMENTARES CET R VALOR TOTAL DEVIDO VALOR LIBERADO DESPESAS VINCULADAS TRIBUTOS IOF TARIFA SIMULACAO PARA UTILIZACAO UNICA E INTEGRAL DO LIMITE POR DIAS A CONTA NAO FOI MOVIMENTADA TRANSACAO EFETUADA COM SUCESSO',
                       'A CONTA NAO FOI MOVIMENTADA TRANSACAO EFETUADA COM SUCESSO',
                       
                       
                       
                       
                       'PAGTO']
    for word in words_to_remove:
        df['Histórico'] = df['Histórico'].str.replace(rf'\b{word}\b', '', regex=True)
    
    # Garantir que espaços extras sejam eliminados novamente
    df['Histórico'] = df['Histórico'].str.replace(r'\s+', ' ', regex=True).str.strip()
    
    # Substituir "C" por "" na coluna Valor
    df['Valor'] = df['Valor'].str.replace(' C', '', regex=False)  # Remove "C" ao final dos valores
    
    # Adicionar "-" no início onde houver "D", e depois remover apenas o "D"
    df['Valor'] = df['Valor'].apply(
        lambda x: f"-{x[:-2]}" if x.endswith(" D") else x  # Adiciona "-" e mantém separadores decimais
    )
    
    return df

# Função para salvar o DataFrame em um arquivo Excel com o mesmo nome do PDF
def save_to_excel(df, output_pdf_name):
    # Substituir a extensão .pdf por .xlsx
    output_path = f"{os.path.splitext(output_pdf_name)[0]}.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Arquivo Excel '{output_path}' criado com sucesso!")

# Listando arquivos PDF na pasta atual
directory = '.'
pdf_files = list_pdf_files(directory)

if not pdf_files:
    print("Nenhum arquivo PDF encontrado na pasta.")
else:
    print("Arquivos PDF disponíveis:")
    for i, file in enumerate(pdf_files):
        print(f"{i + 1}. {file}")
    
    # Escolher quais PDFs processar digitando os números separados por espaço
    choices = input("Digite os números dos PDFs que deseja processar, separados por espaço (ex: 1 3 5): ").strip()
    selected_files = [int(choice) - 1 for choice in choices.split()]  # Converter os números para índices
    
    for index in selected_files:
        pdf_path = os.path.join(directory, pdf_files[index])
        data = extract_data_from_pdf(pdf_path)
        df = create_dataframe(data)
        save_to_excel(df, pdf_files[index])
