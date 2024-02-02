import unittest
from ai_solver_logic import ExpectMMAI


class TestAiLogic(unittest.TestCase):
    def setUp(self):
        self.ai_game = ExpectMMAI()

    def test_take_turn_detects_movement(self):
        board_values = [
            [2,0,0,0],
            [2,0,0,0],
            [2,4,0,0],
            [2,0,0,0]
        ]

        board_values, hadMovement = self.ai_game.take_turn("LEFT",board_values)

        assert (hadMovement == False)
    