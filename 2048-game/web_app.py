"""
Flask web application for the 2048 game with AI solver.
Serves the game board in the browser and provides an API for the AI solver.
"""

import os
import sys
import json
from copy import deepcopy

# Ensure src/ is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from flask import Flask, render_template, request, jsonify
from game_logic import Logic
from ai_solver_logic import ExpectMMAI

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory game state per session (simple – for a single-user demo)
# ---------------------------------------------------------------------------
BOARD = [[0 for _ in range(4)] for _ in range(4)]
SCORE = 0
GAME_OVER = False
SPAWN_NEW = True
START_COUNT = 0
HIGH_SCORE = 0
SCORES_FILE = os.path.join(os.path.dirname(__file__), "src", "scores.txt")

game_logic = Logic()
ai_player = ExpectMMAI()


def _load_high_score():
    global HIGH_SCORE
    try:
        with open(SCORES_FILE, "r") as f:
            HIGH_SCORE = int(f.readline().strip())
    except (FileNotFoundError, ValueError):
        HIGH_SCORE = 0


def _save_high_score():
    try:
        with open(SCORES_FILE, "w") as f:
            f.write(str(HIGH_SCORE))
    except OSError:
        pass  # best-effort


def _add_random_tile(board):
    """Add a 2 (90 %) or 4 (10 %) in a random empty cell."""
    from random import randint

    empty = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty:
        return board
    i, j = empty[randint(0, len(empty) - 1)]
    board[i][j] = 4 if randint(1, 10) == 10 else 2
    return board


def _init_board():
    global BOARD, SCORE, GAME_OVER, SPAWN_NEW, START_COUNT
    BOARD = [[0 for _ in range(4)] for _ in range(4)]
    SCORE = 0
    GAME_OVER = False
    SPAWN_NEW = True
    START_COUNT = 0
    BOARD = _add_random_tile(BOARD)
    BOARD = _add_random_tile(BOARD)
    _load_high_score()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    """Serve the game page."""
    _init_board()
    return render_template("index.html")


@app.route("/api/state")
def get_state():
    """Return the current game state as JSON."""
    global HIGH_SCORE
    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE
        _save_high_score()
    return jsonify({
        "board": BOARD,
        "score": SCORE,
        "highScore": HIGH_SCORE,
        "gameOver": GAME_OVER,
    })


@app.route("/api/move", methods=["POST"])
def make_move():
    """Process a player move (direction)."""
    global BOARD, SCORE, GAME_OVER, SPAWN_NEW, START_COUNT

    data = request.get_json()
    direction = data.get("direction", "").upper()
    if direction not in ("UP", "DOWN", "LEFT", "RIGHT"):
        return jsonify({"error": "Invalid direction"}), 400

    if GAME_OVER:
        return jsonify({"error": "Game is over"}), 400

    old_board = deepcopy(BOARD)
    BOARD, SCORE, had_movement = game_logic.take_turn(direction, BOARD, SCORE)

    if BOARD != old_board:
        SPAWN_NEW = True

    if SPAWN_NEW:
        BOARD = _add_random_tile(BOARD)
        SPAWN_NEW = False

    if not game_logic.moves_possible(BOARD):
        GAME_OVER = True

    if SCORE > HIGH_SCORE:
        global HIGH_SCORE
        HIGH_SCORE = SCORE
        _save_high_score()

    return jsonify({
        "board": BOARD,
        "score": SCORE,
        "highScore": HIGH_SCORE,
        "gameOver": GAME_OVER,
    })


@app.route("/api/ai-move", methods=["POST"])
def ai_move():
    """Ask the AI solver for the best move and apply it."""
    global BOARD, SCORE, GAME_OVER, SPAWN_NEW, START_COUNT

    data = request.get_json()
    depth = data.get("depth", 2)

    if GAME_OVER:
        return jsonify({"error": "Game is over"}), 400

    direction, ai_score = ai_player.best_move_EMM(BOARD, SCORE, depth=depth)

    if not direction:
        GAME_OVER = True
        return jsonify({
            "board": BOARD,
            "score": SCORE,
            "highScore": HIGH_SCORE,
            "gameOver": GAME_OVER,
            "aiMove": None,
            "aiScore": ai_score,
        })

    old_board = deepcopy(BOARD)
    BOARD, SCORE, had_movement = game_logic.take_turn(direction, BOARD, SCORE)

    if BOARD != old_board:
        SPAWN_NEW = True

    if SPAWN_NEW:
        BOARD = _add_random_tile(BOARD)
        SPAWN_NEW = False

    if not game_logic.moves_possible(BOARD):
        GAME_OVER = True

    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE
        _save_high_score()

    return jsonify({
        "board": BOARD,
        "score": SCORE,
        "highScore": HIGH_SCORE,
        "gameOver": GAME_OVER,
        "aiMove": direction,
        "aiScore": ai_score,
    })


@app.route("/api/reset", methods=["POST"])
def reset_game():
    """Reset the game to a fresh state."""
    _init_board()
    return jsonify({
        "board": BOARD,
        "score": SCORE,
        "highScore": HIGH_SCORE,
        "gameOver": GAME_OVER,
    })


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)