"""
Monte Carlo Tree Search (MCTS) Simplificado
Implementação didática ultra-compacta para jogos
"""

import math
import random


from game.board import Board


class MCTS:
    """
    Implementação simplificada do algoritmo Monte Carlo Tree Search.
    """
    
    class Node:
        """Nó da árvore de busca do MCTS"""
        
        def __init__(self, game_state, move=None, parent=None):
            """
            Inicializa um nó do MCTS
            
            Args:
                game_state: Estado atual do jogo
                move: Jogada que levou a este estado (None para o nó raiz)
                parent: Nó pai (None para o nó raiz)
            """
            self.game = game_state.copy()
            self.move = move
            self.parent = parent
            self.children = []
            self.visits = 0
            self.wins = 0.0
            self.untried_moves = game_state.valid_moves()


        # A teoria de bandits, para recompensas normalizadas em [0,1] sugere Raiz de 2
        # para garantir um bom trade-off entre exploração e aproveitamento.
        def ucb(self, exploration_cof=1.41) -> float:
            """Calcula o valor UCB (Upper Confidence Bound)"""
            if self.visits == 0:
                return float('inf')
            
            exploitation = self.wins / self.visits
            exploration = exploration_cof * math.sqrt(math.log(self.parent.visits) / self.visits)
            return exploitation + exploration
        
        def select_child(self) -> 'MCTS.Node':
            """Seleciona o filho com maior valor UCB"""
            return max(self.children, key=lambda child: child.ucb())
        
        def expand(self) -> 'MCTS.Node':
            """Adiciona um novo filho escolhendo uma jogada não testada"""
            move = random.choice(self.untried_moves)
            self.untried_moves.remove(move)
            
            new_game = self.game.copy()
            new_game.make_move(move)
            
            child = MCTS.Node(new_game, move, self)
            self.children.append(child)
            return child

        def find_winning_move(self,board: Board, player: int) -> int | None:
            for col in board.valid_moves():
                copy = board.copy()
                copy.apply_move(col)
                if copy.get_winner() == player:
                    return col
            return None

        def simulate(self) -> float:
            """Simula um jogo até o final com jogadas aleatórias"""
            sim_game = self.game.copy()
            player = sim_game.current_player
            
            # Simula jogadas aleatórias até o fim do jogo
            while not sim_game.is_game_over():
                moves = sim_game.valid_moves()
                if not moves:
                    break
                # Heuristica Para reduzir tamanho MCTree, reduz buscas sempre buscando jogadas vencedoras
                win = self.find_winning_move(sim_game, player)
                if win is not None:
                    move = win
                else:
                    move = random.choice(moves)
                sim_game.make_move(move)

            # Avalia o resultado
            winner = sim_game.get_winner()
            if winner == player:
                return 1.0  # Vitória
            elif winner is None:
                return 0.5  # Empate
            return 0.0  # Derrota


        def backpropagate(self, result: float):
            """Propaga o resultado pela árvore"""
            self.visits += 1
            self.wins += result
            if self.parent:
                self.parent.backpropagate(1.0 - result)
    
    def __init__(self, iterations=1000, time_limit: None = None | float, exploration_cof=1.41 ) -> None:
        """
        Inicializa o algoritmo MCTS
        
        Args:
            iterations: Número máximo de iterações
            time_limit: Tempo máximo em segundos (None para usar apenas iterações)
        """
        self.iterations = iterations
        self.time_limit = time_limit
        self.exploration = exploration_cof

    
    def best_move(self, game_state) -> int:
        """
        Encontra a melhor jogada para o estado atual do jogo
        
        Args:
            game_state: Estado atual do jogo
            
        Returns:
            A melhor jogada segundo o MCTS
        """
        # Cria o nó raiz
        root = self.Node(game_state)
        iterations_done = 0
        
        # Executa o algoritmo MCTS
        while iterations_done < self.iterations:
            iterations_done += 1
            
            # Fase 1: Seleção
            node = root
            while not node.untried_moves and node.children:
                node = node.select_child()
            
            # Fase 2: Expansão
            if node.untried_moves:
                node = node.expand()
            
            # Fase 3: Simulação
            result = node.simulate()
            
            # Fase 4: Retropropagação
            node.backpropagate(result)

        # Se o nó-raiz não tiver filhos, significa que:
        # 1) O estado inicial já era terminal (p.ex. jogo acabou),
        # 2) Ou não houve nenhuma iteração de MCTS (iterations == 0),
        # então não há “melhor filho” para escolher — caímos num fallback:
        if not root.children:
            # Escolhe aleatoriamente qualquer movimento válido do tabuleiro
            # Isso evita erro de max() em lista vazia e garante que
            # sempre retornamos algo legal.
            return random.choice(game_state.valid_moves())

        # max(..., key=lambda child: child.visits)
        # Varre todos os filhos do nó-raiz e devolve aquele com o maior
        # número de visitas (visits). Esse é o critério chamado “robust child”:
        # escolhemos a jogada mais explorada pelas simulações,
        # pois tendem a ser as mais confiáveis.
        best_child = max(root.children, key=lambda child: child.visits)

        # Cada filho guarda em .move qual movimento (coluna) levou
        # da raiz até ele. Aqui retornamos essa coluna “vencedora”:
        return best_child.move