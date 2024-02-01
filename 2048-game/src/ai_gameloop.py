"""
This is the main Gameloop where the game runs
"""
import os
import random
from copy import deepcopy

import pygame
from ai_solver_logic import ExpectMMAI
from game_logic import Logic
from graphics import RenderGame

WIDTH = 600
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048 Game")
timer = pygame.time.Clock()
fps = 60


class AiGameLoop:
    """The game is initialized and run here"""

    def __init__(self):
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
        self.spawn_new = True
        self.make_moves = True
        self.game_over = False
        self.start_count = 0
        self.direction = ""
        self.score = 0
        self.init_high = 0
        self.high_score = 0
        self.set_up_high_score()
        self.ai_player = ExpectMMAI()

    def set_up_high_score(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        scores_file_path = os.path.join(script_directory, "scores.txt")

        with open(scores_file_path, "r") as file:
            self.init_high = int(file.readline())
        file.close()

        self.high_score = self.init_high

    def set_up_game(self):
        """Initialize Logic and Graphics modules"""
        self.game_logic = Logic()
        self.game_graphics = RenderGame()

    def play(self):
        """main loop"""
        run = True
        old_board = None
        while run:
            timer.tick(fps)
            screen.fill("gray")
            self.game_graphics.draw_board(screen, self.score, self.high_score)
            self.game_graphics.draw_pieces(self.board_values, screen)

            if self.make_moves:
                self.direction, self.score = self.ai_player.best_move_EMM(
                    self.board_values, self.score
                )

            if self.direction != "":
                old_board = deepcopy(self.board_values)

                self.board_values, self.score = self.game_logic.take_turn(
                    self.direction, self.board_values, self.score
                )

                self.direction = ""
                if self.start_count < 2:
                    self.spawn_new = True
                else:
                    self.spawn_new = self.board_values != old_board

            if self.spawn_new or self.start_count < 2:
                self.board_values, self.game_over = self.game_logic.new_pieces(
                    self.board_values
                )
                for row in self.board_values:
                    print(row)

                print("Checking in main loop:", self.game_over)
                self.spawn_new = False
                self.start_count += 1

                if self.start_count > 2:
                    self.make_moves = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                    if self.game_over:
                        if event.key == pygame.K_RETURN:
                            self.board_values = [
                                [0 for _ in range(4)] for _ in range(4)
                            ]
                            self.spawn_new = True
                            self.start_count = 0
                            self.score = 0
                            self.direction = ""
                            self.game_over = False

            if self.score > self.high_score:
                self.high_score = self.score

            pygame.display.flip()

        pygame.quit()
