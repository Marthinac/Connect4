"""
Monte Carlo Tree Search (MCTS) Simplificado
Implementação didática ultra-compacta para jogos
"""

import math
import random
import time
from typing import List, Optional


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
        
        def ucb(self, exploration=1.41) -> float:
            """Calcula o valor UCB (Upper Confidence Bound)"""
            if self.visits == 0:
                return float('inf')
            
            exploitation = self.wins / self.visits
            exploration = exploration * math.sqrt(math.log(self.parent.visits) / self.visits)
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
        
        def simulate(self) -> float:
            """Simula um jogo até o final com jogadas aleatórias"""
            sim_game = self.game.copy()
            player = sim_game.current_player
            
            # Simula jogadas aleatórias até o fim do jogo
            while not sim_game.is_terminal():
                moves = sim_game.valid_moves()
                if not moves:
                    break
                sim_game.make_move(random.choice(moves))
            
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
    
    def __init__(self, iterations=1000, time_limit=None):
        """
        Inicializa o algoritmo MCTS
        
        Args:
            iterations: Número máximo de iterações
            time_limit: Tempo máximo em segundos (None para usar apenas iterações)
        """
        self.iterations = iterations
        self.time_limit = time_limit
    
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
        
        # Inicializa contadores
        start_time = time.time()
        iterations_done = 0
        
        # Executa o algoritmo MCTS
        while iterations_done < self.iterations:
            # Verifica o limite de tempo
            if self.time_limit and time.time() - start_time > self.time_limit:
                break
                
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
        
        # Escolhe a jogada com mais visitas
        if not root.children:
            return random.choice(game_state.valid_moves())
        
        best_child = max(root.children, key=lambda child: child.visits)
        
        # Imprime estatísticas (opcional)
        print(f"MCTS fez {iterations_done} iterações em {time.time() - start_time:.2f}s")
        for child in sorted(root.children, key=lambda c: c.visits, reverse=True):
            if child.visits > 0:
                win_rate = child.wins / child.visits
                print(f"Jogada {child.move}: {child.wins:.1f}/{child.visits} ({win_rate:.2%})")
        
        return best_child.move