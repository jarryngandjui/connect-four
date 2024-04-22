from unittest import TestCase
from src.mnk_game import AbstractMNKGame
from src.monte_carlo_bot import MonteCarloTreeSearchNode, MonteCarloBot

class TestMonteCarloTreeSearchTestCase(TestCase):
    def setUp(self):
        self.game = AbstractMNKGame(3, 3, 3)
        self.node = MonteCarloTreeSearchNode(self.game, AbstractMNKGame.PLAYER_1)

    def test_explore(self):
        self.node.explore()
        # Ensure child nodes are created
        expected_child_nodes_len = 3
        expected_child_moves = [(0,0), (1,0), (2,0)]
        expected_players = [AbstractMNKGame.PLAYER_2]*3
        actual_child_nodes_len = len(self.node.child_nodes)
        actual_child_moves = [c.game.moves[AbstractMNKGame.PLAYER_1][-1] for c in self.node.child_nodes]
        actual_players = [c.game.player for c in self.node.child_nodes]
 
        self.assertEqual(actual_child_nodes_len, expected_child_nodes_len)
        self.assertEqual(actual_child_moves, expected_child_moves)
        self.assertEqual(actual_players, expected_players)
        
    def test_simulate(self):
        self.node.explore()
        self.node.simulate()
        for c in self.node.child_nodes:
            self.assertEqual(c.games_total, self.node.simulation_count)

    def test_backpropagate(self):
        self.node.explore()
        self.node.simulate()
        self.node.backpropagate()
        self.assertEqual(self.node.games_total, 3*self.node.simulation_count)

    def test_get_best_move(self):
        self.node.explore()
        self.node.simulate()
        best_move = self.node.get_best_move()
        # Ensure best move is valid
        self.assertIn(best_move[0], range(self.game.column_max))
        self.assertIn(best_move[1], range(self.game.row_max))

class TestMonteCarloBotTestCase(TestCase):
    def setUp(self):
        self.game = AbstractMNKGame(3, 3, 3)
        self.bot = MonteCarloBot(self.game)

    def test_get_next_move(self):
        next_move = self.bot.get_next_move()
        # Ensure next move is valid
        self.assertIn(next_move[0], range(self.game.column_max))
        self.assertIn(next_move[1], range(self.game.row_max))


