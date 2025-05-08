# Constantes
ROWS: int = 6
COLS: int = 7
EMPTY: int = 0
PLAYER_X: int = 1
PLAYER_O: int = 2


class Board:
    # Tabuleiro 7×6 do ConnectFour
    def __init__(self):
        self.board: list[list[int]] = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player: int = PLAYER_X
        self.winner: int | None = None
        self.last_move: tuple[int, int] | None = None  # Armazena a última jogada (row, col)

    def reset(self):
        """Limpa o tabuleiro e reinicia o jogo."""
        for r in range(ROWS):
            for c in range(COLS):
                self.board[r][c] = EMPTY
        self.current_player = PLAYER_X
        self.winner = None
        self.last_move = None

    def valid_moves(self) -> list[int]:
        """Colunas (0‑6) onde a primeira linha ainda está vazia."""
        return [c for c in range(COLS) if self.board[0][c] == EMPTY]

    def apply_move(self, column: int):
        """Solta peça na coluna.

        Levanta ``ValueError`` se coluna inválida ou cheia.
        Alterna ``current_player`` após inserir.
        """
        if column < 0 or column >= COLS:
            raise ValueError("Coluna fora do intervalo 0‑6.")
        if self.board[0][column] != EMPTY:
            raise ValueError("Coluna cheia – escolha outra.")

        # Encontrar a linha onde a peça vai cair
        row = ROWS - 1
        while row >= 0 and self.board[row][column] != EMPTY:
            row -= 1
        
        # Inserir a peça
        self.board[row][column] = self.current_player
        self.last_move = (row, column)  # Armazenar a última jogada

        # Verificar vitória após jogada - otimizado para verificar apenas a partir da última jogada
        self.winner = self.check_win_from_last_move()
        
        # Alternar jogador apenas se o jogo não terminou
        if not self.is_game_over():
            self.current_player = PLAYER_X if self.current_player == PLAYER_O else PLAYER_O

    def check_win_from_last_move(self) -> int | None:
        """Verifica vitória apenas a partir da última jogada."""
        if self.last_move is None:
            return None
            
        row, col = self.last_move
        player = self.board[row][col]
        
        # Verificar horizontal
        if self._check_direction(row, col, 0, 1, player) >= 4:
            return player
            
        # Verificar vertical
        if self._check_direction(row, col, 1, 0, player) >= 4:
            return player
            
        # Verificar diagonal \
        if self._check_direction(row, col, 1, 1, player) >= 4:
            return player
            
        # Verificar diagonal /
        if self._check_direction(row, col, 1, -1, player) >= 4:
            return player
            
        return None

    def _check_direction(self, row: int, col: int, dr: int, dc: int, player: int) -> int:
        """
        Conta peças contíguas na direção especificada.
        
        Args:
            row, col: Posição inicial
            dr, dc: Direção (deltas de linha e coluna)
            player: Jogador a verificar
            
        Returns:
            Número de peças contíguas
        """
        # Contar em direção positiva
        count = 1  # A peça atual
        
        # Contar em uma direção
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Contar na direção oposta
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
            
        return count

    def is_full(self) -> bool:
        """True se não restam movimentos válidos."""
        return all(self.board[0][c] != EMPTY for c in range(COLS))
        
    def is_draw(self) -> bool:
        """True se o jogo terminou em empate."""
        return self.is_full() and self.winner is None
        
    def is_game_over(self) -> bool:
        """True se o jogo terminou (vitória ou empate)."""
        return self.winner is not None or self.is_full()
        
    def get_winner(self) -> int | None:
        """Retorna o jogador vencedor (1 ou 2) ou None se não houver vencedor."""
        return self.winner

    def copy(self) -> "Board":
        """Cópia profunda – usada pelo MCTS para simulações."""
        new = Board()
        new.board = [row[:] for row in self.board]
        new.current_player = self.current_player
        new.winner = self.winner
        new.last_move = self.last_move
        return new

    # ------------------------------------------------------------------
    # Visualização
    # ------------------------------------------------------------------
    def render(self) -> str:
        """Retorna a representação em texto do tabuleiro."""
        symbols = {EMPTY: ".", PLAYER_X: "X", PLAYER_O: "O"}
        lines = [" ".join(symbols[cell] for cell in row) for row in self.board]
        header = " ".join(str(c) for c in range(COLS))
        return "\n".join(lines) + "\n" + header
        
    def display(self):
        """Exibe o tabuleiro atual no console."""
        print(self.render())
        
        # Exibir APENAS o próximo jogador, NÃO mostrar o resultado do jogo
        if not self.is_game_over():
            player_name = "X" if self.current_player == PLAYER_X else "O"
            print(f"Vez do jogador {player_name}")

    def __str__(self) -> str:  # noqa: DunderStr
        return self.render()

    def to_feature_vector(self) -> list[int]:
        """Converte o estado em lista 1‑D de 42 inteiros (para ID3)."""
        return [cell for row in self.board for cell in row]

    def check_win(self) -> int | None:
        """Retorna 1 ou 2 (X ou O) se alguém ganhou; caso contrário ``None`` (empty)."""
        return self.check_win_from_last_move()