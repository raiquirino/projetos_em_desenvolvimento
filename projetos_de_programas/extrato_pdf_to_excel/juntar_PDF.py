import os
from PyPDF2 import PdfMerger

# Obter o caminho da pasta onde o script está localizado
pasta_atual = os.getcwd()

# Listar todos os arquivos PDF na pasta atual
arquivos_pdf = [f for f in os.listdir(pasta_atual) if f.endswith(".pdf")]

if len(arquivos_pdf) == 0:
    print("Nenhum arquivo PDF encontrado na pasta atual.")
else:
    print("Arquivos PDF encontrados:")
    for arquivo in arquivos_pdf:
        print(arquivo)

    # Criar um objeto PdfMerger para combinar os PDFs
    mesclador = PdfMerger()

    # Adicionar cada arquivo PDF ao mesclador
    for arquivo in arquivos_pdf:
        mesclador.append(arquivo)

    # Salvar o arquivo PDF combinado
    arquivo_final = "001_pdf_mesclado_final.pdf"
    mesclador.write(arquivo_final)
    mesclador.close()

    print(f"\nPDFs combinados com sucesso! Arquivo salvo como '{arquivo_final}'.")