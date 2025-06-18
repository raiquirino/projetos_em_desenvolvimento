import tkinter as tk
from tkinter import messagebox

def encontrar_combinacoes_soma(lista_numeros, valor_alvo, combinacao_atual=[], inicio=0):
    if abs(sum(combinacao_atual) - valor_alvo) < 1e-9:
        return combinacao_atual
    for i in range(inicio, len(lista_numeros)):
        nova_combinacao = combinacao_atual + [lista_numeros[i]]
        resultado = encontrar_combinacoes_soma(lista_numeros, valor_alvo, nova_combinacao, i + 1)
        if resultado is not None:
            return resultado

def calcular_combinacoes():
    try:
        lista_numeros = list(map(float, entrada_lista.get().replace(',', '.').split()))
        valor_alvo = float(entrada_alvo.get().replace(',', '.'))
        # Filtrar os números maiores que o valor alvo
        lista_numeros = [num for num in lista_numeros if num <= valor_alvo]
        combinacao = encontrar_combinacoes_soma(lista_numeros, valor_alvo)
        if combinacao is not None:
            resultado_texto = ' '.join(map(lambda x: format(x, '.2f').replace('.', ','), combinacao))
            resultado_entry.delete(0, tk.END)  # Limpa o campo de texto
            resultado_entry.insert(0, resultado_texto)  # Insere o resultado
        else:
            resultado_entry.delete(0, tk.END)  # Limpa o campo de texto
            resultado_entry.insert(0, "HOJE NÃO")
    except ValueError:
        messagebox.showerror("Erro", "TU NÃO COLOCOU NADA MOÇO")

def inserir_novo_alvo():
    entrada_alvo.delete(0, tk.END)  # Limpa a entrada do valor alvo

def resetar():
    entrada_lista.delete(0, tk.END)  # Limpa a entrada da lista de números
    entrada_alvo.delete(0, tk.END)  # Limpa a entrada do valor alvo
    resultado_entry.delete(0, tk.END)  # Limpa o resultado

# Restante do código permanece igual

# Configuração da janela
janela = tk.Tk()
janela.title("Encontrar Combinações de Soma (Desenvolvido por Raí)")
janela.geometry("800x400")

# Crie um rótulo com a mensagem desejada
mensagem_label = tk.Label(janela, text="LISTA DE NÚMEROS")
mensagem_label.pack()

# Entrada de lista de números
entrada_lista = tk.Entry(janela, width=100)
entrada_lista.pack(pady=10)

# Crie um rótulo com a mensagem desejada
mensagem_label = tk.Label(janela, text="NUMERO ALVO")
mensagem_label.pack()

# Entrada do valor alvo
entrada_alvo = tk.Entry(janela)
entrada_alvo.pack(pady=10)

# Botão para calcular
calcular_botao = tk.Button(janela, text="Procurar", command=calcular_combinacoes)
calcular_botao.pack()

# Crie um rótulo com a mensagem desejada
mensagem_label = tk.Label(janela, text="LISTA ENCONTRADA")
mensagem_label.pack()

# Campo de texto para o resultado
resultado_entry = tk.Entry(janela, width=100)
resultado_entry.pack(pady=10)

# Botão para inserir novo número alvo
novo_alvo_botao = tk.Button(janela, text="Inserir Novo Alvo", command=inserir_novo_alvo)
novo_alvo_botao.pack()

# Botão para resetar
resetar_botao = tk.Button(janela, text="Resetar", command=resetar)
resetar_botao.pack(pady=10)

# Crie um rótulo com a mensagem desejada
mensagem_label = tk.Label(janela, text="Não se desanime com a derrota de hoje, porque amanhã tem mais.")
mensagem_label.pack()

# Crie um rótulo com a mensagem desejada
mensagem_label = tk.Label(janela, text="AQUI É O RAÍ RAPAZ!!!")
mensagem_label.pack(pady=25)

janela.mainloop()
