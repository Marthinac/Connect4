import os
import time
from typing import Optional

class UI:
    """
    Classe responsável pela interface do usuário do jogo Connect Four.
    Gerencia a interação com o usuário, exibição de menus e do tabuleiro.
    """
    def __init__(self, game):
        self.game = game

    # Clear do Console
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Exibe boas-vindas e regras do jogo
    def print_welcome(self):
        self.clear_screen()
        print("=" * 56)
        print("       BEM-VINDO AO JOGO CONNECT FOUR (CONECTA 4)       ")
        print("=" * 56)
        print("\nRegras:")
        print("1. Dois jogadores alternam entre colocar peças no tabuleiro")
        print("2. O objetivo é conectar 4 peças na horizontal, vertical ou diagonal")
        print("3. O primeiro jogador a conectar 4 peças vence")
        print("4. Se o tabuleiro ficar cheio sem vencedor, é um empate")
        print("\nControles:")
        print("- Digite o número da coluna (0-6) para colocar uma peça")

    # Solicita nome dos jogadores
    def get_player_names(self, mode: int):
        self.clear_screen()
        print("Configuração dos Jogadores\n")
        if mode == 1:
            player_x = input("Nome do Jogador X: ")
            player_o = input("Nome do Jogador O: ")
        elif mode == 2:
            player_x = input("Nome do Jogador X: ")
            player_o = "Computador"
        else:
            player_x = "Computador 1"
            player_o = "Computador 2"

        self.game.set_player_names(player_x, player_o)

    # Solicita o modo de jogo(PvP, PvIA, IAvIA)
    def get_game_mode(self) -> int:
        self.clear_screen()
        print("Selecione o modo de jogo:")
        print(" 1 - Humano vs Humano")
        print(" 2 - Humano vs Computador")
        print(" 3 - Computador vs Computador")
        while True:
            choose = input("Modo [1/2/3]: ").strip()
            if choose in ("1", "2", "3"):
                return int(choose)
            print("Opção inválida. Digite 1, 2 ou 3.")

    # Solicita o movimento do jogador(0 a 6)
    def get_move(self) -> Optional[int]:
        current_player_name = self.game.get_current_player_name()
        valid_moves = self.game.get_valid_moves()

        while True:
            move_str = input(f"\n{current_player_name}, escolha uma coluna (0-6): ")

            # Verifica se todos caracter é dígito
            if not move_str.isdigit():
                print("Entrada inválida. Digite um número entre 0 e 6")
                continue

            column = int(move_str)
            # Verifica se a coluna escolhida ta entre os movimentos válidos
            if column not in valid_moves:
                print(f"Coluna {column} não está disponível. Escolha uma das colunas: {valid_moves}")
                continue

            return column

    # Mostra resultado do Jogo
    def show_game_result(self):
        if self.game.is_game_over():
            if self.game.is_draw():
                print("\nO jogo terminou em empate!")
            else:
                winner_name = self.game.get_winner_name()
                print(f"\nParabéns! {winner_name} venceu!")
    

    # Mostra o estado do jogo
    def display_game(self):
        self.clear_screen()
        print(f"{self.game.player_names[1]} (X) vs {self.game.player_names[2]} (O)\n")  # PLAYER_X = 1, PLAYER_O = 2
        
        # Exibir tabuleiro
        self.game.display_board()
        
        # Se o jogo terminou, mostrar o resultado
        if self.game.is_game_over():
            self.show_game_result()

    # Mensagem de erro para movimentos invalidos
    def show_move_error(self, error_message: str):
        print(f"Erro: {error_message}")
        time.sleep(1.5)