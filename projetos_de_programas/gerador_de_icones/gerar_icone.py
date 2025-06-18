import os
from PIL import Image

def transformar_em_icone(nome_arquivo, tamanho=(64, 64)):
    """
    Transforma uma imagem em um ícone no formato .ico.

    :param nome_arquivo: Nome do arquivo de imagem a ser transformado.
    :param tamanho: Tamanho do ícone (largura, altura). Padrão: (64, 64).
    """
    try:
        # Abrir a imagem diretamente da pasta atual
        imagem = Image.open(nome_arquivo)

        # Redimensionar a imagem para o tamanho desejado usando LANCZOS para resampling
        imagem = imagem.resize(tamanho, Image.Resampling.LANCZOS)

        # Definir o nome do ícone com o mesmo nome da imagem, mas extensão .ico
        nome_icone = f"{os.path.splitext(nome_arquivo)[0]}.ico"

        # Salvar a imagem como ícone na mesma pasta
        imagem.save(nome_icone, format="ICO")
        print(f"Ícone salvo em: {nome_icone}")
    except Exception as e:
        print(f"Erro ao transformar a imagem em ícone: {e}")

def listar_arquivos_imagem():
    """
    Lista todos os arquivos de imagem na pasta atual.
    :return: Lista de arquivos com extensões de imagem suportadas.
    """
    extensoes_suportadas = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    return [f for f in os.listdir() if f.lower().endswith(extensoes_suportadas)]

if __name__ == "__main__":
    # Listar os arquivos de imagem na pasta atual
    arquivos_imagem = listar_arquivos_imagem()

    if not arquivos_imagem:
        print("Nenhuma imagem encontrada na pasta atual.")
    else:
        print("Arquivos de imagem disponíveis:")
        for i, arquivo in enumerate(arquivos_imagem, start=1):
            print(f"{i}. {arquivo}")

        # Solicitar ao usuário que escolha um arquivo
        escolha = input("Digite o número do arquivo que você deseja transformar em ícone: ")

        try:
            indice = int(escolha) - 1  # Convertendo a entrada para índice
            if 0 <= indice < len(arquivos_imagem):
                arquivo_escolhido = arquivos_imagem[indice]
                print(f"Você escolheu: {arquivo_escolhido}")

                # Transformar o arquivo escolhido em ícone
                transformar_em_icone(arquivo_escolhido)
            else:
                print("Escolha inválida.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")