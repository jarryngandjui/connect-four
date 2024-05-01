import logging

from src.monte_carlo_bot import MonteCarloBot
from src.mnk_game import AbstractMNKGame


logging.basicConfig(level=logging.INFO)


class ConnectFourException(Exception):
    pass


class ConnectFour(AbstractMNKGame):
    NAME = 'Connect Four'

    def __init__(self, should_export: bool = False):
        super().__init__(m=6, n=7, k=4, name=ConnectFour.NAME)
        self.should_export = should_export

    def start_one_player(
        self,
        simulation_count: int = MonteCarloBot.SIMULATION_COUNT,
        explore_depth: int = MonteCarloBot.EXPLORE_DEPTH,
    ):
        logging.info('Starting a 1 player ConnectFour game against MonteCarloBot')
        self.display_start()
        try:
            while not self.is_over:
                if self.player == AbstractMNKGame.PLAYER_1:
                    move = self.get_move()
                else:
                    move = MonteCarloBot(game=self, simulation_count=simulation_count, explore_depth=explore_depth).get_move()
                    if not move:
                        logging.warn('Failed to get an AI bot move')
                        continue
                self.play(move)
                self.display_board()
                self.compute_state()
        except (KeyboardInterrupt, ConnectFourException):
            logging.info('Exiting %s game', self.name)

    def start_two_players(self):
        logging.info('Starting a 2 player ConnectFour game')
        self.display_start()
        try:
            while not self.is_over:
                move = self.get_move()
                self.play(move)
                self.display_board()
                self.compute_state()
        except KeyboardInterrupt:
            logging.info('Exiting %s game', self.name)

    @classmethod
    def replay_game(cls, filename: str, debug=False, should_export=False):
        logging.info('Starting a VAR replay for the ConnectFour game export - %s', filename)
        var_game = None
        try:
            var_game = cls.from_export(filename)
            assert var_game.name == ConnectFour.NAME
        except Exception:
            logging.info('Expected %s game from filename %s', ConnectFour.NAME, filename)
            return

        live_replay = cls(should_export=should_export)
        try:
            while not live_replay.is_over:
                player_move_count = len(live_replay.moves[live_replay.player])
                if len(var_game.moves[live_replay.player]) <= player_move_count:
                    logging.info('Player %s is out of moves', live_replay)
                    break
                if debug:
                    input("Press Enter to continue...")
                move = var_game.moves[live_replay.player][player_move_count]
                live_replay.play(move)
                live_replay.display_board()
                live_replay.compute_state()
        except KeyboardInterrupt:
            logging.info('Exiting %s game', live_replay.name)

    def compute_state(self):
        if self.is_over and self.should_export:
            self.export_result()
        if self.is_won:
            logging.info('Congratulations %s is the winner in %s moves.', self.player, self.moves_count)
        elif self.is_full:
            logging.info('Too bad the game is tied after %s moves.', self.moves_count)
        else:
            logging.info('All moves %s', self.moves)
            self.next_player()

    def export_result(self):
        filename = self.export()
        logging.info('Connect Four game result is exported to %s', filename)
