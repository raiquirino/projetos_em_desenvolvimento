import pdfplumber
import pandas as pd
import re
import os

def extrair_tabela(pdf_path):
    # Função para verificar se uma string é uma data
    def eh_data(texto):
        padrao_data = r'\b\d{2}/\d{2}/\d{4}\b'
        return bool(re.match(padrao_data, texto))

    # Função para verificar se uma string é um valor monetário
    def eh_valor(texto):
        padrao_valor = r'\b[-+()]*\d{1,3}(?:\.\d{3})*,\d{2}[DC]?\b'
        return bool(re.search(padrao_valor, texto))

    # Função para limpar caracteres indesejados
    def limpar_texto(texto):
        texto = re.sub(r'cid:\d+', '', texto)  # Remove ocorrências como "cid:9"
        texto = re.sub(r'[^a-zA-Z0-9À-ÿ\s.,:/-]', '', texto)  # Remove outros caracteres indesejados
        return texto.strip()

    dados = {
        'DATA MOV.': [],
        'ID. DOC': [],
        'HISTÓRICO': [],
        'LANÇAMENTOS (R$)': [],
        'SALDO (R$)': []
    }

    with pdfplumber.open(pdf_path) as pdf:
        saldo_anterior = 0.0  # Assumindo que o saldo inicial é 0
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            linhas = texto.split('\n')
            for linha in linhas:
                colunas = linha.split(' ')
                data = None
                id_doc = None
                valor = None
                historico = []
                for coluna in colunas:
                    coluna = limpar_texto(coluna)
                    if eh_data(coluna):
                        data = coluna
                    elif eh_valor(coluna):
                        if not valor:  # Captura apenas o primeiro valor
                            valor = coluna
                    else:
                        if re.match(r'\d{4,}', coluna):  # Verifica se é um ID de documento
                            id_doc = coluna
                        else:
                            historico.append(coluna)
                
                if data:  # Só adiciona a linha se uma data for encontrada
                    dados['DATA MOV.'].append(data if data else '')
                    dados['ID. DOC'].append(id_doc if id_doc else '')
                    dados['HISTÓRICO'].append(' '.join(historico))
                    if valor:
                        lancamento = float(valor.replace('.', '').replace(',', '.').replace('D', '').replace('C', '').replace('(', '-').replace(')', ''))
                        saldo_anterior += lancamento
                    else:
                        lancamento = 0.0
                    dados['LANÇAMENTOS (R$)'].append(valor if valor else '')
                    dados['SALDO (R$)'].append(f"{saldo_anterior:,.2f}")

    df = pd.DataFrame(dados)
    
    # Gera o nome do arquivo Excel com base no nome do arquivo PDF
    excel_path = os.path.splitext(pdf_path)[0] + '.xlsx'
    df.to_excel(excel_path, index=False)
    print(f'Arquivo Excel salvo em: {excel_path}')

def listar_arquivos_pdf(caminho_pasta):
    arquivos_pdf = [f for f in os.listdir(caminho_pasta) if f.endswith(".pdf")]
    for i, arquivo in enumerate(arquivos_pdf, start=1):
        print(f"{i}. {arquivo}")
    return arquivos_pdf

# Listar arquivos PDF na pasta
caminho_pasta = "."  # Defina o caminho da pasta onde os arquivos PDF estão localizados
arquivos_pdf = listar_arquivos_pdf(caminho_pasta)

# Perguntar qual arquivo o usuário deseja transformar
numero_escolhido = int(input("Digite o número correspondente ao extrato que deseja transformar: ")) - 1
nome_arquivo = arquivos_pdf[numero_escolhido]

# Extrair tabela do arquivo escolhido
extrair_tabela(nome_arquivo)
