import argparse
import logging
from src.connect_four_game import ConnectFour


logging.basicConfig(level=logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Connect Four game with player options.")
    parser.add_argument('--players', type=int, choices=[1, 2], default=2,
                        help="Number of players (1 or 2). Default is 2.")
    parser.add_argument('--simulation_count', type=int, default=30,
                        help="Number of simulations at each node of the Monte Carlo Tree Search.")
    parser.add_argument('--explore_depth', type=int, default=30,
                        help="Forecast moves ahead in the Monte Carlo Tree Search")
    return parser.parse_args()


def main():
    args = parse_arguments()
    game = ConnectFour()

    if args.players == 1:
        game.start_one_player(simulation_count=args.simulation_count, explore_depth=args.explore_depth)
    else:
        game.start_two_players()

if __name__ == "__main__":
    main()
