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
        print("- Digite 'q' para sair do jogo a qualquer momento")
        print("- Digite 'r' para reiniciar o jogo")
        print("- Digite 'h' para ver o histórico de jogos")
        print("\nPressione Enter para começar ou 'q' para sair...")
        choice = input().strip().lower()
        if choice == 'q':
            exit()
        
    def get_player_names(self):
        """Solicita os nomes dos jogadores e os configura no jogo."""
        self.clear_screen()
        print("Configuração dos Jogadores\n")
        
        name1 = input("Nome do Jogador X: ").strip()
        name2 = input("Nome do Jogador O: ").strip()
        
        self.game.set_player_names(name1, name2)
            
    def get_move(self) -> Optional[int]:
        """
        Solicita um movimento do jogador atual.
        
        Returns:
            int: Número da coluna (0-6)
            None: Para sair do jogo
            -1: Para reiniciar o jogo
            -2: Para ver o histórico
        """
        current_player_name = self.game.get_current_player_name()
        valid_moves = self.game.get_valid_moves()
        
        while True:
            try:
                move = input(f"\n{current_player_name}, escolha uma coluna (0-6), 'q' para sair, 'r' para reiniciar ou 'h' para histórico: ")
                
                # Verificar comandos especiais
                if move.lower() == 'q':
                    return None
                elif move.lower() == 'r':
                    return -1
                elif move.lower() == 'h':
                    return -2
                
                # Converter para inteiro e validar
                column = int(move)
                if column not in valid_moves:
                    print(f"Coluna {column} não está disponível. Escolha uma das colunas: {valid_moves}")
                    continue
                
                return column
                
            except ValueError:
                print("Entrada inválida. Digite um número entre 0 e 6, 'q', 'r' ou 'h'.")
    
    def show_game_history(self):
        """Exibe o histórico de jogos."""
        self.clear_screen()
        print("=" * 50)
        print("               HISTÓRICO DE JOGOS                ")
        print("=" * 50)
        
        history = self.game.get_game_history()
        
        if not history:
            print("\nNenhum jogo registrado.")
        else:
            for i, game in enumerate(history, 1):
                print(f"\nJogo #{i} - {game['timestamp']}")
                print(f"Jogador X: {game['players'][1]}")  # PLAYER_X = 1
                print(f"Jogador O: {game['players'][2]}")  # PLAYER_O = 2
                print(f"Resultado: {game['result']}")
        
        print("\nPressione Enter para voltar...")
        input()
    
    def show_game_result(self):
        """Exibe o resultado do jogo atual."""
        if self.game.is_game_over():
            if self.game.is_draw():
                print("\nO jogo terminou em empate!")
            else:
                winner_name = self.game.get_winner_name()
                print(f"\nParabéns! {winner_name} venceu!")
    
    def play_again(self) -> bool:
        """Pergunta se os jogadores querem jogar novamente."""
        while True:
            choice = input("\nDeseja jogar novamente? (s/n): ").lower()
            if choice in ['s', 'sim', 'y', 'yes']:
                return True
            elif choice in ['n', 'não', 'nao', 'no']:
                return False
            else:
                print("Entrada inválida. Digite 's' para sim ou 'n' para não.")
    
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