import logging

from src.monte_carlo_bot import MonteCarloBot
from src.mnk_game import AbstractMNKGame


logging.basicConfig(level=logging.INFO)


class ConnectFour(AbstractMNKGame):
    def __init__(self):
        super().__init__(m=6, n=7, k=4, name='Connect Four')

    def start_one_player(self, simulation_count=10):
        '''
        1 player vs. Monte Carlo Bot using set simulations.
        '''
        self.display_start()
        human = AbstractMNKGame.PLAYER_1
        bot = AbstractMNKGame.PLAYER_2
        try:
            while not self.is_over:
                if self.player == human:
                    move = self.get_move()
                else:
                    move = MonteCarloBot(game=self, mcts_player=bot, simulation_count=simulation_count).get_next_move()

                self.play(move)
                self.display_board()

                if self.is_won:
                    logging.info('Congratulations %s is the winner in %s moves.', self.player, self.moves_count)
                elif self.is_full:
                    logging.info('Too bad the game is tied after %s moves.', self.moves_count)
                else:
                    self.next_player()
        except KeyboardInterrupt:
            logging.info('Exiting %s game', self.name)

    def start_two_players(self):
        '''
        Two players locally
        '''
        self.display_start()
        try:
            while not self.is_over:
                move = self.get_move()
                self.play(move)
                self.display_board()

                if self.is_won:
                    logging.info('Congratulations %s is the winner in %s moves.', self.player, self.moves_count)
                elif self.is_full:
                    logging.info('Too bad the game is tied after %s moves.', self.moves_count)
                else:
                    self.next_player()
        except KeyboardInterrupt:
            logging.info('Exiting %s game', self.name)
    
