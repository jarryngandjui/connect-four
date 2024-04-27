from unittest import TestCase

from src.mnk_game import AbstractMNKGame
from src.monte_carlo_bot import MonteCarloTreeSearchNode, MonteCarloBot


class MonteCarloTreeSearchTestCase(TestCase):
    def setUp(self):
        self.game = AbstractMNKGame(5, 6, 4)

    def test_explore(self):
        node = MonteCarloTreeSearchNode(AbstractMNKGame(5, 6, 4), AbstractMNKGame.PLAYER_1, simulation_count=10, explore_depth=3)
        node.explore()
        # Ensure child nodes are created
        expected_child_nodes_len = 6
        expected_child_moves = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0)]
        expected_players = [AbstractMNKGame.PLAYER_2]*len(expected_child_moves)
        actual_child_nodes_len = len(node.child_nodes)
        actual_child_moves = [c.game.moves[AbstractMNKGame.PLAYER_1][-1] for c in node.child_nodes]
        actual_players = [c.game.player for c in node.child_nodes]
        self.assertEqual(actual_child_nodes_len, expected_child_nodes_len)
        self.assertEqual(actual_child_moves, expected_child_moves)
        self.assertEqual(actual_players, expected_players)

    def test_simulate(self):
        node = MonteCarloTreeSearchNode(AbstractMNKGame(5, 6, 4), AbstractMNKGame.PLAYER_1, simulation_count=10, explore_depth=3)
        node.explore()
        node.simulate()
        for c in node.child_nodes:
            self.assertEqual(c.games_total, node.simulation_count)

    def test_backpropagate(self):
        node = MonteCarloTreeSearchNode(AbstractMNKGame(3, 3, 3), AbstractMNKGame.PLAYER_1, simulation_count=1, explore_depth=1)
        node.tree_search()
        self.assertEqual(node.games_total, 3)

        node = MonteCarloTreeSearchNode(AbstractMNKGame(3, 3, 3), AbstractMNKGame.PLAYER_1, simulation_count=2, explore_depth=1)
        node.tree_search()
        self.assertEqual(node.games_total, 3**2)

        node = MonteCarloTreeSearchNode(AbstractMNKGame(3, 3, 3), AbstractMNKGame.PLAYER_1, simulation_count=1, explore_depth=2)
        node.tree_search()
        self.assertEqual(node.games_total, 3*2)

    def test_get_top_move(self):
        game = AbstractMNKGame(5, 6, 4)
        node = MonteCarloTreeSearchNode(game, AbstractMNKGame.PLAYER_1, simulation_count=10, explore_depth=3)
        node.explore()
        node.simulate()
        top_move = node.get_top_move()
        # Ensure best move is valid
        self.assertIsNotNone(top_move)
        self.assertIn(top_move[0], range(game.column_max))
        self.assertIn(top_move[1], range(game.row_max))


class MonteCarloBotTestCase(TestCase):
    def test_get_next_move(self):
        game = AbstractMNKGame(3, 3, 3)
        bot = MonteCarloBot(game)
        next_move = bot.get_move()
        # Ensure next move is valid
        self.assertIsNotNone(next_move)
        self.assertIn(next_move[0], range(game.column_max))
        self.assertIn(next_move[1], range(game.row_max))

    def test_play_defensive_move(self):
        game = AbstractMNKGame(6, 7, 4)
        game.player = AbstractMNKGame.PLAYER_1
        game.play((2, 0))
        game.play((3, 0))
        game.play((5, 0))
        game.player = AbstractMNKGame.PLAYER_2
        bot = MonteCarloBot(game, simulation_count=30, explore_depth=30)
        defensive_move = bot.get_move()
        self.assertEqual(defensive_move, (4, 0))
