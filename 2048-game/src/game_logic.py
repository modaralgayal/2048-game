"""
This Module is responsible for the moves made on the board, such
as merging the tiles in the game and keeping score.
"""

from random import randint


class Logic:
    """This Class Handles the board Logic"""

    def __init__(self):
        pass

    def take_turn(self, direc, board, score):
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
                            score += board[i - shift - 1][j]
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
                            score += board[3 - i + shift][j]
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
                        score += board[i][j - shift - 1]
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
                            score += board[i][4 - j + shift]
                            board[i][3 - j + shift] = 0
                            merged[i][4 - j + shift] = True

        return board, score

    def new_pieces(self, board):
        """
        Generate a new tile in a random empty spot
        """
        empty_spots = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]

        if not empty_spots:
            full_board = True
        else:
            row, col = empty_spots[randint(0, len(empty_spots) - 1)]

            if randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2

            full_board = False

        return board, full_board
