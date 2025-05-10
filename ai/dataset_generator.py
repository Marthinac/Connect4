import csv
import os
import sys

# Garantindo que os módulos sejam encontrados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'game')))

from mcts import MCTS
from game import Game

def generate_dataset(num_games=1000, output_file='connect4_dataset.csv'):
    """
    Gera um conjunto de dados simulando partidas de Connect Four usando MCTS.
    Args:
        num_games: Número de partidas simuladas.
        output_file: Nome do arquivo CSV para salvar os dados.
    """
    # Caminho absoluto para a pasta 'data'
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, output_file)

    print(f"Salvando arquivo em: {output_path}")
    
    try:
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Corrigindo o cabeçalho
            header = [f'cell_{i}' for i in range(42)] + ['move']
            writer.writerow(header)
            
            print(f"Arquivo {output_path} criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar o arquivo: {e}")

if __name__ == "__main__":
    generate_dataset(num_games=1000)

        