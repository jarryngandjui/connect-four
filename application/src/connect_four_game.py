import logging
import os
import pygame
import time

from typing import Callable, Tuple

from src.monte_carlo_bot import MonteCarloBot
from src.mnk_game import AbstractMNKGame


logging.basicConfig(level=logging.INFO)


class ConnectFourException(Exception):
    pass


class ConnectFour(AbstractMNKGame):
    NAME = "Connect Four"
    IN_GAME_AUDIO = os.path.join("static", "in_game.mp3")
    GAME_OVER_AUDIO = os.path.join("static", "game_over.mp3")
    MOVE_AUDIO = os.path.join("static", "move.mp3")

    def __init__(self, simulation_count=MonteCarloBot.SIMULATION_COUNT, explore_depth=MonteCarloBot.EXPLORE_DEPTH, should_export: bool = False, has_volume: bool = True):
        super().__init__(m=6, n=7, k=4, name=ConnectFour.NAME)
        self.simulation_count = simulation_count
        self.explore_depth = explore_depth
        self.should_export = should_export
        self.has_volume = has_volume

    @classmethod
    def play_in_game_audio(cls):
        pygame.mixer.init()
        pygame.mixer.music.load(ConnectFour.IN_GAME_AUDIO)
        pygame.mixer.music.play()

    @classmethod
    def play_game_over_audio(cls):
        pygame.mixer.init()
        pygame.mixer.music.load(ConnectFour.GAME_OVER_AUDIO)
        pygame.mixer.music.play()

    @classmethod
    def play_move_audio(cls):
        pygame.mixer.init()
        pygame.mixer.music.load(ConnectFour.MOVE_AUDIO)
        pygame.mixer.music.play()

    @classmethod
    def stop_audio(cls):
        pygame.mixer.music.stop()

    def start_one_player(
        self,
        simulation_count: int = MonteCarloBot.SIMULATION_COUNT,
        explore_depth: int = MonteCarloBot.EXPLORE_DEPTH,
    ):
        def move_callback():
            if self.player == AbstractMNKGame.PLAYER_1:
                return self._get_input_move()
            else:
                return self._get_bot_move(
                    simulation_count=simulation_count, explore_depth=explore_depth
                )

        logging.info("Starting a 1 player ConnectFour game against MonteCarloBot")
        self._live_game(move_callback)

    def start_two_players(self):
        logging.info("Starting a 2 player ConnectFour game")
        self._live_game(self._get_input_move)

    @classmethod
    def start_game_replay(cls, filename: str, debug=False, should_export=False):
        var_replay = None
        try:
            var_replay = cls.from_export(filename)
        except Exception:
            logging.info(
                "Expected %s game from export game - %s", ConnectFour.NAME, filename
            )
            return

        live_replay = cls(should_export=should_export, has_volume=False)

        def move_callback():
            move_i = len(live_replay.moves[live_replay.player])
            if len(var_replay.moves[live_replay.player]) <= move_i:
                logging.info("Player %s is out of moves", live_replay)
                return live_replay._get_input_move()
            else:
                if debug:
                    input("Press Enter to continue...\n")
                return var_replay.moves[live_replay.player][move_i]

        logging.info(
            "Starting a VAR replay for the ConnectFour game export - %s", filename
        )
        live_replay._live_game(move_callback)

    def play_bot_move(self):
        self.play(self._get_bot_move())

    def _live_game(self, move_callback: Callable):
        self.start()
        try:
            while not self.is_over:
                logging.info(
                    "%s please enter your next move from options: %s",
                    self.player,
                    self.get_column_options(),
                )
                if self.has_volume:
                    time.sleep(0.5)
                    ConnectFour.play_in_game_audio()
                self.play(move_callback())
                if self.has_volume:
                    ConnectFour.play_move_audio()
                self.display_board()
                self._compute_state()
        except KeyboardInterrupt:
            logging.info("Exiting %s game", self.name)

        if self.has_volume:
            ConnectFour.play_game_over_audio()
            time.sleep(2)
            ConnectFour.stop_audio()

    def _get_input_move(self) -> Tuple[int, int]:
        move = None
        column_options = self.get_column_options()
        while not move:
            try:
                column = int(input())
                move = (column, self.board[column])
                assert type(move) is tuple
                assert len(move) == 2
                assert move[0] in column_options
            except Exception:
                move = None
        return move

    def _get_bot_move(
        self,
        simulation_count: int = MonteCarloBot.SIMULATION_COUNT,
        explore_depth: int = MonteCarloBot.EXPLORE_DEPTH,
    ) -> Tuple[int, int]:
        move = None
        column_options = self.get_column_options()
        while not move:
            try:
                move = MonteCarloBot(
                    game=self,
                    simulation_count=simulation_count,
                    explore_depth=explore_depth,
                ).get_move()
                assert type(move) is tuple
                assert len(move) == 2
                assert move[0] in column_options
            except Exception:
                move = None
        return move

    def _compute_state(self):
        if self.is_over and self.should_export:
            filename = self.export()
            logging.info("Connect Four game result is exported to %s", filename)
        if self.is_won:
            logging.info(
                "Congratulations %s is the winner in %s moves.",
                self.player,
                self.moves_count,
            )
        elif self.is_full:
            logging.info("Too bad the game is tied after %s moves.", self.moves_count)
        else:
            self.next_player()
