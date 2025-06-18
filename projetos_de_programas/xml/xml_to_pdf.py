import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def remove_namespace(tree):
    """Remove namespaces do XML para facilitar a busca de elementos."""
    for elem in tree.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]  # Remove o namespace
    return tree

def parse_any_xml(xml_file):
    """Extrai **todos** os dados de qualquer XML, independentemente da estrutura."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Remove namespaces
        tree = remove_namespace(tree)

        # Extrai **todos** os dados disponíveis no XML
        dados_xml = {"arquivo": os.path.basename(xml_file)}
        for elem in root.iter():
            if elem.text and elem.text.strip():  # Ignora elementos vazios
                dados_xml[elem.tag] = elem.text.strip()

        return dados_xml
    
    except ET.ParseError:
        print(f"Erro ao processar {xml_file}. O arquivo pode estar corrompido ou não ser um XML válido.")
        return None

def generate_pdf(data, output_file):
    """Gera um PDF com **todos** os dados do XML."""
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, f"Dados do XML - {data['arquivo']}")

    c.setFont("Helvetica", 12)
    y_position = height - 80

    for key, value in data.items():
        if key != "arquivo":  # Evita repetir o nome do arquivo no PDF
            c.drawString(50, y_position, f"{key}: {value}")
            y_position -= 20  # Ajusta a posição vertical

    c.showPage()
    c.save()

def process_folder(folder_path):
    """Processa todos os arquivos XML na pasta e gera PDFs."""
    print(f"Processando arquivos na pasta: {folder_path}")
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            xml_file = os.path.join(folder_path, filename)
            pdf_file = os.path.join(folder_path, filename.replace(".xml", ".pdf"))

            print(f"Processando {xml_file}...")
            dados_xml = parse_any_xml(xml_file)
            if dados_xml:
                generate_pdf(dados_xml, pdf_file)
                print(f"PDF gerado: {pdf_file}")

# Define a pasta como o diretório atual
folder_path = os.getcwd()
process_folder(folder_path)