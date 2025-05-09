from game import Game
from ui import UI
import time

def main():
    """
    Função principal que inicia o jogo Connect Four.
    Gerencia o fluxo principal do jogo e a interação entre as classes Game e UI.
    """
    # Inicializar o jogo e a interface
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
    # Quando tivermos o algoritmo da IA pronto vai ser trocado random_ai por algo como mctr.get_move()
    elif mode == 2:  # Humano vs IA
        agentes = {
            1: ui.get_move,
            2: random_ai
        }
    else:  # IA vs IA
        agentes = {
            1: random_ai,
            2: random_ai
        }
    # Só pergunta nome se houver algum jogador humano
    if mode != 3:
        ui.get_player_names(mode)
    
    # Loop principal do jogo
    while game.is_active():
        # Exibir o estado atual
        ui.display_game()
        # Solicitar movimento
        move = ui.get_move()


        # Aplicar o movimento
        try:
            game.make_move(move)
        except ValueError as e:
            ui.show_move_error(str(e))
        
    ui.display_game()

    print("\nObrigado por jogar Connect Four!")

if __name__ == "__main__":
    main()