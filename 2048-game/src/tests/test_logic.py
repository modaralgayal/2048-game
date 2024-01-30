import unittest

from game_logic import Logic


class TestLogic(unittest.TestCase):
    def setUp(self):
        self.logic = Logic()

    def test_take_turn_up(self):
        board = [[2, 0, 0, 2], [4, 0, 0, 2], [2, 2, 2, 2], [0, 0, 4, 4]]
        score = 0

        new_board, new_score = self.logic.take_turn("UP", board, score)

        self.assertEqual(new_board[0][3], 4)
        self.assertTrue(new_score >= 4)

    def test_take_turn_down(self):
        board = [[2, 0, 0, 2], [4, 0, 0, 2], [2, 2, 2, 2], [0, 0, 4, 4]]
        score = 0

        new_board, new_score = self.logic.take_turn("DOWN", board, score)

        self.assertEqual(new_board[2][3], 4)
        self.assertTrue(new_score >= 4)

    def test_take_turn_left(self):
        board = [[2, 0, 0, 2], [4, 0, 0, 2], [2, 2, 2, 2], [0, 0, 4, 4]]
        score = 0

        new_board, new_score = self.logic.take_turn("LEFT", board, score)

        self.assertEqual(new_board[2][0], 4)
        self.assertEqual(new_board[2][1], 4)
        self.assertTrue(new_score >= 4)

    def test_take_turn_right(self):
        board = [[2, 0, 0, 2], [4, 0, 0, 2], [2, 2, 2, 2], [0, 0, 4, 4]]
        score = 0

        new_board, new_score = self.logic.take_turn("RIGHT", board, score)

        self.assertEqual(new_board[0][3], 4)
        self.assertTrue(new_score >= 4)

    def test_new_pieces(self):
        new_board, full_board = self.logic.new_pieces(
            [[2, 4, 2, 0], [4, 0, 2, 0], [2, 2, 0, 0], [0, 0, 4, 0]]
        )

        self.assertNotEqual(
            new_board, [[2, 4, 2, 0], [4, 0, 2, 0], [2, 2, 0, 0], [0, 0, 4, 0]]
        )
        self.assertFalse(full_board)


if __name__ == "__main__":
    unittest.main()
