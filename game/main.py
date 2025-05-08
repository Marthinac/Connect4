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
    ui.get_player_names()
    
    playing = True
    
    while playing:
        # Reiniciar para um novo jogo
        game.reset()
        
        # Loop principal do jogo
        while game.is_active():
            # Exibir o estado atual
            ui.display_game()                
            # Solicitar movimento
            move = ui.get_move()
            
            # Processar comandos especiais
            if move is None:  # Sair do jogo
                return
            elif move == -1:  # Reiniciar
                break
            elif move == -2:  # Ver histórico
                ui.show_game_history()
                continue
                
            # Aplicar o movimento
            try:
                game.make_move(move)
            except ValueError as e:
                ui.show_move_error(str(e))
        
        ui.display_game()    
        #ui.show_game_result()
       
        if not ui.play_again():
            break
    
    # Mostrar histórico ao final
    ui.show_game_history()
    print("\nObrigado por jogar Connect Four!")

if __name__ == "__main__":
    main()