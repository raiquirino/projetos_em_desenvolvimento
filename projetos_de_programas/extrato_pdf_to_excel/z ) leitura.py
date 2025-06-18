import os
import pdfplumber
import pandas as pd
import unicodedata
import re

def remover_acentos(texto):
    """Remove acentos de um texto."""
    nfkd = unicodedata.normalize('NFKD', texto)
    return u"".join([c for c in nfkd if not unicodedata.combining(c)])

def limpar_sequencias_numericas(texto):
    """Remove sequências numéricas puras com 5 ou mais dígitos."""
    texto = re.sub(r'(?<![.,])\b\d{5,}\b(?![.,])', '', texto)
    texto = re.sub(r'[A-Z]+\d{5,}\b(?![.,])', '', texto)
    texto = re.sub(r'(?<![.,])\b\d{5,}[A-Z]+', '', texto)
    return ' '.join(texto.split())

def substituir_quebra_linha_por_espaco(texto):
    """Substitui quebras de linha por espaços."""
    return re.sub(r'\n+', ' ', texto)

# Listar arquivos PDF na pasta atual
arquivos_pdf = [arquivo for arquivo in os.listdir() if arquivo.endswith('.pdf')]

if not arquivos_pdf:
    print("Nenhum arquivo PDF encontrado na pasta.")
else:
    print("Arquivos PDF encontrados:")
    for idx, arquivo in enumerate(arquivos_pdf):
        print(f"{idx + 1}: {arquivo}")

    escolha = int(input("Digite o número do arquivo que você deseja usar: ")) - 1

    if 0 <= escolha < len(arquivos_pdf):
        arquivo_escolhido = arquivos_pdf[escolha]
        print(f"Você escolheu: {arquivo_escolhido}")

        # Extrair texto do arquivo PDF
        linhas = []
        with pdfplumber.open(arquivo_escolhido) as pdf:
            for pagina in pdf.pages:
                conteudo = pagina.extract_text()
                if conteudo:
                    for linha in conteudo.splitlines():
                        linha_processada = remover_acentos(linha.upper())
                        linha_processada = limpar_sequencias_numericas(linha_processada)
                        linha_processada = substituir_quebra_linha_por_espaco(linha_processada)
                        if linha_processada.strip():
                            linhas.append(linha_processada)

        # Criar DataFrame e salvar no Excel
        nome_arquivo_excel = arquivo_escolhido.replace('.pdf', '.xlsx')
        contador = 1
        while os.path.exists(nome_arquivo_excel):
            nome_arquivo_excel = arquivo_escolhido.replace('.pdf', f'_{contador}.xlsx')
            contador += 1

        df = pd.DataFrame(linhas, columns=['Linha'])
        df.to_excel(nome_arquivo_excel, index=False)
        print(f"As linhas extraídas foram salvas em '{nome_arquivo_excel}'")
    else:
        print("Escolha inválida. Por favor, tente novamente.")