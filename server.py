import logging

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    session,
)

from src.connect_four_game import (
    ConnectFour,
)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s : %(message)s')

app = Flask(__name__, template_folder='templates/')
app.secret_key = b"6a20cd0be3d9c565b8978f48fff4098c"
game = ConnectFour()

@app.route("/")
def index():
    if "username" in session:
        logging.info(f'Logged in as {session["username"]}')
    else:
        logging.info("You are not logged in")
    return render_template('index.html', game_data=game.to_dict())

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    column = data.get('column')

    if column is None:
        return jsonify({"error": "no column provided"}), 400
    if column < 0 or column > game.column_max - 1:
        return jsonify({"error": "Column is out of bound"}), 400
    if column not in game.get_column_options():
        return jsonify({"error": "Column is full"}), 400

    game.play((column, game.board[column]))
    game._compute_state()
    game.play_bot_move()
    game._compute_state()
    game.display_board()
    return jsonify(game.to_dict()), 200

if __name__ == "__main__":
    app.run(port=3000, debug=True)
