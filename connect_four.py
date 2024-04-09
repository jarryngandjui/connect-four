import logging
import math
from typing import List, Tuple


logging.basicConfig(level=logging.INFO)


class ConnectFour():
    COLUMN_MAX = 6
    ROW_MAX = 7
    TARGET = 4

    PLAYER_1 = 'X'
    PLAYER_2 = 'O'
    PLAYERS = [PLAYER_1, PLAYER_2]

    def __init__(self):
        self.board = {col: 0 for col in range(ConnectFour.COLUMN_MAX)}
        self.moves = {p: [] for p in ConnectFour.PLAYERS}
        self.player = ConnectFour.PLAYER_1
        self.duration = 0
        self.is_game_over = False

    def get_moves(self, player) -> List[Tuple[int, int]]:
        return self.moves.get(player, [])

    def start_game(self):
        logging.info('Starting a game of Connect Four')
        self.display_board()

        try:
            while not self.is_game_over:
                move = self.play()
                self.display_board()
                self.compute_state(move)
        except KeyboardInterrupt:
            logging.info('Exiting Connect Four')

    def play(self) -> Tuple[int, int]:
        move = None
        while not move:
            logging.info('%s please enter your next move.', self.player)
            column = input()
            try:
                column = int(column)
                assert column >= 0 and column <= ConnectFour.COLUMN_MAX - 1,  f'{column} is outside the range (0, {ConnectFour.COLUMN_MAX})'
                assert self.board[column] < ConnectFour.ROW_MAX, f'Column {column} on the board is full'
                move = (column, self.board[column])
            except Exception as e:
                logging.error('Please try again', str(e))
                move = None
        self.get_moves(self.player).append(move)
        self.board[column] += 1
        self.duration += 1
        return move

    def compute_state(self, move: Tuple[int, int]):
        is_connected = self.is_connected(move)
        is_moves_full = self.is_moves_full()
        self.is_game_over = is_moves_full or self.is_connected(move)
        is_player_winner = self.is_game_over and is_connected
        is_game_tied = self.is_game_over and not is_connected

        if is_player_winner:
            logging.info('Congratulations %s is the winner in %s moves.', self.player, self.duration)
        elif is_game_tied:
            logging.info('Too bad the game is tied after %s moves.', self.duration)
        else:
            self.next_player()

    def is_connected(self, move: Tuple[int, int]) -> bool:
        player_moves = self.get_moves(self.player) 
        player_moves_in_target = [m for m in player_moves if int(math.dist(m, move)) <= ConnectFour.TARGET] 

        if len(player_moves_in_target) < ConnectFour.TARGET:
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

        for i in range(len(player_moves)-1):
            if player_moves[i][0]+1 == player_moves[i+1][0]:
                connected_plays += 1
            else:
                connected_plays = 1
            if connected_plays >= ConnectFour.TARGET:
                return True
        return False

    def is_vertically_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        player_moves = list(filter(lambda m: m[0]==move[0], player_moves))
        player_moves = sorted(player_moves, key=lambda m: m[1])
        connected_plays = 1

        for i in range(len(player_moves)-1):
            if player_moves[i][1]+1 == player_moves[i+1][1]:
                connected_plays += 1
            else:
                connected_plays = 1
            if connected_plays >= ConnectFour.TARGET:
                return True
        return False

    def is_diagonally_connected(self, move: Tuple[int, int], player_moves: List[Tuple[int, int]]=[]) -> bool:
        player_moves = list(filter(lambda m: m[1]-move[1]==m[0]-move[0], player_moves))
        player_moves = sorted(player_moves, key=lambda m: (m[0], m[1]))
        connected_plays = 1
        
        for i in range(len(player_moves)-1):
            if (
                abs(player_moves[i][0] - player_moves[i+1][0]) == 1
                and abs(player_moves[i][1] - player_moves[i+1][1]) == 1
            ):
                connected_plays += 1
            else:
                connected_plays = 1
            if connected_plays >= ConnectFour.TARGET:
                return True
        return False

    def is_moves_full(self) -> bool:
        return self.duration >= ConnectFour.COLUMN_MAX * ConnectFour.ROW_MAX

    def next_player(self):
        self.player = ConnectFour.PLAYER_2 if self.player == ConnectFour.PLAYER_1 else ConnectFour.PLAYER_1

    def display_board(self):
        logging.info('Board after %s moves by players %s', self.duration, ConnectFour.PLAYERS)
        for row in range(ConnectFour.ROW_MAX - 1, -1, -1):
            line = "|"
            for col in range(ConnectFour.COLUMN_MAX):
                if (col, row) in self.moves[ConnectFour.PLAYER_1]:
                    line += " X |"  # Player 1's move
                elif (col, row) in self.moves[ConnectFour.PLAYER_2]:
                    line += " O |"  # Player 2's move
                else:
                    line += "   |"  # Empty slot
            logging.info(line)
        logging.info("|---" * ConnectFour.COLUMN_MAX + "|")
        column_numbers = "|"
        for col in range(ConnectFour.COLUMN_MAX):
            column_numbers += f" {col} |"
        logging.info(column_numbers)
