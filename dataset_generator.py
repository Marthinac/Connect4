# dataset_generator.py
import csv, os, sys, time
from multiprocessing import Pool, cpu_count

sys.path.append(os.path.dirname(__file__))       # raiz do projecto
from game.game import Game                        # nossa lógica de jogo
from ai.mcts import MCTS                              # busca adversária

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_jogo(args):
    """
    Função executada em cada processo:
    simula uma partida completa usando MCTS e
    retorna todas as linhas [42 estados + movimento].
    """
    iters, _ = args
    engine = MCTS(iterations=iters)
    game   = Game()
    linhas = []
    while game.is_active():
        estado   = game.board.to_feature_vector()
        movimento = engine.best_move(game.board)
        linhas.append(estado + [movimento])
        game.make_move(movimento)
    return linhas

def generate_dataset(n_games: int = 1_000,
                     iters:    int = 500,
                     out_file: str = "connect4_dataset.csv") -> None:
    """
    Gera n_games partidas Connect-Four por auto-jogo MCTS
    em paralelo usando todos os núcleos disponíveis,
    e grava (estado, movimento) em CSV.
    """
    path = os.path.join(DATA_DIR, out_file)

    # Cria o CSV com o cabeçalho
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        header = [f"cell_{i}" for i in range(42)] + ["move"]
        writer.writerow(header)

    # Prepara o pool de processos
    n_processes = cpu_count()  # aproveita todos os núcleos
    pool = Pool(processes=n_processes)
    print(f"🧵 Iniciando geração em paralelo com {n_processes} processos...")

    # mapeia cada tarefa (iters, idx) para um processo
    # usamos enumerate só para feedback de progresso
    for idx, linhas in enumerate(pool.imap(gerar_jogo, [(iters, i) for i in range(n_games)], chunksize=1), start=1):
        # abre em append e escreve todas as linhas desse jogo
        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(linhas)

        if idx % 100 == 0:
            print(f"[{time.strftime('%H:%M:%S')}] completos {idx}/{n_games} jogos")

    pool.close()
    pool.join()

    print(f"✅ Dataset paralelo salvo em: {path}")

if __name__ == "__main__":
    generate_dataset()
