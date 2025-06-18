import os
import xml.etree.ElementTree as ET
from openpyxl import Workbook
from datetime import datetime

def formatar_valor(valor):
    """
    Formata um número decimal no estilo brasileiro (com vírgula como separador decimal e ponto como separador de milhar).
    """
    try:
        # Converte o valor para float e aplica o formato
        return f"{float(valor):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    except (ValueError, TypeError):
        return valor  # Retorna o valor original caso não seja possível formatar

def formatar_cnpj(cnpj):
    # Remove qualquer caractere que não seja número
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    # Checa se o CNPJ tem 14 dígitos
    if len(cnpj) == 14:
        # Formata no padrão ##.###.###/####-##
        cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]} {cnpj[8:12]}-{cnpj[12:]}"
        return cnpj_formatado
    else:
        return "CNPJ inválido!"

def extrair_dados_xml(xml_file):
    """
    Extrai os dados de um arquivo XML com base na estrutura fornecida.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Adicionando suporte para namespaces
        namespace = {'ns': 'http://www.abrasf.org.br/nfse.xsd'}

        # Extração da data de emissão e conversão para dd/mm/aaaa
        data_emissao = root.findtext('.//ns:DataEmissao', default="", namespaces=namespace)
        if data_emissao:
            try:
                # Extrair e formatar a data
                data_emissao = datetime.strptime(data_emissao.split("T")[0], "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                print(f"Erro ao formatar a data no arquivo {xml_file}. Data original: {data_emissao}")
                data_emissao = ""

        # Extração dos valores, formatando apenas os numéricos no estilo brasileiro
        dados = {
            "Razao Social": root.findtext('.//ns:RazaoSocial', default="", namespaces=namespace),
            "Numero": root.findtext('.//ns:Numero', default="", namespaces=namespace),
            "Cnpj": formatar_cnpj(root.findtext('.//ns:Cnpj', default="", namespaces=namespace)),
            "Emissao": data_emissao,  # Data convertida
            "Valor Bruto": formatar_valor(root.findtext('.//ns:ValorServicos', default="0", namespaces=namespace)),
            "Pis": formatar_valor(root.findtext('.//ns:ValorPis', default="0", namespaces=namespace)),
            "Cofins": formatar_valor(root.findtext('.//ns:ValorCofins', default="0", namespaces=namespace)),
            "Inss": formatar_valor(root.findtext('.//ns:ValorInss', default="0", namespaces=namespace)),
            "Ir": formatar_valor(root.findtext('.//ns:ValorIr', default="0", namespaces=namespace)),
            "Csll": formatar_valor(root.findtext('.//ns:ValorCsll', default="0", namespaces=namespace)),
            "Iss": formatar_valor(root.findtext('.//ns:ValorIss', default="0", namespaces=namespace)),
            "Outras Ret.": formatar_valor(root.findtext('.//ns:OutrasRetencoes', default="0", namespaces=namespace)),
            "Liquido Nfse": formatar_valor(root.findtext('.//ns:ValorLiquidoNfse', default="0", namespaces=namespace))
        }
        return dados
    except Exception as e:
        print(f"Erro ao processar o arquivo {xml_file}: {e}")
        return None

def processar_xmls_para_excel():
    """
    Processa todos os XMLs na pasta e salva os dados em um arquivo Excel.
    """
    arquivos_xml = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.xml')]
    if not arquivos_xml:
        print("Nenhum arquivo XML encontrado.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Dados Extraídos"

    # Cabeçalho atualizado, com "Numero" entre "RazaoSocial" e "Emissao"
    colunas = [
        "Emissao", "Razao Social", "Cnpj", "Numero", "Valor Bruto", "Pis", "Cofins",
        "Inss", "Ir", "Csll", "Iss", "Outras Ret.", "Liquido Nfse"
    ]
    ws.append(colunas)

    # Processar cada XML e extrair os dados
    for arquivo in arquivos_xml:
        print(f"Processando: {arquivo}")
        dados = extrair_dados_xml(arquivo)
        if dados:
            ws.append([dados[coluna] for coluna in colunas])

    # Salvar o Excel
    wb.save("01 - dados_extraidos.xlsx")
    print("Dados salvos no arquivo 'dados_extraidos.xlsx'.")

if __name__ == "__main__":
    processar_xmls_para_excel()