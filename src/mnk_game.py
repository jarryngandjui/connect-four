import logging
import math
from os import walk
from typing import List, Tuple


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
        self.player = AbstractMNKGame.PLAYER_2 if self.player == AbstractMNKGame.PLAYER_1 else AbstractMNKGame.PLAYER_1

    def get_move(self) -> Tuple[int, int]:
        move = None
        column_options = self.get_column_options()
        while not move:
            logging.info('%s please enter your next move from options: %s', self.player, column_options)
            try:
                column = int(input())
                assert column in column_options
                move = (column, self.board[column])
            except Exception:
                move = None
        return move

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
            self.is_diagonally_connected(move, player_moves=player_moves_in_target)
            or self.is_horizontally_connected(move, player_moves=player_moves_in_target)
            or self.is_vertically_connected(move, player_moves=player_moves_in_target)
        )

    def is_horizontally_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        player_moves = list(filter(lambda m: m[1] == move[1], player_moves))
        player_moves = sorted(player_moves, key=lambda m: m[0])
        connected_plays = 1

        if not len(player_moves) >= self.target:
            return False

        for i in range(len(player_moves)-1):
            if player_moves[i][0]+1 == player_moves[i+1][0]:
                connected_plays += 1
            else:
                connected_plays = 1
            if connected_plays >= self.target:
                return True
        return False

    def is_vertically_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        player_moves = list(filter(lambda m: m[0]==move[0], player_moves))
        player_moves = sorted(player_moves, key=lambda m: m[1])
        connected_plays = 1

        if not len(player_moves) >= self.target:
            return False

        for i in range(len(player_moves)-1):
            if player_moves[i][1]+1 == player_moves[i+1][1]:
                connected_plays += 1
            else:
                connected_plays = 1
            if connected_plays >= self.target:
                return True
        return False

    def is_diagonally_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        player_moves = list(filter(lambda m: abs(m[1]-move[1])==abs(m[0]-move[0]), player_moves))
        player_moves = sorted(player_moves, key=lambda m: (m[0], m[1]))
        connected_plays = 1

        if not len(player_moves) >= self.target:
            return False

        for i in range(len(player_moves)-1):
            if (
                abs(player_moves[i][0] - player_moves[i+1][0]) == 1
                and abs(player_moves[i][1] - player_moves[i+1][1]) == 1
            ):
                connected_plays += 1
            else:
                connected_plays = 1
            if connected_plays >= self.target:
                return True
        return False

    def display_start(self):
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

