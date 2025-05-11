# ai/mcts.py

import math
import random
from typing import Optional

from game.board import Board

class Node:
    def __init__(self, board: Board, parent: Optional["Node"] = None, move: Optional[int] = None):
        self.board = board
        self.parent = parent
        self.move = move  # coluna (0–6) que levou a este estado
        self.children: list[Node] = []
        self.wins: float = 0.0
        self.visits: int = 0
        # movimentos ainda não expandidos a partir deste nó
        self.untried_moves: list[int] = board.valid_moves()

    def uct_select_child(self, exploration_weight: float) -> "Node":
        """Seleciona o filho com maior valor UCT."""
        log_parent_visits = math.log(self.visits)
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            # exploitation + exploration
            score = (child.wins / child.visits) + exploration_weight * math.sqrt(log_parent_visits / child.visits)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

class MCTS:
    def __init__(self, iterations: int = 1000, exploration_weight: float = math.sqrt(2)):
        """
        :param iterations: número de simulações MCTS
        :param exploration_weight: coeficiente de exploração (c)
        """
        self.iterations = iterations
        self.exploration_weight = exploration_weight

    def best_move(self, root_board: Board) -> int:
        """
        Executa MCTS a partir de root_board e retorna a coluna (0–6) do melhor movimento.
        """
        root_node = Node(root_board.copy())
        # quem está jogando no estado raiz
        self.player = root_board.current_player

        for _ in range(self.iterations):
            node = root_node
            board_copy = root_board.copy()

            # 1) Seleção
            while not node.untried_moves and node.children:
                node = node.uct_select_child(self.exploration_weight)
                board_copy.apply_move(node.move)

            # 2) Expansão
            if node.untried_moves:
                m = random.choice(node.untried_moves)
                board_copy.apply_move(m)
                node.untried_moves.remove(m)
                child = Node(board_copy.copy(), parent=node, move=m)
                node.children.append(child)
                node = child

            # 3) Simulação (rollout)
            winner = self._rollout(board_copy.copy())

            # 4) Retropagação
            while node is not None:
                node.visits += 1
                if winner == self.player:
                    node.wins += 1
                elif winner is None:
                    node.wins += 0.5  # empate vale meio ponto
                node = node.parent

        # Escolhe como melhor o filho com mais visitas
        best_child = max(root_node.children, key=lambda c: c.visits)
        return best_child.move

    def _rollout(self, board: Board) -> Optional[int]:
        """
        Joga aleatoriamente até o fim e retorna o vencedor (1, 2 ou None).
        """
        while not board.is_game_over():
            moves = board.valid_moves()
            m = random.choice(moves)
            board.apply_move(m)
        return board.get_winner()
