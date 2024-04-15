from unittest import TestCase
from MNKGame import AbstractMNKGame, ConnectFour


class TestConnectFour(TestCase):
    def test_initialization(self):
        game = ConnectFour()
        self.assertEqual(len(game.board), game.column_max)
        self.assertEqual(len(game.moves[AbstractMNKGame.PLAYER_1]), 0)
        self.assertEqual(len(game.moves[AbstractMNKGame.PLAYER_2]), 0)
        self.assertEqual(game.moves_count_total, 0)
        self.assertFalse(game.is_game_over)

    def test_generic_mnk_game(self):
        connect_three_game = AbstractMNKGame(m=4, n=5, k=3)
        self.assertEqual(len(connect_three_game.board), 5)
        self.assertEqual(connect_three_game.column_max, 5)
        self.assertEqual(connect_three_game.row_max, 4)
        self.assertEqual(len(connect_three_game.moves[AbstractMNKGame.PLAYER_1]), 0)
        self.assertEqual(len(connect_three_game.moves[AbstractMNKGame.PLAYER_2]), 0)
        self.assertEqual(connect_three_game.moves_count_total, 0)
        self.assertFalse(connect_three_game.is_game_over)

        connect_three_game.moves[connect_three_game.player] = [(1, 1), (2, 1), (3, 1)]
        self.assertTrue(connect_three_game.is_connected((3, 1)))
        connect_three_game.moves[connect_three_game.player] = [(0, 2), (0, 1), (0, 0)]
        self.assertTrue(connect_three_game.is_connected((0, 2)))
        connect_three_game.moves[connect_three_game.player] = [(3, 2), (2, 1), (1, 0)]
        self.assertTrue(connect_three_game.is_connected((1, 0)))

    def test_get_next_player(self):
        game = ConnectFour()
        self.assertEqual(game.player, AbstractMNKGame.PLAYER_1)
        game.player = game.get_next_player(game.player)
        self.assertEqual(game.player, AbstractMNKGame.PLAYER_2)
        game.player = game.get_next_player(game.player)
        self.assertEqual(game.player, AbstractMNKGame.PLAYER_1)

    def test_is_connected_horizontally(self):
        game = ConnectFour()
        # Test inline and ordered
        game.moves[game.player] = [(0, 1), (1, 1), (2, 1), (3, 1)]
        self.assertTrue(game.is_connected((3, 1)))
        # Test gap
        game.moves[game.player] = [(0, 1), (1, 1), (2, 1), (4, 1)]
        self.assertFalse(game.is_connected((4, 1)))
        # Test inline and unordered
        game.moves[game.player] = [(1, 1), (2, 1), (0, 1), (3, 1)]
        self.assertTrue(game.is_connected((3, 1)))
        # Test multi-inline and unordered
        game.moves[game.player] = [(1, 1), (2, 1), (0, 1), (4, 3), (3, 3), (5, 3), (2, 3)]
        self.assertTrue(game.is_connected((2, 3)))

    def test_is_connected_vertically(self):
        game = ConnectFour()
        # Test inline and ordered
        game.moves[game.player] = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertTrue(game.is_connected((0, 4)))
        # Test gap
        game.moves[game.player] = [(0, 1), (0, 2), (0, 4), (0, 5)]
        self.assertFalse(game.is_connected((0, 5)))
        # Test inline and unordered
        game.moves[game.player] = [(0, 2), (0, 1), (0, 3), (0, 0)]
        self.assertTrue(game.is_connected((0, 3)))
        # Test multi-inline and unordered
        game.moves[game.player] = [(0, 2), (0, 4), (0, 3), (0, 6), (0, 1), (0, 5)]
        self.assertTrue(game.is_connected((0, 5)))

    def test_is_connected_diagonally(self):
        game = ConnectFour()
        # Test diagonal connection with slope 1
        game.moves[game.player] = [(0, 0), (1, 1), (2, 2), (3, 3)]
        self.assertTrue(game.is_connected((3, 3)))

        # Test unordered moves
        game.moves[game.player] = [(4, 3), (3, 2), (2, 1), (5, 4)]
        self.assertTrue(game.is_connected((2, 1)))

        # Test non-diagonal connection
        game.moves[game.player] = [(0, 0), (1, 1), (2, 2), (4, 4)]
        self.assertFalse(game.is_connected((4, 4)))

        # Test diagonal connection with slope -1
        game.moves[game.player] = [(3, 3), (2, 2), (1, 1), (0, 0)]
        self.assertTrue(game.is_connected((3, 3)))
