from typing import List, Optional
from .board import Board, PLAYER_X, PLAYER_O


class Game:
    # Classe responsável pela lógica do jogo Connect Four.
    # Gerencia o estado do jogo, histórico, jogadores e regras.
    def __init__(self):
        self.board = Board()
        self.player_names = {
            PLAYER_X: "Jogador X",
            PLAYER_O: "Jogador O"
        }
        self.current_game_active = True

    #Define nome dos jogadores
    def set_player_names(self, player_x_name: str, player_o_name: str):
        if player_x_name:
            self.player_names[PLAYER_X] = player_x_name
        if player_o_name:
            self.player_names[PLAYER_O] = player_o_name

    # Faz o movimento selecionado
    def make_move(self, column: int) -> bool:
        # Aplica o movimento
        self.board.apply_move(column)

        # Verificar se o jogo terminou após o movimento
        if self.board.is_game_over():
            self.current_game_active = False

        return True

    # Retorna lista com colunas disponiveis
    def get_valid_moves(self) -> List[int]:
        return self.board.valid_moves()

    # Retorna nome do jogador da Rodada
    def get_current_player_name(self) -> str:
        return self.player_names[self.board.current_player]

    # Retorna nome do vencedor
    def get_winner_name(self) -> Optional[str]:
        """Retorna o nome do vencedor ou None se não houver."""
        winner = self.board.get_winner()
        # Verificação para garantir que esta correto
        if winner and winner in self.player_names:
            return self.player_names[winner]
        return None

    # Verifica se o jogo acabou
    def is_game_over(self) -> bool:
        return self.board.is_game_over()

    # Verifica se terminou em empate
    def is_draw(self) -> bool:
        return self.board.is_draw()

    # Mostra tabuleiro no terminal
    def display_board(self):
        self.board.display()

    # Verifica se o jogo ta ativo
    def is_active(self) -> bool:
        return self.current_game_active