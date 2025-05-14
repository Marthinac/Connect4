import csv
import os
import sys
import time
from multiprocessing import Pool, cpu_count
from typing import Optional, Tuple, List

# Adiciona raiz do projeto ao path para importar módulos
sys.path.append(os.path.dirname(__file__))

from game.game import Game                # lógica do jogo Connect-Four
from ai.mcts import MCTS                  # algoritmo MCTS+UCT

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def gerar_jogo(args: Tuple[int, Optional[int]]) -> List[List[int]]:
    """
    Simula uma partida completa usando MCTS e retorna uma lista de linhas:
    [42 valores do estado] + [movimento escolhido]

    :param args: tupla (iterations, max_children)
    """
    iterations, max_children = args
    engine = MCTS(iterations=iterations, max_children=max_children)
    game = Game()
    linhas: List[List[int]] = []

    while game.is_active():
        estado = game.board.to_feature_vector()
        movimento = engine.best_move(game.board)
        linhas.append(estado + [movimento])
        game.make_move(movimento)

    return linhas


def generate_dataset(
    n_games: int = 1000,
    iterations: int = 10000,
    k: Optional[int] = None,
    out_file: str = "connect4_dataset.csv"
) -> None:
    """
    Gera `n_games` partidas de Connect-Four em paralelo usando MCTS,
    gravando cada par (estado, movimento) em CSV.

    :param k: número máximo de filhos por nó (None = expansão total)
    """
    path = os.path.join(DATA_DIR, out_file)

    # Escrever cabeçalho
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        header = [f"cell_{i}" for i in range(42)] + ["move"]
        writer.writerow(header)

    n_processes = cpu_count()
    pool = Pool(processes=n_processes)
    print(f"🧵 Iniciando geração em paralelo com {n_processes} processos...")

    # Prepara tarefas: cada tupla é (iterations, k)
    tarefas = [(iterations, k) for _ in range(n_games)]

    for idx, linhas in enumerate(
        pool.imap(gerar_jogo, tarefas, chunksize=1),
        start=1
    ):
        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(linhas)

        if idx % 100 == 0:
            print(f"[{time.strftime('%H:%M:%S')}] completos {idx}/{n_games} jogos")

    pool.close()
    pool.join()
    print(f"✅ Dataset salvo em: {path}")


if __name__ == "__main__":
    # Exemplo de uso básico; altera k conforme desejado
    generate_dataset(n_games=3000, iterations=600, k=5)  # k=None expande todos os filhos
