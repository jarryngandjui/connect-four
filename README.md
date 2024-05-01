# connect-four

Build a connect-four game for the terminal, that supports two local players.

The game should support two players (X, O) until there is one winner. Connect four is a type of m-n-k game. An m,n,k-game is an abstract board game in which two players take turns in placing a stone of their color on an m-by-n board, the winner being the player who first gets k stones of their own color in a row, horizontally, vertically, or diagonally.

## Features

- Play abstract m-n-k games where users can win vertically, horizontally, and diagonally.
- 2 players locally.
- 1 player vs. bot opponent that uses a Monte Carlo Tree Search to pick the next move.
- Export the game state
- Replay a game state
- Unit tests.

## Get started 

- Clone locally, uses default python3 packages so it has no dependencies.
- Play 1 player vs. bot
  - `python main.py --players 1`
  - optional arg `--simulation_count N` to control the competitiveness of the bot, default is 30.
  - optional arg `--explore_depth N` to control how many moves ahead the bot forcasts, default is 30.
  - optional arg `--should_export True` saves the final game state in a export/{uuid4}.json file to be replayed.
- Play 2 players
  - `python main.py --players 2`
  - optional arg `--should_export True` saves the final game state in a export/{uuid4}.json file to be replayed.
- Replay exported game
  - `python main.py --replay {uuid4}.json`
  - optional arg `--debug True` enables a step through debugger for each move.
  - optional arg `--should_export True` saves the final game state in a export/{uuid4}.json file to be replayed.
- Run tests
  - `pytest tests/__test_name__`
