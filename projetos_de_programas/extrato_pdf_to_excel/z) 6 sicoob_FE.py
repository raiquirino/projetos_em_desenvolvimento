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


        ######

        
        
        ############################################################################################################
        # REMOVER LINHAS QUE CONTEM
        remove_linha_contem = [
            "RESUMO",
            "SALDO DO DIA =====",
            "SALDO EM CONTA",
            "LIMITE CHEQUE",
            "SALDO DISPONIVEL",
            "SALDO BLOQUEADO",
            "TAXA CHEQUE ESPECIAL",
            "PREVISAO CPMF",
            "PREVISAO IOF",
            "PREVISAO ENCARGOS",
            "PREVISAO TARIFAS:",
            "LIMITES DE CREDITO",
            "ACESSE O MENU CREDITO",
            "EXTRATO NO.",
            "SAC: 0800",
            "ABOUT:BLANK",
            "PAGAMENTO PIX",
            "RECEBIMENTO PIX",
            "CODIGO TED",
            "TRANSFERENCIA PIX",
            "FENELON",
            "ODONTOLOGICA FENEL",
            "PLATAFORMA DE SERVICOS FINANCEIRO",
            "SICOOB -SISTEMA DE COOPERATIVAS DE CREDITO DO BRASIL",
            "EXTRATO CONTA CORRENTE",
            "DATA DOCUMENTO HISTORICO VALOR",
            "SICOOB UNICENTRO BR",
            "XXXXXXXX",
            "XXXXXXXX",
            "XXXXXXXX"
        ]

        # Filtrar as linhas para remover aquelas que contêm os textos definidos
        for remove_linha in remove_linha_contem:
            df = df[~df["Linha"].str.contains(
                remove_linha, case=False, na=False)]


        ###################################################################################################

            substituicoes_iniciais = {
   
            "xxxx": "",
            "xxxx": "",
            "xxxx": "",
            "xxxx": "",
        }

        # Aplicar as alterações usando um loop
        # Aplicar as substituições no DataFrame
        for padrao, novo_valor in substituicoes_iniciais.items():
            df.loc[df["Linha"].str.contains(
                padrao, regex=False), "Linha"] = novo_valor

       ############################################################################################################
       # padroes_para_remover = [
        # Texto
        padroes_para_remover = [
            r"  ",
            r"PAGE \d+ OF \d+",
            r"CDA CONTRATO.*",
            r"CDA-CONTRATO*",
        ]

        for padrao in padroes_para_remover:
            df["Linha"] = df["Linha"].str.replace(padrao, "", regex=True)

       # Extrair datas para nova coluna

        ############################################################################################################'''
        # Criar coluna Data vazia
        df['Data'] = None
        # Para cada linha, verificar se tem data e processar
        for idx in df.index:
            data_match = re.search(
                r'\b\d{2}/\d{2}/\d{2,4}\b', df.at[idx, 'Linha'])  # Reconhece 2 ou 4 dígitos no ano
            if data_match:
                data = data_match.group(0)
                df.at[idx, 'Data'] = data
                # Remove a data do texto original e limpa espaços extras
                df.at[idx, 'Linha'] = re.sub(
                    r'\b\d{2}/\d{2}/\d{2,4}\b', '', df.at[idx, 'Linha']).strip()
        ############################################################################################################'''
        
        # Extrair valores monetários
        df['Valor'] = None  # Criar coluna Valor vazia

        # Padrão para encontrar valores monetários (com ou sem espaço antes de C/D)
        padrao_valor = r'\b\d{1,3}(?:\.\d{3})*(?:,\d{2})?\s*[CD]\b'

        # Para cada linha, procurar valores monetários
        for idx in df.index:
            if pd.notna(df.at[idx, 'Data']):  # Só processa linhas com data
                valor_match = re.search(padrao_valor, df.at[idx, 'Linha'])
                if valor_match:
                    valor = valor_match.group(0)
                    df.at[idx, 'Valor'] = valor
                    # Remove o valor do texto original e limpa espaços extras
                    df.at[idx, 'Linha'] = re.sub(
                        padrao_valor, '', df.at[idx, 'Linha']).strip()

        ############################################################################################################
        # Mover informações de linhas sem data para o histórico da primeira data anterior
        ultima_data_idx = None
        linhas_para_remover = []

        for idx in df.index:
            if pd.notna(df.at[idx, 'Data']):
                ultima_data_idx = idx
            elif ultima_data_idx is not None and pd.notna(df.at[idx, 'Linha']):
                # Adicionar informação à linha com a última data
                df.at[ultima_data_idx, 'Linha'] = df.at[ultima_data_idx,
                    'Linha'] + ' ' + df.at[idx, 'Linha']
                linhas_para_remover.append(idx)

        # Remover as linhas que foram movidas
        df = df.drop(linhas_para_remover).reset_index(drop=True)
   
        ############################################################################################################
        # Segunda verificação de valores monetários apenas em células vazias
        
        for idx in df.index:
            # Só processa se não tem valor E tem data (linha principal)
            if pd.isna(df.at[idx, 'Valor']) and pd.notna(df.at[idx, 'Data']):
                texto = df.at[idx, 'Linha']
                # Expressão regular para capturar valores (exemplo: 1.414,87D ou 1.573,00D)
                valor_match = re.search(r'\d{1,3}(?:\.\d{3})*,\d{2}[CD]?', texto)

        ############################################################################################################

        # Processar valores com D para adicionar sinal negativo
        for idx in df.index:
            if pd.notna(df.at[idx, 'Valor']):
                valor = df.at[idx, 'Valor']             
                # Se valor é uma string, realiza a lógica necessária
                if isinstance(valor, str):
                    # Se termina com D (com ou sem espaço)
                    if valor.strip().endswith('D'):
                            # Remove o D e adiciona o sinal negativo
                        valor_sem_d = valor.replace('D', '').strip()
                        df.at[idx, 'Valor'] = f"-{valor_sem_d}"
                        # Se termina com C, apenas remove o C
                    elif valor.strip().endswith('C'):
                        df.at[idx, 'Valor'] = valor.replace('C', '').strip()
                else:
                        # Caso 'valor' não seja uma string, continue ou trate isso como necessário
                    pass

        ############################################################################################################
        substituicoes_finais = {
            "PIX PIX ": "PIX ",
            "PIX  ": "PIX ",
            "PAGAMENTO A FENELON": "",
            "TRANSFERENCIA ENTRE CONTAS": "",
            "TRANSFERENCIA ENTRE CONTA": "",
            "REM.:": "",
            "FAV.:": "",
            "NTERCREDIS": "NTERCREDIS ",
            "xxxx": "",
            "xxxx": "",
            "xxxx": "",
            "xxxx": "",
            "xxxx": "",
            "  ": " ",  # Remove espaços duplos
            " ,": ",",  # Corrige espaço antes da vírgula
            ", ": ",",  # Corrige espaço depois da vírgula
        }

        ############################################################################################################
        # Lista de substituições
        substituicoes = {
        "78.738.101 0001 -51": "DENTAL UNI COOPERATIVA ODONTOLOGICA",

        }

        # Aplicar as alterações usando um loop
        # Aplicar as substituições no DataFrame
        for padrao, novo_valor in substituicoes.items():
            df.loc[df["Linha"].str.contains(
                padrao, regex=False), "Linha"] = novo_valor
        ############################################################################################################

            

            # Função para carregar as substituições do arquivo substituicao.txt


            def carregar_substituicoes(caminho):
                substituicoes = {}
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    for linha in arquivo:
                        if "=" in linha:
                            chave, valor = linha.split("=", 1)
                            substituicoes[chave.strip()] = valor.strip()
                return substituicoes


            # Carregar o arquivo substituicao.txt
            # Certifique-se de que o arquivo está na mesma pasta
            caminho_arquivo = "substituicao.txt"
            substituicoes = carregar_substituicoes(caminho_arquivo)
            
            # Aplicar as substituições
            for padrao, novo_valor in substituicoes.items():
                df.loc[df["Linha"].str.contains(padrao, regex=False), "Linha"] = novo_valor
            
        #############################################################################################################

        # Aplicar substituições
        for termo, substituto in substituicoes_finais.items():
            df["Linha"] = df["Linha"].str.replace(
                termo, substituto, regex=False)

        # Limpar espaços extras no final
        df["Linha"] = df["Linha"].str.strip()

        # Remover texto após padrão de CNPJ com espaços
        for idx in df.index:
            texto = df.at[idx, 'Linha']
            # Procura por padrão XX XXX XXX XXXX XX (onde X são dígitos)
            match = re.search(
                r'\b\d{2}\s+\d{3}\s+\d{3}\s+\d{4}\s+\d{2}\b', texto)
            if match:
                # Mantém o texto até o final do CNPJ
                df.at[idx, 'Linha'] = texto[:match.end()].strip()

        ############################################################################################################

        # Reordenar e renomear colunas
        df = df.rename(columns={'Linha': 'Historico'})
        df = df[['Data', 'Historico', 'Valor']]

        ############################################################################################################
        # Criar DataFrame e salvar no Excel
        nome_arquivo_excel = arquivo_escolhido.replace('.pdf', '.xlsx')
        contador = 1
        while os.path.exists(nome_arquivo_excel):
            nome_arquivo_excel = arquivo_escolhido.replace(
                '.pdf', f'_{contador}.xlsx')
            contador += 1

        df.to_excel(nome_arquivo_excel, index=False)
        print(f"As linhas extraídas foram salvas em '{nome_arquivo_excel}'")
    else:
        print("Escolha inválida. Por favor, tente novamente.")
