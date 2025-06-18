import os
import PyPDF2
import pandas as pd
import re

# Listar arquivos PDF na pasta atual
arquivos_pdf = [arquivo for arquivo in os.listdir()
                                                  if arquivo.endswith('.pdf')]

if not arquivos_pdf:
    print("Nenhum arquivo PDF encontrado na pasta.")
else:
    print("Arquivos PDF encontrados:")
    for idx, arquivo in enumerate(arquivos_pdf):
        print(f"{idx + 1}: {arquivo}")

    # Permitir que o usuário escolha o arquivo
    try:
        escolha = int(
            input("Digite o número do arquivo que você deseja usar: ")) - 1

        if 0 <= escolha < len(arquivos_pdf):
            arquivo_escolhido = arquivos_pdf[escolha]
            print(f"Você escolheu: {arquivo_escolhido}")

            # Extrair texto do arquivo PDF
            linhas = []
            with open(arquivo_escolhido, 'rb') as arquivo_pdf:
                leitor = PyPDF2.PdfReader(arquivo_pdf)
                for pagina in leitor.pages:
                    conteudo = pagina.extract_text()
                    linhas.extend(conteudo.splitlines())

            # Funções para extrair informações (datas e valores monetários)
            def extrair_datas(texto):
                padrao_data = r"\d{2}/\d{2}/\d{4}|\d{2}/\d{2}"
                return re.findall(padrao_data, texto)

            def extrair_valores(texto):
                # Novo padrão para capturar valores no formato especificado
                padrao_valor = r"\d{1,3}(?:\.\d{3}){0,5},\d{2} ?-?"
                return re.findall(padrao_valor, texto)

            # Inicializar listas para linhas, datas e valores
            linhas_processadas = []
            datas = []
            valores = []

            for linha in linhas:
                # Buscar todas as ocorrências de datas na linha
                datas_encontradas = extrair_datas(linha)
                if datas_encontradas:
                    # Adicionar a primeira data encontrada na coluna 'Data'
                    datas.append(datas_encontradas[0])
                    # Remover as datas da linha original
                    for data in datas_encontradas:
                        linha = linha.replace(data, "").strip()
                else:
                    datas.append(None)

                # Buscar todas as ocorrências de valores monetários na linha
                valores_encontrados = extrair_valores(linha)
                if valores_encontrados:
                    # Adicionar o primeiro valor encontrado na coluna 'Valor'
                    valores.append(valores_encontrados[0])
                    # Remover os valores da linha original
                    for valor in valores_encontrados:
                        linha = linha.replace(valor, "").strip()
                else:
                    valores.append(None)

                # Adicionar a linha processada sem datas e valores
                linhas_processadas.append(linha)

            # Criar DataFrame com as colunas reorganizadas
            df = pd.DataFrame(
                {'Data': datas, 'Histórico': linhas_processadas, 'Valor': valores})

            # Preencher células vazias na coluna 'Data' com o último valor válido
            df['Data'] = df['Data'].ffill()

            substituicoes_finais = {
            "+ " : "",
            " +" : "",
            "C/C" : "",
            "F ACIL FIRF CP AU" : "",
            "TR ANSF" : "TRANSF",
             "RESGA TE" : "RESGATE",
             "ELET CONT A" : "ELET CONTA",
             " P AGAMENTO" : " PAGAMENTO"
            }

            # Defina as substituições diretamente em um dicionário
            substituicoes = {
                "PACOTE EMPRES": "TARIFA BANCARIA",
    

            }

            
            # Criar um DataFrame com os dados extraídos
            remove_linha_contem = [
            "SALDO",
            "Total"
            ]

            for remove_linha in remove_linha_contem:
                df = df[~df["Histórico"].str.contains(remove_linha, case=False, na=False)]

            # Realize as substituições no DataFrame
            for padrao, substituicao in substituicoes.items():
                df.loc[df["Histórico"].str.contains(padrao, regex=False), "Histórico"] = substituicao

            
            for termo, substituto in substituicoes_finais.items():
                df["Histórico"] = df["Histórico"].str.replace(termo, substituto, regex=False)
            
            # Remover números da coluna "Histórico" diretamente no DataFrame
            df["Histórico"] = df["Histórico"].str.replace(r"\d+", "", regex=True)
            
            # Ajustar valores na coluna "Valor", movendo o "-" para a frente
            df["Valor"] = df["Valor"].str.replace(r"(\d{1,3}(?:\.\d{3})*,\d{2}) -", r"-\1", regex=True)


            
            df = df[~df["Valor"].isnull()]

            # Salvar no Excel
            nome_arquivo_excel = arquivo_escolhido.replace('.pdf', '.xlsx')
            contador = 1
            while os.path.exists(nome_arquivo_excel):
                nome_arquivo_excel = arquivo_escolhido.replace(
                    '.pdf', f'_{contador}.xlsx')
                contador += 1

            df.to_excel(nome_arquivo_excel, index=False)
            print(
                f"Arquivo Salvo '{nome_arquivo_excel}'")
        else:
            print("Escolha inválida. Por favor, tente novamente.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
