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
        
    def clear_screen(self):
        """Limpa a tela do console."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_welcome(self):
        """Exibe mensagem de boas-vindas e regras do jogo."""
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

        
    def get_player_names(self, mode: int):
        """Solicita os nomes dos jogadores e os configura no jogo."""
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

    def get_game_mode(self) -> int:
        """
        Pergunta qual o modo de jogo:
         1 - Humano vs Humano
         2 - Humano vs Computador
         3 - Computador vs Computador
        Retorna 1, 2 ou 3.
        """
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

    def get_move(self) -> Optional[int]:
        """
        Solicita um movimento do jogador atual.
        
        Returns:
            int: Número da coluna (0-6)
           """
        current_player_name = self.game.get_current_player_name()
        valid_moves = self.game.get_valid_moves()
        
        while True:
            try:
                move = input(f"\n{current_player_name}, escolha uma coluna (0-6)")
                # Converter para inteiro e validar
                column = int(move)
                if column not in valid_moves:
                    print(f"Coluna {column} não está disponível. Escolha uma das colunas: {valid_moves}")
                    continue
                
                return column
                
            except ValueError:
                print("Entrada inválida. Digite um número entre 0 e 6")
    

    def show_game_result(self):
        """Exibe o resultado do jogo atual."""
        if self.game.is_game_over():
            if self.game.is_draw():
                print("\nO jogo terminou em empate!")
            else:
                winner_name = self.game.get_winner_name()
                print(f"\nParabéns! {winner_name} venceu!")
    

    
    def display_game(self):
        """Exibe o estado atual do jogo, incluindo o tabuleiro e informações dos jogadores."""
        self.clear_screen()
        print(f"{self.game.player_names[1]} (X) vs {self.game.player_names[2]} (O)\n")  # PLAYER_X = 1, PLAYER_O = 2
        
        # Exibir tabuleiro
        self.game.display_board()
        
        # Se o jogo terminou, mostrar o resultado
        if self.game.is_game_over():
            self.show_game_result()
    
    def show_move_error(self, error_message: str):
        """Exibe mensagem de erro para movimentos inválidos."""
        print(f"Erro: {error_message}")
        time.sleep(1.5)  # Pausa para o usuário ler a mensagem