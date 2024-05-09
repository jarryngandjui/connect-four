import json
import logging
import math
import os
from typing import Callable, List, Tuple
from uuid import uuid4


logging.basicConfig(level=logging.INFO)


class AbstractMNKGame():
    '''
    An m,n,k-game is an abstract board game in which two players take turns 
    in placing a stone of their color on an m-by-n board, the winner being 
    the player who first gets k stones of their own color in a row,
    horizontally, vertically, or diagonally.
    '''


    PLAYER_1 = 'X'
    PLAYER_2 = 'O'
    PLAYERS = [PLAYER_1, PLAYER_2]
    EXPORT_DIR = 'export'

    def __init__(self, m: int, n: int, k: int, name: str =''):
        assert k > 1, 'Players must win in at least 2 connected moves'
        assert n <= 9, 'Column size must be less than or equal to 9 to display properly'
        assert m >= k and n >= k, f'Diagonal connected wins is not possible m-n-k config {m}-{n}-{k}'

        self.name = name or f'{m}-{n}-{k}'
        self.row_max = m
        self.column_max = n
        self.target = k
        self.board = [0] * self.column_max
        self.moves = {p: [] for p in AbstractMNKGame.PLAYERS}
        self.player = AbstractMNKGame.PLAYER_1
        self.moves_count = 0
        self.is_won = False
        self.is_tied = False
        self.is_full = False
        self.is_over = False
        self.winner = None

    def get_player_moves(self, player) -> List[Tuple[int, int]]:
        return self.moves.get(player, [])

    def get_column_options(self) -> List[int]:
        return [c for c in range(self.column_max) if self.board[c] < self.row_max]

    def next_player(self):
        self.player = self.get_next_player()

    def get_next_player(self) -> str:
        return AbstractMNKGame.PLAYER_2 if self.player == AbstractMNKGame.PLAYER_1 else AbstractMNKGame.PLAYER_1

    def play(self, move: Tuple[int, int]):
        column_options = self.get_column_options()
        assert move[0] in column_options, f'Bad move {move}, please select from {column_options}.' 
        self.get_player_moves(self.player).append(move)
        self.board[move[0]] += 1
        self.moves_count += 1
        self.is_full = self.moves_count >= self.column_max * self.row_max
        self.is_won = self.is_connected(move)
        self.winner = self.player if self.is_won else None
        self.is_tied = self.is_full and not self.is_won
        self.is_over = self.is_tied or self.is_won

    def is_connected(self, move: Tuple[int, int]) -> bool:
        player_moves = self.get_player_moves(self.player) 
        player_moves_in_target = [m for m in player_moves if int(math.dist(m, move)) <= self.target] 

        if len(player_moves_in_target) < self.target:
            return False
        return (
            self.is_horizontally_connected(move, player_moves=player_moves_in_target)
            or self.is_vertically_connected(move, player_moves=player_moves_in_target)
            or self.is_positive_diagonally_connected(move, player_moves=player_moves_in_target)
            or self.is_negative_diagonally_connected(move, player_moves=player_moves_in_target)
        )

    def is_horizontally_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        return self._is_connected_base(
            move,
            player_moves,
            sort_key_cb=lambda a: a[0],
            is_linear_cb=lambda a, b: a[1] == b[1],
            is_continuous_cb=lambda a, b: b[0] == a[0] + 1
        )

    def is_vertically_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        return self._is_connected_base(
            move,
            player_moves,
            sort_key_cb=lambda a: a[1],
            is_linear_cb=lambda a, b: a[0] == b[0],
            is_continuous_cb=lambda a, b: b[1] == a[1] + 1
        )

    def is_positive_diagonally_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        def is_positive_slope(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
            if a == b:
                # include the last move
                return True
            elif not a[0] - b[0]:
                # division by zero in slope formula
                return False
            else:
                return (b[1] - a[1]) / (b[0]-a[0]) == 1

        return self._is_connected_base(
            move,
            player_moves,
            sort_key_cb=lambda a: (a[0], a[1]),
            is_linear_cb=is_positive_slope,
            is_continuous_cb=lambda a, b: b[0] - a[0] == 1 and b[1] - a[1] == 1
        )

    def is_negative_diagonally_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        def is_negative_slope(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
            if a == b:
                # include the last move
                return True
            elif not a[0] - b[0]:
                # division by zero in slope formula
                return False
            else:
                return (b[1] - a[1]) / (b[0]-a[0]) == -1

        return self._is_connected_base(
            move,
            player_moves,
            sort_key_cb=lambda a: (a[1], a[0]),
            is_linear_cb=is_negative_slope,
            is_continuous_cb=lambda a, b: a[0] - b[0] == 1 and a[1] - b[1] == -1
        )

    def _is_connected_base(
            self, move: Tuple[int, int],
            player_moves: List[Tuple[int, int]],
            sort_key_cb: Callable=None,
            is_linear_cb: Callable[[Tuple, Tuple], bool]=None,
            is_continuous_cb: Callable[[Tuple, Tuple], bool]=None,
    ) -> bool:
        assert sort_key_cb, "sort_key_cb must be callable"
        assert is_linear_cb, "is_linear_cb must be callable"
        assert is_continuous_cb, "is_continuous_cb must be callable"

        player_moves = list(filter(lambda m: is_linear_cb(m, move), player_moves))
        player_moves = sorted(player_moves, key=lambda m: sort_key_cb(m))
        connected_plays = 1

        if not len(player_moves) >= self.target:
            return False

        for i in range(1, len(player_moves)):
            is_continuous = is_continuous_cb(player_moves[i-1], player_moves[i])
            connected_plays = connected_plays + 1 if is_continuous else 1
            if connected_plays >= self.target:
                return True
        return False

    def start(self):
        logging.info('Starting a game of %s with board size', self.name)
        logging.info('Creating of a board size of %sx%s', self.column_max, self.row_max)
        logging.info('First to connect %s wins...', self.target)
        self.display_board()

    def display_board(self):
        logging.info('Board after %s moves by players %s', self.moves_count, AbstractMNKGame.PLAYERS)
        logging.info('Game is over: %s', self.is_over)
        logging.info('Game is tied: %s', self.is_tied)
        logging.info('Game is won: %s', self.is_won)
        logging.info('Game winner: %s', self.winner)
        for row in range(self.row_max - 1, -1, -1):
            line = "|"
            for col in range(self.column_max):
                if (col, row) in self.moves[AbstractMNKGame.PLAYER_1]:
                    line += " X |"  # Player 1's move
                elif (col, row) in self.moves[AbstractMNKGame.PLAYER_2]:
                    line += " O |"  # Player 2's move
                else:
                    line += "   |"  # Empty slot
            logging.info(line)
        logging.info("|---" * self.column_max + "|")
        column_numbers = "|"
        for col in range(self.column_max):
            column_numbers += f" {col} |"
        logging.info(column_numbers)

    def export(self) -> str:
        filename = f'{uuid4()}.json'
        game_data = {
            'name': self.name,
            'row_max': self.row_max,
            'column_max': self.column_max,
            'target': self.target,
            'board': self.board,
            'moves': self.moves,
            'player': self.player,
            'moves_count': self.moves_count,
            'is_won': self.is_won,
            'is_tied': self.is_tied,
            'is_full': self.is_full,
            'is_over': self.is_over,
            'winner': self.winner
        }
        with open(os.path.join(AbstractMNKGame.EXPORT_DIR, filename), 'w') as f:
            json.dump(game_data, f, indent=4)
        return filename

    @classmethod
    def from_export(cls, filename) -> 'AbstractMNKGame':
        filepath = os.path.join(cls.EXPORT_DIR, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
        game = cls()
        game.name = data['name']
        game.row_max = data['row_max']
        game.column_max = data['column_max']
        game.target = data['target']
        game.board = data['board']
        game.player = data['player']
        game.moves_count = data['moves_count']
        game.is_won = data['is_won']
        game.is_tied = data['is_tied']
        game.is_full = data['is_full']
        game.is_over = data['is_over']
        game.winner = data['winner']
        game.moves = {}
        for p, moves in data['moves'].items():
            moves = [(m[0], m[1]) for m in moves]
            game.moves[p] = moves
        return game

    def __copy__(self):
        new_instance = self.__class__(self.row_max, self.column_max, self.target, self.name)
        new_instance.board = self.board.copy()
        new_instance.moves = {k: v.copy() for k, v in self.moves.items()}
        new_instance.player = self.player
        new_instance.moves_count = self.moves_count
        new_instance.is_won = self.is_won
        new_instance.is_tied = self.is_tied
        new_instance.is_full = self.is_full
        new_instance.is_over = self.is_over
        new_instance.winner = self.winner
        return new_instance
