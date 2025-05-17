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


    # Devolve as colunas em que ainda tem posições disponíveis
    def valid_moves(self) -> list[int]:
        return [c for c in range(COLS) if self.board[0][c] == EMPTY]

    # "Solta" peça na coluna
    def apply_move(self, column: int):
        if column not in range(COLS):
            print(f"Coluna fora do intervalo 0‑6.")
        if self.board[0][column] != EMPTY:
            print(f"Coluna cheia – escolha outra.")

        for row in range(ROWS - 1, -1, -1):
            if self.board[row][column] == EMPTY:
                self.board[row][column] = self.current_player
                break
        #
        self.current_player = PLAYER_X if self.current_player == PLAYER_O else PLAYER_O
        self.winner = self.check_win()

    # Checa se houve vencedor na ultima rodada
    # None caso nao tenha vencedor
    def check_win(self) -> int | None:
        for player in (PLAYER_X, PLAYER_O):
            if (
                self._four_horizontal(player)
                or self._four_vertical(player)
                or self._four_diagonal(player)
            ):
                return player
        return None

    # Devolve se o tabuleiro está cheio
    def is_full(self) -> bool:
        return all(self.board[0][c] != EMPTY for c in range(COLS))

    # Devolve se o jogo acabou ou não
    def is_game_over(self):
        return self.winner is not None or self.is_full()

    # Devolve se o jogo terminou empatado
    def is_draw(self):
        return self.is_full() and self.winner is None

    # Retorna o vencedor ou None caso nao haja
    def get_winner(self) -> int | None:
        return self.winner

    # Cópia usada pelo Monte Carlo para fazer simulações
    def copy(self) -> "Board":
        new = Board()
        new.board = [row[:] for row in self.board]
        new.current_player = self.current_player
        new.winner = self.winner          # <-- correcção crucial
        return new

    # Prepara o tabuleiro para a modelagem da ID3
    def to_feature_vector(self) -> list[int]:
        """Converte o estado em lista 1‑D de 42 inteiros (para ID3)."""
        return [cell for row in self.board for cell in row]

    # Constrói o tabuleiro
    def render(self) -> str:
        symbols = {EMPTY: ".", PLAYER_X: "X", PLAYER_O: "O"}
        lines = [" ".join(symbols[cell] for cell in row) for row in self.board]
        header = " ".join(str(c) for c in range(COLS))
        return "\n".join(lines) + "\n" + header

    # Exibe o tabuleiro no terminal
    def display(self):
        print(self.render())

        # Exibir APENAS o próximo jogador, NÃO mostrar o resultado do jogo
        if not self.is_game_over():
            player_name = "X" if self.current_player == PLAYER_X else "O"
            print(f"Vez do jogador {player_name}")


    # Métodos para verificar 4 peças em sequência em todas direções
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