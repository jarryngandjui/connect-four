import argparse
import logging
from src.connect_four_game import ConnectFour


logging.basicConfig(level=logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Connect Four game with player options.")
    parser.add_argument('--players', type=int, choices=[1, 2],
                        help="Number of players (1 or 2). Default is 2.")
    parser.add_argument('--replay', type=str,
                        help="Filename to a game that was exported.")
    parser.add_argument('--simulation_count', type=int, default=30,
                        help="Number of simulations at each node of the Monte Carlo Tree Search.")
    parser.add_argument('--explore_depth', type=int, default=30,
                        help="Forecast moves ahead in the Monte Carlo Tree Search")
    parser.add_argument('--should_export', type=bool, default=True,
                        help="Output the result of the game to a json file.")
    parser.add_argument('--var_replay', type=str,
                        help="Filename to a game that was exported.")
    parser.add_argument('--debug', type=bool, default=False,
                        help="Step through debugger for the replay.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    game = ConnectFour(should_export=args.should_export)

    if args.players == 1:
        game.start_one_player(
            simulation_count=args.simulation_count,
            explore_depth=args.explore_depth
        )
    elif args.players == 2:
        game.start_two_players()
    elif args.replay:
        ConnectFour.start_game_replay(
            filename=args.replay,
            debug=args.debug,
            should_export=args.should_export
        )
    else:
        logging.info('Unsupported options for Connect Four')


if __name__ == "__main__":
    main()
