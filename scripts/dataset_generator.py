import csv
import os
import sys
import time
from typing import Optional, List

# Garante que conseguimos importar os módulos do projeto
sys.path.append(os.path.dirname(__file__))

from game.game import Game
from ai.mcts import MCTS

# Diretório onde o CSV será salvo
DATA_DIR = os.path.join("../data")
os.makedirs(DATA_DIR, exist_ok=True)

# Simula uma partida usando Monte Carlo e retorna 42 colunas por linha indicando o movimento escolhido
# Iterations indica numero de simulaçoes por jogada
# Max Children indica o limite de filhos por nó
def generate_game(iterations: int, max_children: Optional[int]) -> List[List[int]]:
    engine = MCTS(iterations=iterations, max_children=max_children)
    game = Game()
    records: List[List[int]] = []

    # Enquanto o jogo estiver ativo
    while game.is_active():
        # Busca o estado do Board
        state = game.board.to_feature_vector()
        # Decide o melhor movimento pelo MCTS
        move = engine.best_move(game.board)
        # Append [estado + movimento] para o CSV
        records.append(state + [move])
        # Executa o movimento e continua simulaçoes
        game.make_move(move)

    return records

# Simula n_games de forma sequencial para gerar o dataset
def generate_dataset(
    n_games: int = 1000,
    iterations: int = 10000,
    max_children: Optional[int] = None,
    out_file: str = "connect4_dataset.csv"
) -> None:
    path = os.path.join(DATA_DIR, out_file)

    # Colocar o cabeçalho do csv
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        header = [f"cell_{i}" for i in range(42)] + ["move"]
        writer.writerow(header)

    # Gerar Jogos
    for idx in range(1, n_games + 1):
        records = generate_game(iterations, max_children)
        # Coloca os registros deste jogo ao final do CSV
        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(records)

        # Exibe progresso a cada 100 jogos (ou no final)
        if idx % 100 == 0 or idx == n_games:
            now = time.strftime("%H:%M:%S")
            print(f"[{now}] Jogos completados: {idx}/{n_games}")

    print(f"Dataset salvo em: {path}")

if __name__ == "__main__":
    # Exemplo de uso: 500 jogos, 5000 simulações por jogada, sem limite de expansão
    generate_dataset(n_games=20, iterations=50, max_children=None)
