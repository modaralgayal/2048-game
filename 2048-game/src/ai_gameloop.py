"""
This is the main Gameloop where the game runs
"""

import asyncio
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
fps = 120


class AiGameLoop:
    """The game is initialized and run here"""

    def __init__(self):
        self.board_values = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.spawn_new = True
        self.make_moves = False
        self.game_over = False
        self.start_count = 0
        self.score = 0
        self.direction = ""
        self.init_high = 0
        self.high_score = 0
        self.set_up_high_score()
        self.ai_player = ExpectMMAI()

    def set_up_high_score(self):
        """ This function establishes connection with the scores file to update the next possible highscore """
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
        """Main game loop"""
        run = True

        while run:
            timer.tick(fps)
            screen.fill("gray")

            self.game_graphics.draw_board(screen, self.score, self.high_score)
            self.game_graphics.draw_pieces(self.board_values, screen)

            if self.make_moves:
                self.direction = self.ai_player.best_move_EMM(self.board_values, self.score)[0]

            if self.direction != "":
                self.board_values, self.score, hadMovement = self.game_logic.take_turn(
                    self.direction, self.board_values, self.score
                )  # Execute the move
                self.direction = ""
                if self.start_count < 2:
                    self.spawn_new = True
                else:
                    self.spawn_new = hadMovement

            if self.spawn_new or self.start_count < 2:
                self.board_values = self.game_logic.new_pieces(
                    self.board_values
                )
                self.spawn_new = False
                self.start_count += 1

                if self.start_count >= 2:
                    self.make_moves = True

            # Check if the game is over
            if not self.game_logic.moves_possible(self.board_values):
                self.game_graphics.draw_over(screen)
                if self.score > self.high_score:
                    self.high_score = self.score
                if self.high_score > self.init_high:
                    self.init_high = self.high_score
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RETURN:
                            # Reset the game
                            self.board_values = [[0 for _ in range(4)] for _ in range(4)]
                            self.spawn_new = True
                            self.start_count = 0
                            self.score = 0
                            self.direction = ""
                            self.game_over = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

               

            if self.score > self.high_score:
                self.high_score = self.score

            pygame.display.flip()

        pygame.quit()
