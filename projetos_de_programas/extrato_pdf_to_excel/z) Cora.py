import os
import PyPDF2
import pandas as pd
import re
import unidecode

def listar_arquivos(pasta):
    return [f for f in os.listdir(pasta) if f.endswith('.pdf')]

def ler_pdf(arquivo):
    conteudos = []
    with open(arquivo, 'rb') as f:
        leitor = PyPDF2.PdfReader(f)
        for pagina in range(len(leitor.pages)):
            conteudo = leitor.pages[pagina].extract_text()
            conteudos.append(conteudo)
    return conteudos

def excluir_frases(conteudos):
    conteudos_filtrados = []
    for conteudo in conteudos:
        linhas_texto = conteudo.split('\n')
        linhas_filtradas = [linha for linha in linhas_texto if "Extrato gerado no dia" not in linha]
        conteudos_filtrados.append("\n".join(linhas_filtradas))
    return conteudos_filtrados

def organizar_informacoes(conteudos):
    data_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    valor_pattern = re.compile(r'[+-] R\$[\s]*[\d\.,]+')
    linhas = []
    ultima_data = None
    
    for conteudo in conteudos:
        linhas_texto = conteudo.split('\n')
        for linha in linhas_texto:
            data_encontrada = data_pattern.search(linha)
            valor_encontrado = valor_pattern.search(linha)
            
            if data_encontrada:
                data = data_encontrada.group()
                linha_sem_data = data_pattern.sub('', linha).strip()
                ultima_data = data
            else:
                linha_sem_data = linha
            
            if valor_encontrado:
                valor = valor_encontrado.group().replace('R$', '').replace(' ', '').replace('+', '')
                linha_sem_valor = valor_pattern.sub('', linha_sem_data).strip()
            else:
                valor = ''
                linha_sem_valor = linha_sem_data
            
            historico = unidecode.unidecode(linha_sem_valor.upper()).replace("  ", " ")
            historico = historico.replace("TRANSACOESEXTRATO DO PERIODO", "")
            linhas.append([linha_sem_valor, ultima_data, historico, valor])
    
    return linhas

def salvar_em_excel(conteudos, nome_arquivo):
    def obter_nome_disponivel(nome_arquivo):
        base, extensao = os.path.splitext(nome_arquivo)
        contador = 1
        novo_nome = nome_arquivo
        while os.path.exists(novo_nome):
            novo_nome = f"{base}({contador}){extensao}"
            contador += 1
        return novo_nome

    nome_arquivo = obter_nome_disponivel(nome_arquivo)
    conteudos_filtrados = excluir_frases(conteudos)
    linhas = organizar_informacoes(conteudos_filtrados)
    df = pd.DataFrame(linhas, columns=['Conteúdo', 'Data', 'Histórico', 'Valor'])
    df = df[df['Valor'] != '']
    df = df[~df['Histórico'].str.contains('TOTAL DE SAIDAS|TOTAL DE ENTRADAS')]
    df.to_excel(nome_arquivo, index=False)

def main():
    pasta = os.path.dirname(os.path.realpath(__file__))
    arquivos = listar_arquivos(pasta)
    
    print("Arquivos PDF na pasta:")
    for i, arquivo in enumerate(arquivos):
        print(f"{i + 1}. {arquivo}")

    numero = int(input("\nDigite o número do arquivo que deseja ler: ")) - 1
    
    if 0 <= numero < len(arquivos):
        nome_pdf = arquivos[numero]
        print(f"\nLendo o arquivo: {nome_pdf}\n")
        conteudos = ler_pdf(os.path.join(pasta, nome_pdf))
        nome_arquivo_excel = os.path.splitext(nome_pdf)[0] + '.xlsx'
        salvar_em_excel(conteudos, nome_arquivo_excel)
        print(f"Conteúdo salvo em {nome_arquivo_excel}")
    else:
        print("Número inválido.")

if __name__ == "__main__":
    main()
