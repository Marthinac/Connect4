
import csv, os, sys, random, time
sys.path.append(os.path.dirname(__file__))           # raiz do projecto
from game.game import Game                                # nossa lógica de jogo
from ai.mcts import MCTS                                # busca adversária


def generate_dataset(n_games: int = 1_000,
                     iters: 500 = 500,
                     out_file: str = "data/connect4_dataset.csv") -> None:
    """
    Gera *n_games* partidas Connect-Four por auto-jogo MCTS
    e grava (estado, movimento recomendado) em CSV.

    Cada linha tem 42 colunas chamadas cell_0 … cell_41
    + coluna 'move' com o número da coluna (0-6).
    """
    mcts_engine = MCTS(iterations=iters)

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        header = [f"cell_{i}" for i in range(42)] + ["move"]
        writer.writerow(header)

        for g in range(n_games):
            game = Game()                # novo tabuleiro
            while game.is_active():
                state_vec = game.board.to_feature_vector()
                best = mcts_engine.best_move(game.board)
                writer.writerow(state_vec + [best])
                game.make_move(best)     # aplica jogada
            if g % 100 == 0:
                print(f"[{time.strftime('%H:%M:%S')}] jogo {g}/{n_games}")

    print(f" Dataset salvo em {out_file}")

if __name__ == "__main__":
    generate_dataset()
