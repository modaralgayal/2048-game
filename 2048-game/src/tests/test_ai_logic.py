import unittest

from ai_solver_logic import ExpectMMAI


class TestAiLogic(unittest.TestCase):
    def setUp(self):
        self.ai_game = ExpectMMAI()

    def test_take_turn_detects_movement(self):
        board_values = [[2, 0, 0, 0], [2, 0, 0, 0], [2, 4, 0, 0], [2, 0, 0, 0]]

        other_board = [[2, 0, 0, 0], [2, 0, 0, 0], [2, 4, 0, 0], [2, 0, 0, 0]]

        board_values = self.ai_game.take_turn("LEFT", board_values)

        assert board_values == other_board

    def test_best_move_EMM(self):
        # Test that the best move is selected
        board_values = [[2, 2, 0, 0], 
                        [2, 4, 0, 0], 
                        [0, 0, 0, 0], 
                        [0, 0, 0, 0]]

        expected_best_move = "DOWN"

        best_move, _ = self.ai_game.best_move_EMM(board_values, depth=2)

        self.assertEqual(best_move, expected_best_move)
