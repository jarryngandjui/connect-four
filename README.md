# connect-four

Build a connect-four game for the terminal, that supports two local players.

The game should support two players (X, O) until there is one winner. Connect four is a type of m-n-k game. An m,n,k-game is an abstract board game in which two players take turns in placing a stone of their color on an m-by-n board, the winner being the player who first gets k stones of their own color in a row, horizontally, vertically, or diagonally.

## Features

- ConnectFour 1 player vs. bot opponent that uses a Monte Carlo Tree Search (MCTS) to pick the next move
- ConnectFour 2 players locally
- In game audio
- Export the game state
- Replay a game state
- Extend to abstract m-n-k games
- Unit tests

## Get started 

- Clone locally, uses default python3 packages so it has no dependencies.
- Create a virtual env `python -m venv venv`
- Activate the virtual env `source ./venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
- Play 1 player vs. bot on a web ui 
  - `python application/server.py`
  - Navigate to http://localhost:3000/ to play against the MCTS bot
- Play 1 player vs. bot on the terminal
  - `python main.py --players 1`
  - optional arg `--simulation_count N` to control the competitiveness of the bot, default is 30.
  - optional arg `--explore_depth N` to control how many moves ahead the bot forcasts, default is 30.
  - optional arg `--should_export True` saves the final game state in a export/{uuid4}.json file to be replayed.
- Play 2 players on the terminal
  - `python main.py --players 2`
  - optional arg `--should_export True` saves the final game state in a export/{uuid4}.json file to be replayed.
- Replay exported game on the terminal
  - `python main.py --replay {uuid4}.json`
  - optional arg `--debug True` enables a step through debugger for each move.
  - optional arg `--should_export True` saves the final game state in a export/{uuid4}.json file to be replayed.
- Run tests
  - `pytest tests/__test_name__`
