import copy
import logging
from random import randint
from typing import Optional

from src.mnk_game import AbstractMNKGame

logging.basicConfig(level=logging.INFO)


class MonteCarloTreeSearchNode():
    '''
    Data struture for a node in the Monte Carlo Tree Seach for an MNK Game
    '''

    def __init__(self, game: AbstractMNKGame, mcts_player: str, simulation_count: int, explore_depth: int = 5, parent: Optional['MonteCarloTreeSearchNode'] = None):
        self.parent = parent
        self.game = game
        self.mcts_player = mcts_player
        self.simulation_count = simulation_count
        self.explore_depth = explore_depth
        self.is_searched = False
        self.games_won = 0
        self.games_lost = 0
        self.games_tied = 0
        self.games_total = 0
        self.child_nodes: list[MonteCarloTreeSearchNode] = []

    def get_win_rate(self) -> float:
        return float(self.games_won/self.games_total) if self.games_total else 0.0

    def get_lost_rate(self) -> float:
        return float(self.games_lost/self.games_total) if self.games_total else 0.0

    def get_top_child_node(self) -> Optional['MonteCarloTreeSearchNode']:
        if not self.child_nodes:
            return None

        win_rate_max = 0.0
        top_child_node = None
        for c in self.child_nodes:
            if c.get_win_rate() > win_rate_max:
                win_rate_max = c.get_win_rate()
                top_child_node = c
        return top_child_node

    def get_top_move(self) -> Optional[tuple[int, int]]:
        '''
        Top move is the last move made on the highest ranked
        child node.
        '''
        top_child_node = self.get_top_child_node()
        return top_child_node.game.moves[self.mcts_player][-1] if top_child_node else None

    def tree_search(self):
        if self.game.is_over or not self.explore_depth:
            return
        if self.is_searched:
            self._tree_search_top_child()
            return

        self.is_searched = True
        self.explore()
        self.simulate()
        self._tree_search_top_child()

    def _tree_search_top_child(self):
        if not self.is_searched:
            return
        top_child_node = self.get_top_child_node()
        if top_child_node:
            top_child_node.tree_search()

    def explore(self):
        '''
        Create a child node for each move option possible by the current player,
        in the new node, update the game state, player, and parent.
        '''
        if self.child_nodes:
            return

        column_options = self.game.get_column_options()
        for column in column_options:
            game_copy = copy.deepcopy(self.game)
            move = (column, game_copy.board[column])
            game_copy.play(move)
            game_copy.next_player()
            mcts_move_node = MonteCarloTreeSearchNode(
                parent=self,
                game=game_copy,
                mcts_player=self.mcts_player,
                simulation_count=self.simulation_count,
                explore_depth=self.explore_depth-1,
            )
            self.child_nodes.append(mcts_move_node)

    def simulate(self):
        '''
        Monte Carlo Tree Search Simulation randomly picks moves the options until
        the game reaches an end state.
        '''
        for child in self.child_nodes:
            if child.games_total:
                continue

            for _ in range(self.simulation_count):
                child._run_simulation(copy.deepcopy(child.game))
                child.backpropagate(
                    games_won=child.games_won,
                    games_lost=child.games_lost,
                    games_tied=child.games_tied,
                    games_total=child.games_total
                )

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

    def backpropagate(self, games_won: int = 0, games_lost: int = 0, games_tied: int = 0, games_total: int = 0):
        '''
        Updates the game stats for all nodes on the path to this one up the root
        '''
        if not self.parent:
            return
        self.parent.games_won += games_won
        self.parent.games_lost += games_lost
        self.parent.games_tied += games_tied
        self.parent.games_total += games_total
        self.parent.backpropagate(
            games_won=games_won,
            games_lost=games_lost,
            games_tied=games_tied,
            games_total=games_total
        )


class MonteCarloBot():
    EXPLORE_DEPTH = 30
    SIMULATION_COUNT = 30
    '''
    From a MNK Game state, find the next move using Monte Carlo Tree Search (MCTS)
    - find move based on winning odds
    - consider other player's best move and play defensively
    '''

    def __init__(self, game: AbstractMNKGame, simulation_count: int = SIMULATION_COUNT, explore_depth: int = EXPLORE_DEPTH):
        self.simulation_count = max(simulation_count, MonteCarloBot.SIMULATION_COUNT)
        self.explore_depth = max(explore_depth, MonteCarloBot.EXPLORE_DEPTH)
        self.mcts_player = game.player
        self.other_player = game.get_next_player()
        self.mcts_player_game = copy.deepcopy(game)
        self.other_player_game = copy.deepcopy(game)
        self.mcts_player_game.player = self.mcts_player
        self.other_player_game.player = self.other_player
        self.mcts_palyer_root = MonteCarloTreeSearchNode(
            game=self.mcts_player_game,
            mcts_player=self.mcts_player,
            simulation_count=self.simulation_count,
            explore_depth=self.explore_depth,
        )
        self.other_player_root = MonteCarloTreeSearchNode(
            game=self.other_player_game,
            mcts_player=self.other_player,
            simulation_count=self.simulation_count,
            explore_depth=self.explore_depth,
        )
        self.should_play_defensive = False

    def get_move(self) -> Optional[tuple[int, int]]:
        self.mcts_palyer_root.tree_search()
        self.other_player_root.tree_search()
        self.should_play_defensive = self.mcts_palyer_root.get_win_rate() < self.other_player_root.get_win_rate()
        self.display_stats()
        return self.other_player_root.get_top_move() if self.should_play_defensive else self.mcts_palyer_root.get_top_move()

    def display_stats(self):
        logging.info('Player %s games simulation_count %s explore_depth %s.', self.mcts_player, self.simulation_count, self.explore_depth)
        logging.info('Player %s stat results after playing %s games.', self.mcts_player, self.mcts_palyer_root.games_total)
        logging.info('mcts_palyer: %s win_rate: %s', self.mcts_player, self.mcts_palyer_root.get_win_rate())
        logging.info('other_palyer %s win_rate %s', self.other_player, self.other_player_root.get_win_rate())
        logging.info('mcts_player: %s should_play_defensive: %s', self.mcts_player, self.should_play_defensive)
