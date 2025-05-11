import pandas as pd
import os
import matplotlib.pyplot as plt

# Caminho absoluto para o arquivo CSV
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'connect4_dataset.csv'))

try:
    # Carregar o arquivo CSV
    data = pd.read_csv(csv_path)
    print("Primeiras linhas do dataset:")
    print(data.head())
    print("\nInformações sobre o dataset:")
    print(data.info())
except Exception as e:
    print(f"Erro ao carregar o arquivo CSV: {e}")
    
# Contagem dos movimentos realizados em cada coluna
move_counts = data['move'].value_counts().sort_index()

# Plotar a distribuição dos movimentos
plt.figure(figsize=(8, 5))
plt.bar(move_counts.index, move_counts.values, color='skyblue')
plt.xlabel("Coluna")
plt.ylabel("Frequência de Movimentos")
plt.title("Distribuição dos Movimentos Feitos pela IA")
plt.xticks(range(7))  # Colunas de 0 a 6
plt.show()

