""""

Script para:
 1. Simular N partidas de Connect Four entre MCTS (jogador X) e ID3 (jogador O);
 2. Gravar o vencedor de cada jogo num ficheiro text;
 3. Gerar:
    • Gráfico de pizza com a distribuição de vitórias;
    • Gráfico de linha com a taxa de vitória do MCTS em lotes de 10 jogos.
"""

import matplotlib.pyplot as plt
from game.game import Game
from ai.mcts import MCTS
from main import load_id3_model, id3_ai  # reaproveita as funções já escritas em main.py

def simulate_games(n_games: int, mcts_iterations: int) -> list[int]:
    """
    Simula n_games partidas e guarda o vencedor de cada uma.
    Retorna uma lista de inteiros: 1 para vitória do MCTS, 2 para vitória do ID3.
    """
    # 1) Carrega uma única vez o modelo ID3
    id3_model = load_id3_model()

    winners: list[int] = []

    for i in range(1, n_games + 1):
        game = Game()
        # 2) Joga até o fim
        while game.is_active():
            if game.board.current_player == 1:
                # MCTS faz a jogada quando for o 0
                #move = MCTS(iterations=mcts_iterations).best_move(game.board)
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
    """
    Gera um gráfico de pizza com a percentagem de vitórias de cada agente.
    """
    # Contagem simples
    count_mcts = winners.count(1)
    count_id3  = winners.count(2)
    labels = ["ID3 (X)","MCTS (0)"]
    sizes  = [count_mcts, count_id3]

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Distribuição de Vitórias: MCTS vs ID3")
    ax.axis("equal")  # círculos perfeitos
    plt.show()


if __name__ == "__main__":
    N_GAMES = 100   # trocar para o número desejado
    MCTS_ITERS = 300

    # Executa a simulação e gera os dois gráficos
    results = simulate_games(N_GAMES, MCTS_ITERS)
    plot_pie(results)
