"""
This is the main Gameloop where the game runs
"""
import copy
import random
import os
import pygame
from game_logic import Logic
from graphics import RenderGame

WIDTH = 600
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048 Game")
timer = pygame.time.Clock()
fps = 60


class GameLoop:
    """The game is initialized and run here"""

    def __init__(self):
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
        self.spawn_new = True
        self.game_over = False
        self.start_count = 0
        self.direction = ""
        self.score = 0
        self.init_high = 0
        self.high_score = 0
        self.set_up_high_score()

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
            if self.direction != "":
                old_board = copy.deepcopy(self.board_values)
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

            if self.game_over:
                self.game_graphics.draw_over(screen)
                if self.high_score > self.init_high:
                    scores_file_path = os.path.join(
                        os.path.dirname(os.path.abspath(
                            __file__)), "scores.txt"
                    )
                    with open(scores_file_path, "w") as file:
                        file.write(f"{self.high_score}")
                    file.close()
                    self.init_high = self.high_score

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.direction = "UP"
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.direction = "DOWN"
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.direction = "LEFT"
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.direction = "RIGHT"

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
