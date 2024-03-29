"""
Here I implement the Expectiminimax algorithm that searches for the best possible moves.
It determines that by checking the "highest possible score of a state" given by the heuristic function.
"""

INFINITY = float("inf")
import multiprocessing as mp
from copy import deepcopy
from random import randint
#import numpy as np

from game_logic import Logic
from heuristic import Heuristic


class ExpectMMAI:
    "The Ai that solves the game"

    def __init__(self) -> None:
        self.game_logic = Logic()
        self.heuristic = Heuristic()
        self.score = 0
        self.max_tiles = 3

    def take_turn(self, direc, board):
        """Makes move on the board"""
        array_temp = [[0 for x in range(0, 4)] for x in range(0, 4)]
        for x in range(0, 16):
            array_temp[x % 4][x // 4] = board[x % 4][x // 4]

        if direc == "UP":
            for y_ind in range(0, 4):

                for x_ind in range(0, 4):

                    if array_temp[x_ind][y_ind] == 0:
                        for x_temp in range(x_ind + 1, 4):
                            if array_temp[x_temp][y_ind]:
                                array_temp[x_ind][y_ind] = array_temp[x_temp][y_ind]
                                array_temp[x_temp][y_ind] = 0
                                break

                for x_ind in range(0, 3):
                    if (
                        array_temp[x_ind][y_ind] == array_temp[x_ind + 1][y_ind]
                        and array_temp[x_ind][y_ind] != 0
                    ):
                        array_temp[x_ind][y_ind] *= 2

                        for x_temp in range(x_ind + 1, 3):
                            array_temp[x_temp][y_ind] = array_temp[x_temp + 1][y_ind]

                        array_temp[3][y_ind] = 0

        if direc == "DOWN":
            for y_ind in range(0, 4):

                for x_ind in range(3, -1, -1):

                    if array_temp[x_ind][y_ind] == 0:
                        for x_temp in range(x_ind - 1, -1, -1):
                            if array_temp[x_temp][y_ind]:
                                array_temp[x_ind][y_ind] = array_temp[x_temp][y_ind]
                                array_temp[x_temp][y_ind] = 0
                                break

                for x_ind in range(3, 0, -1):
                    if (
                        array_temp[x_ind][y_ind] == array_temp[x_ind - 1][y_ind]
                        and array_temp[x_ind][y_ind] != 0
                    ):
                        array_temp[x_ind][y_ind] *= 2

                        for x_temp in range(x_ind - 1, 0, -1):
                            array_temp[x_temp][y_ind] = array_temp[x_temp - 1][y_ind]

                        array_temp[0][y_ind] = 0

        if direc == "LEFT":
            for x_ind in range(0, 4):

                for y_ind in range(0, 4):

                    if array_temp[x_ind][y_ind] == 0:
                        for y_temp in range(y_ind + 1, 4):
                            if array_temp[x_ind][y_temp]:
                                array_temp[x_ind][y_ind] = array_temp[x_ind][y_temp]
                                array_temp[x_ind][y_temp] = 0
                                break

                for y_ind in range(0, 3):
                    if (
                        array_temp[x_ind][y_ind] == array_temp[x_ind][y_ind + 1]
                        and array_temp[x_ind][y_ind] != 0
                    ):
                        array_temp[x_ind][y_ind] *= 2

                        for y_temp in range(y_ind + 1, 3):
                            array_temp[x_ind][y_temp] = array_temp[x_ind][y_temp + 1]

                        array_temp[x_ind][3] = 0

        if direc == "RIGHT":
            for x_ind in range(0, 4):

                for y_ind in range(3, -1, -1):

                    if array_temp[x_ind][y_ind] == 0:
                        for y_temp in range(y_ind - 1, -1, -1):
                            if array_temp[x_ind][y_temp]:
                                array_temp[x_ind][y_ind] = array_temp[x_ind][y_temp]
                                array_temp[x_ind][y_temp] = 0

                                break

                for y_ind in range(3, 0, -1):
                    if (
                        array_temp[x_ind][y_ind] == array_temp[x_ind][y_ind - 1]
                        and array_temp[x_ind][y_ind] != 0
                    ):
                        array_temp[x_ind][y_ind] *= 2

                        for y_temp in range(y_ind - 1, 0, -1):
                            array_temp[x_ind][y_temp] = array_temp[x_ind][y_temp - 1]

                        array_temp[x_ind][0] = 0

        return array_temp

    def best_move_EMM(self, board, current_score, depth=6):
        """
        This function calls the expectiminimax algorithm and gathers possible moves,
        then chooses the best move based based on the heuristis score.
        """
        best_score = -INFINITY
        best_next_move = ""
        print("Depth is:", depth)
        testing_board = deepcopy(board)
        best_score, best_next_move = self.expectiminimax(testing_board, depth)

        return best_next_move, best_score

    def open_spots(self, board):
        """
        Checks all the open tiles in the board.
        """
        empty_spots = []
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    empty_spots.append((i, j))

        return empty_spots

    def add_tile(self, board, location, value=None):
        """
        Adds tile in given spot. This function is used for testing.
        """
        i, j = location

        if value:
            board[i][j] = 0
            return

        board[i][j] = 2

        return

    def expectiminimax(self, board, depth, direction = None):
        """
        Expectiminimax function that also uses pruning,
        it checks at max the top 8 most valuable tiles.
        """

        if not self.game_logic.moves_possible(board):
            return -INFINITY, direction

        if depth < 0:
            return self.heuristic.heuristicValue(board), direction
        a = 0
        if depth % 2 == 0:
            a = -INFINITY
            for next_direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
                testing_board = deepcopy(board)
                old_board = deepcopy(board)

                testing_board = self.take_turn(next_direction, testing_board)

                if testing_board != old_board:
                    response = self.expectiminimax(
                        testing_board, depth - 1, next_direction
                    )
                    if response[0] > a:
                        a = response[0]
                        direction = response[1]
        elif depth % 2 != 0:
            a = 0
            open_tiles = self.open_spots(board)

            open_tiles = sorted(
                open_tiles,
                key=lambda loc: self.heuristic.tile_weight(loc),
                reverse=True,
            )
            open_tiles = open_tiles[: self.max_tiles]

            for prob, value in [(0.9, 2), (0.1, 4)]:
                for location in open_tiles:
                    self.add_tile(board, location, value)
                    response = (
                        prob * self.expectiminimax(board, depth - 1, direction)[0]
                    )
                    a += response
                    self.add_tile(board, location)
        return a, direction
