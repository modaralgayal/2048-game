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
    def __init__(self) -> None:
        self.game_logic = Logic()
        self.heuristic = Heuristic()
        self.score = 0

    def take_turn(self, direc, board):
        """
        This function handles Up, Down, Left,
        Right moves on the board and updates the score.
        """
        merged = [[False for _ in range(4)] for _ in range(4)]
        if direc == "UP":
            for i in range(4):
                for j in range(4):
                    shift = 0
                    if i > 0:
                        for q in range(i):
                            if board[q][j] == 0:
                                shift += 1
                        if shift > 0:
                            board[i - shift][j] = board[i][j]
                            board[i][j] = 0
                        if (
                            board[i - shift - 1][j] == board[i - shift][j]
                            and not merged[i - shift][j]
                            and not merged[i - shift - 1][j]
                        ):
                            # If the piece above has the same value as the moved piece, they
                            # merge and the piece gets double its value
                            board[i - shift - 1][j] *= 2
                            board[i - shift][j] = 0
                            merged[i - shift - 1][j] = True

        elif direc == "DOWN":
            for i in range(3):
                for j in range(4):
                    shift = 0
                    for q in range(i + 1):
                        if board[3 - q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[2 - i + shift][j] = board[2 - i][j]
                        board[2 - i][j] = 0
                    if 3 - i + shift <= 3:
                        if (
                            board[2 - i + shift][j] == board[3 - i + shift][j]
                            and not merged[3 - i + shift][j]
                            and not merged[2 - i + shift][j]
                        ):
                            board[3 - i + shift][j] *= 2
                            board[2 - i + shift][j] = 0
                            merged[3 - i + shift][j] = True

        elif direc == "LEFT":
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if board[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][j - shift] = board[i][j]
                        board[i][j] = 0
                    if (
                        board[i][j - shift] == board[i][j - shift - 1]
                        and not merged[i][j - shift - 1]
                        and not merged[i][j - shift]
                    ):
                        board[i][j - shift - 1] *= 2
                        board[i][j - shift] = 0
                        merged[i][j - shift - 1] = True

        elif direc == "RIGHT":
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if board[i][3 - q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][3 - j + shift] = board[i][3 - j]
                        board[i][3 - j] = 0
                    if 4 - j + shift <= 3:
                        if (
                            board[i][4 - j + shift] == board[i][3 - j + shift]
                            and not merged[i][4 - j + shift]
                            and not merged[i][3 - j + shift]
                        ):
                            board[i][4 - j + shift] *= 2
                            board[i][3 - j + shift] = 0
                            merged[i][4 - j + shift] = True

        return board

    def best_move_EMM(self, board, depth=2):
        best_score = -INFINITY
        best_next_move = ""
        results = []
        for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            testing_board = deepcopy(board)
            testing_board = self.take_turn(direction, testing_board)
            res = self.expectiminimax(testing_board, depth, direction)
            print(res)
            results.append(res)

        results = [res for res in results]
        print(results)

        for res in results:
            if res[0] >= best_score:
                best_score = res[0]
                best_next_move = res[1]

        self.score = best_score

        print(best_next_move)
        print(results)


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
            board[i][j] = 2

        return

    def expectiminimax(self, board, depth, direction):
        if not self.game_logic.moves_possible(board):
            print("fails right here")
            return -INFINITY, direction
        
        if depth < 0:
            return self.heuristic.heuristicValue(board), direction

        a = 0
        if depth != int(depth):
            a = -INFINITY
            for next_direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
                testing_board = deepcopy(board)
                old_board = deepcopy(board)

                testing_board = self.take_turn(next_direction, testing_board)

                if testing_board != old_board:
                    response = self.expectiminimax(
                        testing_board, depth - 0.5, next_direction
                    )[0]
                    if response > a:
                        a = response
        elif depth == int(depth):
            a = 0
            open_tiles = self.open_spots(board)
            for location in open_tiles:
                self.add_tile(board, location)
                #print("working here")
                response = (
                    1.0
                    / len(open_tiles)
                    * self.expectiminimax(board, depth - 0.5, direction)[0]
                )
                a += response
                self.add_tile(board, location)
        return a, direction

