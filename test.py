from unittest import TestCase
from connect_four import ConnectFour


class TestConnectFour(TestCase):

    def setUp(self):
        self.game = ConnectFour()

    def test_initialization(self):
        self.assertEqual(len(self.game.board), ConnectFour.COLUMN_MAX)
        self.assertEqual(len(self.game.moves[ConnectFour.PLAYER_1]), 0)
        self.assertEqual(len(self.game.moves[ConnectFour.PLAYER_2]), 0)
        self.assertEqual(self.game.duration, 0)
        self.assertFalse(self.game.is_game_over)

    def test_next_player(self):
        self.assertEqual(self.game.player, ConnectFour.PLAYER_1)
        self.game.next_player()
        self.assertEqual(self.game.player, ConnectFour.PLAYER_2)
        self.game.next_player()
        self.assertEqual(self.game.player, ConnectFour.PLAYER_1)

    def test_is_connected_horizontally(self):
        # Test inline and ordered
        self.game.moves[self.game.player] = [(0, 1), (1, 1), (2, 1), (3, 1)]
        self.assertTrue(self.game.is_connected((3, 1)))
        # Test gap
        self.game.moves[self.game.player] = [(0, 1), (1, 1), (2, 1), (4, 1)]
        self.assertFalse(self.game.is_connected((4, 1)))
        # Test inline and unordered
        self.game.moves[self.game.player] = [(1, 1), (2, 1), (0, 1), (3, 1)]
        self.assertTrue(self.game.is_connected((3, 1)))
        # Test multi-inline and unordered
        self.game.moves[self.game.player] = [(1, 1), (2, 1), (0, 1), (4, 3), (3, 3), (5, 3), (2, 3)]
        self.assertTrue(self.game.is_connected((2, 3)))

    def test_is_connected_vertically(self):
        # Test inline and ordered
        self.game.moves[self.game.player] = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertTrue(self.game.is_connected((0, 4)))
        # Test gap
        self.game.moves[self.game.player] = [(0, 1), (0, 2), (0, 4), (0, 5)]
        self.assertFalse(self.game.is_connected((0, 5)))
        # Test inline and unordered
        self.game.moves[self.game.player] = [(0, 2), (0, 1), (0, 3), (0, 0)]
        self.assertTrue(self.game.is_connected((0, 3)))
        # Test multi-inline and unordered
        self.game.moves[self.game.player] = [(0, 2), (0, 4), (0, 3), (0, 6), (0, 1), (0, 5)]
        self.assertTrue(self.game.is_connected((0, 5)))

    def test_is_connected_diagonally(self):
        # Test diagonal connection with slope 1
        self.game.moves[self.game.player] = [(0, 0), (1, 1), (2, 2), (3, 3)]
        self.assertTrue(self.game.is_connected((3, 3)))

        # Test unordered moves
        self.game.moves[self.game.player] = [(4, 3), (3, 2), (2, 1), (5, 4)]
        self.assertTrue(self.game.is_connected((2, 1)))

        # Test non-diagonal connection
        self.game.moves[self.game.player] = [(0, 0), (1, 1), (2, 2), (4, 4)]
        self.assertFalse(self.game.is_connected((4, 4)))

        # Test diagonal connection with slope -1
        self.game.moves[self.game.player] = [(3, 3), (2, 2), (1, 1), (0, 0)]
        self.assertTrue(self.game.is_connected((3, 3)))
