"""
Here I define what is the ideal tile order on the board,
this is the most popular shape I could find related to this game. It's
called the Snake shape. 
"""

IDEAL_SNAKE = [
    [2**15, 2**14, 2**13, 2**12],
    [2**11, 2**10, 2**9, 2**8],
    [2**7, 2**6, 2**5, 2**4],
    [2**3, 2**2, 2**1, 2**0],
]

class Heuristic:
    """This class has the current heuristic score of a board"""

    def heuristicValue(self, board):
        """
        This function returns the sum of the score on the snakeboard
        with each tile multiplied by its corresponding ideal shape value
        """
        heuristicValue = 0
        for i in range(4):
            for j in range(4):
                heuristicValue += board[i][j] * IDEAL_SNAKE[i][j]
        return heuristicValue

    def tile_weight(self, location):
        """
        This function returns the weight of a tile based on its location.
        It uses the IDEAL_SNAKE to determine the weight.
        """
        i, j = location
        return IDEAL_SNAKE[i][j]
