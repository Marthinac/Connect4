# Constantes
ROWS: int = 6
COLS: int = 7
EMPTY: int = 0
PLAYER_X: int = 1
PLAYER_O: int = 2


class Board:
    #Tabuleiro 7×6 do ConnectFour
    def __init__(self):
        self.board: list[list[int]] = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player: int = PLAYER_X
        self.winner = None


    def reset(self):
        """Limpa o tabuleiro e reinicia o jogo."""
        for r in range(ROWS):
            for c in range(COLS):
                self.board[r][c] = EMPTY
        self.current_player = PLAYER_X

    def valid_moves(self) -> list[int]:
        """Colunas (0‑6) onde a primeira linha ainda está vazia."""
        return [c for c in range(COLS) if self.board[0][c] == EMPTY]

    def make_move(self, column: int) -> None:
        """
        alias function para padronizar em board e game
        """
        self.apply_move(column)

    def apply_move(self, column: int):
        """Solta peça na *column*.
        Levanta ``ValueError`` se coluna inválida ou cheia.
        Alterna ``current_player`` após inserir.
        """
        if column not in range(COLS):
            raise ValueError("Coluna fora do intervalo 0‑6.")
        if self.board[0][column] != EMPTY:
            raise ValueError("Coluna cheia – escolha outra.")

        for row in range(ROWS - 1, -1, -1):
            if self.board[row][column] == EMPTY:
                self.board[row][column] = self.current_player
                break

        self.current_player = PLAYER_X if self.current_player == PLAYER_O else PLAYER_O
        self.winner = self.check_win()

    def check_win(self) -> int | None:
        """Retorna 1 ou 2 se alguém ganhou; caso contrário ``None``."""
        for player in (PLAYER_X, PLAYER_O):
            if (
                self._four_horizontal(player)
                or self._four_vertical(player)
                or self._four_diagonal(player)
            ):
                return player
        return None

    def is_full(self) -> bool:
        """True se não restam movimentos válidos."""
        return all(self.board[0][c] != EMPTY for c in range(COLS))

    def is_game_over(self):
        return self.winner is not None or self.is_full()

    def is_draw(self):
        return self.is_full() and self.winner is None

    def get_winner(self) -> int | None:
        """Retorna o jogador vencedor (1 ou 2) ou None se não houver vencedor."""
        return self.winner

    def copy(self) -> "Board":
        """Cópia profunda – usada pelo MCTS para simulações."""
        new = Board()
        new.board = [row[:] for row in self.board]
        new.current_player = self.current_player
        new.winner = self.winner          # <-- correcção crucial
        return new

    def to_feature_vector(self) -> list[int]:
        """Converte o estado em lista 1‑D de 42 inteiros (para ID3)."""
        return [cell for row in self.board for cell in row]

    # Visualização
    def render(self) -> str:
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

    #Checa Horizontal
    def _four_horizontal(self, player: int) -> bool:
        for r in range(ROWS):
            consecutive = 0
            for c in range(COLS):
                consecutive = consecutive + 1 if self.board[r][c] == player else 0
                if consecutive == 4:
                    return True
        return False
    #Checa Vertical
    def _four_vertical(self, player: int) -> bool:
        for c in range(COLS):
            consecutive = 0
            for r in range(ROWS):
                consecutive = consecutive + 1 if self.board[r][c] == player else 0
                if consecutive == 4:
                    return True
        return False

    # Checa Diagonais
    def _four_diagonal(self, player: int) -> bool:
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r + i][c + i] == player for i in range(4)):
                    return True
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.board[r - i][c + i] == player for i in range(4)):
                    return True
        return False