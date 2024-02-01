"""
Here I implement the Expectiminimax algorithm that searches for the best possible moves.
It determines that by checking the "highest possible score of a state" given by the heuristic function.
"""
INFINITY = float("inf")
import multiprocessing as mp
from copy import deepcopy
from random import randint

from game_logic import Logic
from heuristic import Heuristic


class ExpectMMAI:
    def best_move_EMM(self, board, score, depth=2):
        best_score = -INFINITY
        best_next_move = ""
        results = []
        for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            testing_board = deepcopy(board)
            testing_board, new_score = Logic.take_turn(
                direction, testing_board, score
            )
            results.append(self.expectiminimax(testing_board, depth, direction))

        results = [res for res in results]

        for res in results:
            if res[0] >= best_score:
                best_score = res[0]
                best_next_move = res[1]

        return best_next_move, best_score

    def open_spots(self, board):
        empty_spots = []
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    empty_spots.append((i, j))

        return empty_spots

    def add_tile(self, board, location, value=None):
        i, j = location

        if value:
            board[i][j] = 0
            return

        if randint(1, 10) == 10:
            board[i][j] = 4
        else:
            board[j][j] = 2

        return

    def expectiminimax(self, board, depth, direction=None):
        print(board)
        for row in board:
            print(row)
        if not Logic.moves_possible(board):
            return -INFINITY, direction
        elif depth < 0:
            return Heuristic.heuristicValue(board), dir

        a = 0
        if depth != int(depth):
            a = -INFINITY
            for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
                testing_board = deepcopy(board)
                old_board = deepcopy(board)
                testing_board, score = Logic.take_turn(
                    direction, testing_board, score
                )

                if testing_board != old_board:
                    response = self.expectiminimax(
                        testing_board, depth - 0.5, direction
                    )[0]
                    if response > a:
                        a = response
        elif depth == int(depth):
            a = 0
            open_tiles = self.open_spots(board)
            for location in open_tiles:
                self.add_tile(board, location)
                a += (
                    1.0
                    / len(open_tiles)
                    * self.expectiminimax(board, depth - 0.5, direction)[0]
                )
                self.add_tile(board, location)
        return (a, direction)
