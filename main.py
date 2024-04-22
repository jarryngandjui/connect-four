import argparse
import logging
from src.connect_four_game import ConnectFour


logging.basicConfig(level=logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Connect Four game with player options.")
    parser.add_argument('--players', type=int, choices=[1, 2], default=2,
                        help="Number of players (1 or 2). Default is 2.")
    parser.add_argument('--simulation_count', type=int, default=10,
                        help="Number of simulations for Monte Carlo Tree Search. Must be an integer greater than 2. Default is 10.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    game = ConnectFour()

    if args.players == 1:
        game.start_one_player(simulation_count=args.simulation_count) 
    else:
        game.start_two_players()

if __name__ == "__main__":
    main()
