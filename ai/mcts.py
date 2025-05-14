import math
import random
from typing import Optional

from game.board import Board

class Node:
    def __init__(self, board: Board, parent: Optional["Node"] = None, move: Optional[int] = None):
        self.board = board
        self.parent = parent
        self.move = move  # coluna (0–6) que gerou este nó
        self.children: list[Node] = []
        self.wins: float = 0.0
        self.visits: int = 0
        # movimentos ainda não expandidos a partir deste nó
        self.untried_moves: list[int] = board.valid_moves()

    def uct_select_child(self, exploration_weight: float) -> "Node":
        """Seleciona o filho com maior valor UCT."""
        log_parent = math.log(self.visits)
        best = max(
            self.children,
            key=lambda c: (c.wins / c.visits) + exploration_weight * math.sqrt(log_parent / c.visits)
        )
        return best

class MCTS:
    def __init__(
        self,
        iterations: int = 1000,
        exploration_weight: float = math.sqrt(2),
        max_children: Optional[int] = None
    ):
        """
        :param iterations: número de simulações MCTS por jogada
        :param exploration_weight: coeficiente de exploração (c)
        :param max_children: limita quantos filhos são expandidos por nó (None = sem limite)
        """
        self.iterations = iterations
        self.exploration_weight = exploration_weight
        self.max_children = max_children

    def best_move(self, root_board: Board) -> int:
        root = Node(root_board.copy())
        player = root_board.current_player

        for _ in range(self.iterations):
            node = root
            state = root_board.copy()

            # 1) Seleção
            while True:
                can_expand = (
                    node.untried_moves and
                    (self.max_children is None or len(node.children) < self.max_children)
                )
                if can_expand or not node.children:
                    break
                node = node.uct_select_child(self.exploration_weight)
                state.apply_move(node.move)

            # 2) Expansão
            if node.untried_moves and (
                self.max_children is None or len(node.children) < self.max_children
            ):
                m = random.choice(node.untried_moves)
                state.apply_move(m)
                node.untried_moves.remove(m)
                child = Node(state.copy(), parent=node, move=m)
                node.children.append(child)
                node = child

            # 3) Simulação com heurística de vitória imediata
            winner = self._rollout(state.copy())

            # 4) Retropropagação
            while node:
                node.visits += 1
                if winner == player:
                    node.wins += 1
                elif winner is None:
                    node.wins += 0.5
                node = node.parent

        # escolhe o filho mais visitado
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move

    def _rollout(self, board: Board) -> Optional[int]:
        """
        Rollout simples com heurística de vitória imediata:
        Se existir um movimento que leva à vitória do jogador atual, joga-o.
        Caso contrário, escolhe aleatoriamente.
        """
        while not board.is_game_over():
            moves = board.valid_moves()
            player = board.current_player
            # Heurística: checar movimento de vitória usando copia
            for m in moves:
                temp = board.copy()
                temp.apply_move(m)
                if temp.get_winner() == player:
                    return player
            # se não há vitória imediata, escolhe aleatório
            board.apply_move(random.choice(moves))
        return board.get_winner()

