import unittest

from ai_solver_logic import ExpectMMAI
from game_logic import Logic


class TestAiLogic(unittest.TestCase):
    def setUp(self):
        self.ai_game = ExpectMMAI()
        self.game_logic = Logic()

    def test_take_turn_detects_movement(self):
        board_values = [[2, 0, 0, 0], 
                        [2, 0, 0, 0], 
                        [2, 4, 0, 0], 
                        [2, 0, 0, 0]]

        other_board = [[2, 0, 0, 0], 
                       [2, 0, 0, 0], 
                       [2, 4, 0, 0], 
                       [2, 0, 0, 0]]

        board_values = self.ai_game.take_turn("LEFT", board_values)

        assert board_values == other_board

    def test_best_move_EMM(self):
        # Test that the best move is selected
        board_values = [[2, 2, 0, 0], [2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        expected_best_move = "DOWN"

        best_move, _ = self.ai_game.best_move_EMM(board_values, depth=2)

        self.assertEqual(best_move, expected_best_move)

    def test_correct_movement(self):

        board_values = [[2, 128, 64, 0], [0, 0, 32, 2], [0, 0, 0, 8], [0, 0, 0, 2]]

        new_board_values, _, _ = self.game_logic.take_turn("LEFT", board_values, 0)

        expected_board = [[2, 128, 64, 0], [32, 2, 0, 0], [8, 0, 0, 0], [2, 0, 0, 0]]

        self.assertEqual(new_board_values, expected_board)
