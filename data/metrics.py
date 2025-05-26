import matplotlib.pyplot as plt
from game.game import Game
from ai.mcts import MCTS
from main import load_id3_model, id3_ai

def simulate_games(n_games: int, mcts_iterations: int) -> list[int]:

    # 1) Carrega uma única vez o modelo ID3
    id3_model = load_id3_model()

    winners: list[int] = []

    for i in range(1, n_games + 1):
        game = Game()
        while game.is_active():
            if game.board.current_player == 1:
                # MCTS faz a jogada quando for o 0
                # move = MCTS(iterations=mcts_iterations).best_move(game.board)
                move = id3_ai(game, id3_model)
            else:
                # ID3 faz a jogada quando for o X
                #move = id3_ai(game, id3_model)
                move = MCTS(iterations=mcts_iterations).best_move(game.board)
            game.make_move(move)

        # Ao terminar, guarda quem ganhou (1 ou 2)
        winners.append(game.board.get_winner())

    print(f"✓ Simulação concluída: {n_games} jogos.")
    return winners


def plot_pie(winners: list[int]) -> None:

    # Contagem simples
    count_mcts = winners.count(1)
    count_id3  = winners.count(2)
    labels = ["ID3 (X)","MCTS (0)"]
    sizes  = [count_mcts, count_id3]

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Distribuição de Vitórias: MCTS vs ID3")
    ax.axis("equal")
    plt.show()


if __name__ == "__main__":
    N_GAMES = 100
    MCTS_ITERS = 300

    results = simulate_games(N_GAMES, MCTS_ITERS)
    plot_pie(results)
