import copy
import logging
from random import randint
from typing import List, Tuple
from src.mnk_game import AbstractMNKGame 

logging.basicConfig(level=logging.INFO)


class MonteCarloTreeSearchNode():
    '''
    Node in the Monte Carlo Tree Seach for an MNK Game
    '''
    def __init__(self, game: AbstractMNKGame, mcts_player: str, parent=None, simulation_count=10):
        self.parent = parent 
        self.game = game
        self.mcts_player = mcts_player
        self.simulation_count = simulation_count
        self.games_won = 0
        self.games_lost = 0
        self.games_tied = 0
        self.games_total = 0
        self.child_nodes: List[MonteCarloTreeSearchNode] = []

    def explore(self):
        '''
        Create a child node for each move option possible by the current player,
        in the new node, update the game state, player, and parent.
        '''
        if self.game.is_over:
            return
        column_options = self.game.get_column_options()
        for column in column_options:
            game_copy = copy.deepcopy(self.game)
            game_copy.play((column, game_copy.board[column]))
            game_copy.next_player()
            mcts_move_node = MonteCarloTreeSearchNode(game=game_copy, mcts_player=self.mcts_player, parent=self)
            self.child_nodes.append(mcts_move_node)

    def simulate(self):
        '''
        Monte Carlo Tree Search Simulation randomly picks moves the options until 
        the game reaches an end state. 
        '''
        for child in self.child_nodes:
            for _ in range(self.simulation_count):
                child._run_simulation(copy.deepcopy(child.game))

    def _run_simulation(self, game: AbstractMNKGame):
        if game.is_over:
            self.games_total += 1
            self.games_won += 1 if game.is_won and self.mcts_player == game.winner else 0
            self.games_lost += 1 if game.is_won and self.mcts_player != game.winner else 0
            self.games_tied += 1 if game.is_tied else 0
            return

        column_options = game.get_column_options()
        column = column_options[randint(0, len(column_options)-1)] if len(column_options) > 1 else column_options[0]
        game.play((column, game.board[column]))
        game.next_player()
        self._run_simulation(game)

    def backpropagate(self):
        '''
        Updates the game stats for all nodes on the path to this one up the root
        '''
        for c in self.child_nodes:
            self.games_won += c.games_won
            self.games_lost += c.games_lost
            self.games_tied += c.games_tied
            self.games_total += c.games_total

        if self.parent:
            self.parent.backpropagation()

    def get_best_move(self) -> Tuple[int, int]:
        '''
        Each child node is one move out from the parent, therefor the child node
        with the highest win rate has the best move.
        '''
        win_rate_max = 0.0
        win_move = (0, 0) 
        for c in self.child_nodes:
            c_win_rate = float(c.games_won/c.games_total)
            if c_win_rate > win_rate_max:
                win_rate_max = c_win_rate
                win_move = c.game.moves[c.mcts_player][-1]
        return win_move


class MonteCarloBot():
    '''
    From a MNK Game state, find the next move using Monte Carlo Tree Search (MCTS)
    '''
    def __init__(self, game: AbstractMNKGame, mcts_player: str=AbstractMNKGame.PLAYER_1, simulation_count=10) -> None:
        self.root = MonteCarloTreeSearchNode(game=copy.deepcopy(game), mcts_player=mcts_player, simulation_count=simulation_count)
        self.mcts_player = mcts_player

    def get_next_move(self) -> Tuple[int, int]:
        self.root.explore()
        self.root.simulate()
        self.root.backpropagate()
        return self.root.get_best_move()

    def display_stats(self):
        logging.info('Player %s stat results after playing %s games.', self.mcts_player, self.root.games_total)
        logging.info('Player %s won %s games.', self.mcts_player, self.root.games_won)
        logging.info('Player %s lost %s games.', self.mcts_player, self.root.games_lost)
        logging.info('Player %s tied %s games.', self.mcts_player, self.root.games_tied)
        logging.info('Player %s most successful move is %s.', self.mcts_player, self.root.get_best_move())



