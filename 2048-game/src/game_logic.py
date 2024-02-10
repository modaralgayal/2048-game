"""
This Module is responsible for the moves made on the board, such
as merging the tiles in the game and keeping score.
"""

from random import randint
from copy import deepcopy


class Logic:
    """This Class Handles the board Logic"""

    def __init__(self):
        pass

    def take_turn(self, direc, board, score):
        array_temp = [[0 for x in range(0,4)] for x in range(0,4)]
        for x in range(0,16):
            array_temp[x%4][x//4] = board[x%4][x//4]
        hadMovement = False

        
        if(direc == 'UP'):
            for y_ind in range(0,4):

                for x_ind in range(0,4):

                    if(array_temp[x_ind][y_ind] == 0):
                        for x_temp in range(x_ind+1,4):
                            if(array_temp[x_temp][y_ind]):
                                array_temp[x_ind][y_ind] = array_temp[x_temp][y_ind]
                                array_temp[x_temp][y_ind] = 0
                                hadMovement = True
                                break                    

                for x_ind in range(0,3):
                    if(array_temp[x_ind][y_ind] == array_temp[x_ind+1][y_ind] and array_temp[x_ind][y_ind] != 0): 
                        array_temp[x_ind][y_ind] *= 2
                        score += array_temp[x_ind][y_ind]

                        for x_temp in range(x_ind+1,3):
                            array_temp[x_temp][y_ind] = array_temp[x_temp+1][y_ind]
                            hadMovement = True


                        array_temp[3][y_ind] = 0

        if(direc == 'DOWN'):
            for y_ind in range(0,4):

                for x_ind in range(3,-1,-1):

                    if(array_temp[x_ind][y_ind] == 0):
                        for x_temp in range(x_ind-1,-1,-1):
                            if(array_temp[x_temp][y_ind]):
                                array_temp[x_ind][y_ind] = array_temp[x_temp][y_ind]
                                array_temp[x_temp][y_ind] = 0
                                hadMovement = True
                                break                    

                for x_ind in range(3,0,-1):
                    if(array_temp[x_ind][y_ind] == array_temp[x_ind-1][y_ind] and array_temp[x_ind][y_ind] != 0): 
                        array_temp[x_ind][y_ind] *= 2
                        score += array_temp[x_ind][y_ind]

                        for x_temp in range(x_ind-1,0,-1):
                            array_temp[x_temp][y_ind] = array_temp[x_temp-1][y_ind]
                            hadMovement = True

                        array_temp[0][y_ind] = 0

        if(direc == 'LEFT'):
            for x_ind in range(0,4):

                for y_ind in range(0,4):

                    if(array_temp[x_ind][y_ind] == 0):
                        for y_temp in range(y_ind+1,4):
                            if(array_temp[x_ind][y_temp]):
                                array_temp[x_ind][y_ind] = array_temp[x_ind][y_temp]
                                array_temp[x_ind][y_temp] = 0
                                hadMovement = True
                                break                    

                for y_ind in range(0,3):
                    if(array_temp[x_ind][y_ind] == array_temp[x_ind][y_ind+1] and array_temp[x_ind][y_ind] != 0): 
                        array_temp[x_ind][y_ind] *= 2
                        score += array_temp[x_ind][y_ind]
                        hadMovement = True

                        for y_temp in range(y_ind+1,3):
                            array_temp[x_ind][y_temp] = array_temp[x_ind][y_temp+1]
                            hadMovement = True


                        array_temp[x_ind][3] = 0

        if(direc == 'RIGHT'):
            for x_ind in range(0,4):

                for y_ind in range(3,-1,-1):

                    if(array_temp[x_ind][y_ind] == 0):
                        for y_temp in range(y_ind-1,-1,-1):
                            if(array_temp[x_ind][y_temp]):
                                array_temp[x_ind][y_ind] = array_temp[x_ind][y_temp]
                                array_temp[x_ind][y_temp] = 0
                                hadMovement = True

                                break                    

                for y_ind in range(3,0,-1):
                    if(array_temp[x_ind][y_ind] == array_temp[x_ind][y_ind-1] and array_temp[x_ind][y_ind] != 0): 
                        array_temp[x_ind][y_ind] *= 2
                        score += array_temp[x_ind][y_ind]

                        for y_temp in range(y_ind-1,0,-1):
                            array_temp[x_ind][y_temp] = array_temp[x_ind][y_temp-1]
                            hadMovement = True


                        array_temp[x_ind][0] = 0

        
        return (array_temp, score, hadMovement)    

    def moves_possible(self, board):
        """
        Check if there are any possible moves left on the board.
        Returns True if there are moves left, False otherwise.
        """
        # Check if any adjacent tiles have the same value
        for i in range(4):
            for j in range(4):
                if i > 0 and board[i][j] == board[i - 1][j]:
                    return True
                if i < 3 and board[i][j] == board[i + 1][j]:
                    return True
                if j > 0 and board[i][j] == board[i][j - 1]:
                    return True
                if j < 3 and board[i][j] == board[i][j + 1]:
                    return True

        # Check if there are any empty tiles
        for row in board:
            if 0 in row:
                return True

        # No possible moves left
        return False

    def new_pieces(self, board):
        """
        Generate a new tile in a random empty spot
        """
        # print("board in new_pieces")

        placable = []
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    placable.append((i, j))

        row, col = placable[randint(0, len(placable) - 1)]

        if randint(1, 10) == 10:
            board[row][col] = 4
        else:
            board[row][col] = 2

        empty_spots = []
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    empty_spots.append((i, j))

        return board
        
