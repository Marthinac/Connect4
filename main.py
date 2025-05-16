import os
import sys
import pickle
import pandas as pd
from ai.mcts import MCTS
from game.game import Game
from game.ui import UI

sys.path.append(os.path.join(os.path.dirname(__file__), "ai"))

#Carrega o Modelo treinado
def load_id3_model():
    model_path = os.path.join("ai/models/id3_model.pkl")

    # Carrega o modelo ID3
    with open(model_path, "rb") as file:
        model = pickle.load(file)

    return model


# Lê o Estado do Jogo e com base nesse estado usa o modelo para prever e devolver o melhor movimento
def id3_ai(game_state, id3_model):
    board_state = game_state.board.to_feature_vector()
    board_df = pd.DataFrame([board_state], columns=[f'cell_{i}' for i in range(42)])
    prediction = id3_model.predict(board_df)
    return int(prediction[0])

#Instancia o Monte Carlo e com base no estado do board devolve a jogada considerada ótima
def mcts_ai(game_state):
    mcts = MCTS(iterations=300)
    return mcts.best_move(game_state.board)


def main():
    """
    Função principal que inicia o jogo Connect Four.
    Gerencia o fluxo principal do jogo e a interação entre as classes Game e UI.
    """

    # Carregar o modelo ID3
    id3_model = load_id3_model()

    # Inicializar jogo e interface
    game = Game()
    ui = UI(game)

    # Exibir boas-vindas e configurar jogadores
    ui.print_welcome()
    mode = ui.get_game_mode()

    if mode == 1:  # Humano vs Humano
        agentes = {
            1: ui.get_move,
            2: ui.get_move
        }
    elif mode == 2:  # Humano vs IA
        agentes = {
            1: ui.get_move,
            2: lambda: mcts_ai(game)
        }
    else:  # IA vs IA
        agentes = {
            1: lambda: mcts_ai(game),
            2: lambda: id3_ai(game, id3_model)
        }

    # Só pergunta nome se houver algum jogador humano
    if mode != 3:
        ui.get_player_names(mode)

    # Loop principal do jogo
    while game.is_active():
        # Exibir o estado atual
        ui.display_game()
        # Solicitar movimento e aplicar diretamente
        move = agentes[game.board.current_player]()
        game.make_move(move)

    ui.display_game()
    print("\nObrigado por jogar Connect Four!")


if __name__ == "__main__":
    main()