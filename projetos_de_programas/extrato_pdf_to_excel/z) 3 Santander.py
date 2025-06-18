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

        # Criar DataFrame inicial
        df = pd.DataFrame(linhas, columns=['Linha'])
       
        ############################################################################################################
        # Remove linhas indesejadas logo apos a criação do dataframe
        remove_linha_contem = [
            "AGENCIA: 3739 CONTA:",
            "EXTRATO >",
            "CONSULTAR",
            "OPCAO DE PESQUISA:",
            "TAXA DE JUROS LIMITE",
            "HTTPS:",
            "INTERNET BANKING",
            "SALDO DE CONTA CORRENTE",
            "SALDO DISPONIVEL",
            "PERIODOS:",
            "DATA HISTORICO DOCUMENTO ",
            "XXXXXXXX",
            "XXXXXXXX",
            "XXXXXXXX",
            "XXXXXXXX",
            
        ]
        
        for remove_linha in remove_linha_contem:
            df = df[~df["Linha"].str.contains(
                remove_linha, case=False, na=False)]

        ###################################################################################################'''
        # Substituições iniciais que devem ser feitas no historico após a remoção de linhas indesejadas
        substituicoes_iniciais = {
            "xxxx": "",
        }

        for padrao, novo_valor in substituicoes_iniciais.items():
            df.loc[df["Linha"].str.contains(
                padrao, regex=False), "Linha"] = novo_valor

       ############################################################################################################'''
       # padroes_para_remover = [
        # Texto
        padroes_para_remover = [
            r"PAGE \d+ OF \d+",
            r"CDA CONTRATO.*",
        ]

        for padrao in padroes_para_remover:
            df["Linha"] = df["Linha"].str.replace(padrao, "", regex=True)

        ############################################################################################################'''
        # Extrair datas para nova coluna
        df['Data'] = None  # Criar coluna Data vazia

        # Para cada linha, verificar se tem data e processar
        for idx in df.index:
            data_match = re.search(
                r'\b\d{2}/\d{2}/\d{4}\b', df.at[idx, 'Linha'])
            if data_match:
                data = data_match.group(0)
                df.at[idx, 'Data'] = data
                # Remove a data do texto original e limpa espaços extras
                df.at[idx, 'Linha'] = re.sub(
                    r'\b\d{2}/\d{2}/\d{4}\b', '', df.at[idx, 'Linha']).strip()

        ############################################################################################################'''
        # 1º Chamada de estração de valoers  da colunha linha para coluna valor
        padrao_valor = r'[-+]?(\d{1,3}(?:\.\d{3})*(?:,\d{2}))\s*[CD]?'

        # Processar cada linha e extrair o valor
        for idx in df.index:
            if pd.notna(df.at[idx, 'Data']):  # Só processa linhas com data
                valor_match = re.search(padrao_valor, df.at[idx, 'Linha'])
                if valor_match:
                    valor = valor_match.group(0)
                    df.at[idx, 'Valor'] = valor
                    # Remove o valor da coluna 'Linha'
                    df.at[idx, 'Linha'] = re.sub(re.escape(valor), '', df.at[idx, 'Linha']).strip()

        ############################################################################################################'''
            
       
        ############################################################################################################'''
        # substitui todo o historico da linha de acordo com um texto contido na linha.
        substituicoes = {
        "APLICACAO CONTAMAX": "APLICACAO CONTAMAX",
        "RESGATE CONTAMAX": "RESGATE CONTAMAX",
        "xxxxx": "xxxxx",

        }

        for padrao, novo_valor in substituicoes.items():
            df.loc[df["Linha"].str.contains(
                padrao, regex=False), "Linha"] = novo_valor
        ############################################################################################################'''     
            # Função para carregar as substituições do arquivo substituicao.txt

            def carregar_substituicoes(caminho):
                substituicoes = {}
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    for linha in arquivo:
                        if "=" in linha:
                            chave, valor = linha.split("=", 1)
                            substituicoes[chave.strip()] = valor.strip()
                return substituicoes

            caminho_arquivo = "substituicao.txt"
            substituicoes = carregar_substituicoes(caminho_arquivo)
            
            # Aplicar as substituições
            for padrao, novo_valor in substituicoes.items():
                df.loc[df["Linha"].str.contains(padrao, regex=False), "Linha"] = novo_valor

        ############################################################################################################'''#
        # Substituições que devem ser feita no historico após os tratamentos de dados   
        substituicoes_finais = {
            "xxxx": "",
            "xxxx": "",
            "  ": " ",  # Remove espaços duplos
            " ,": ",",  # Corrige espaço antes da vírgula
            ", ": ",",  # Corrige espaço depois da vírgula
        }

        for termo, substituto in substituicoes_finais.items():
            df["Linha"] = df["Linha"].str.replace(
                termo, substituto, regex=False)
        
        ############################################################################################################'''
        # Limpar espaços extras no final
        df["Linha"] = df["Linha"].str.strip()
        
        ############################################################################################################'''
        # Remover texto após padrão de CNPJ com espaços
        for idx in df.index:
            texto = df.at[idx, 'Linha']
            # Procura por padrão XX XXX XXX XXXX XX (onde X são dígitos)
            match = re.search(
                r'\b\d{2}\s+\d{3}\s+\d{3}\s+\d{4}\s+\d{2}\b', texto)
            if match:
                # Mantém o texto até o final do CNPJ
                df.at[idx, 'Linha'] = texto[:match.end()].strip()

        ############################################################################################################'''
        # Reordenar e renomear colunas
        df = df.rename(columns={'Linha': 'Historico'})
        df = df[['Data', 'Historico', 'Valor']]

        ############################################################################################################'''
        # Criar DataFrame e salvar no Excel
        nome_arquivo_excel = arquivo_escolhido.replace('.pdf', '.xlsx')
        contador = 1
        while os.path.exists(nome_arquivo_excel):
            nome_arquivo_excel = arquivo_escolhido.replace('.pdf', f'_{contador}.xlsx')
            contador += 1

        df.to_excel(nome_arquivo_excel, index=False)
        print(f"As linhas extraídas foram salvas em '{nome_arquivo_excel}'")
    else:
        print("Escolha inválida. Por favor, tente novamente.")