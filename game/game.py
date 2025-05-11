from typing import List, Optional
from .board import Board, PLAYER_X, PLAYER_O


class Game:
    """
    Classe responsável pela lógica do jogo Connect Four.
    Gerencia o estado do jogo, histórico, jogadores e regras.
    """
    def __init__(self):
        self.board = Board()
        self.player_names = {
            PLAYER_X: "Jogador X",
            PLAYER_O: "Jogador O"
        }
        self.current_game_active = True
        
    def reset(self):
        """Reinicia o tabuleiro e prepara para um novo jogo."""
        self.board.reset()
        self.current_game_active = True
        
    def set_player_names(self, player_x_name: str, player_o_name: str):
        """Define os nomes dos jogadores."""
        if player_x_name:
            self.player_names[PLAYER_X] = player_x_name
        if player_o_name:
            self.player_names[PLAYER_O] = player_o_name
            
    def make_move(self, column: int) -> bool:
        """
        Aplica o movimento na coluna selecionada.
        
        Args:
            column: Número da coluna (0-6)
            
        Returns:
            True se o movimento foi válido, False caso contrário
            
        Raises:
            ValueError: Se o movimento for inválido
        """
        try:
            self.board.apply_move(column)
            
            # Verificar se o jogo terminou após o movimento
            if self.board.is_game_over():
                self.current_game_active = False
                
            return True
        except ValueError as e:
            raise
    
    def get_valid_moves(self) -> List[int]:
        """Retorna lista de movimentos válidos (colunas disponíveis)."""
        return self.board.valid_moves()
    
    def get_current_player_name(self) -> str:
        """Retorna o nome do jogador atual."""
        return self.player_names[self.board.current_player]
    
    def get_winner_name(self) -> Optional[str]:
        """Retorna o nome do vencedor ou None se não houver."""
        winner = self.board.get_winner()
        
        # Verificação explícita para garantir que obtemos o nome correto
        if winner and winner in self.player_names:
            return self.player_names[winner]
        return None
    
    def is_game_over(self) -> bool:
        """Verifica se o jogo terminou."""
        return self.board.is_game_over()
    
    def is_draw(self) -> bool:
        """Verifica se o jogo terminou em empate."""
        return self.board.is_draw()
    

    def get_board_state(self) -> str:
        """Retorna a representação em string do estado atual do tabuleiro."""
        return self.board.render()
    
    def display_board(self):
        """Exibe o tabuleiro no console."""
        self.board.display()
    
    def is_active(self) -> bool:
        """Verifica se o jogo atual está ativo."""
        return self.current_game_active