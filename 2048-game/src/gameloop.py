import copy
import random
import pygame
from game_logic import Logic
from graphics import RenderGame

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048 Game")
timer = pygame.time.Clock()
fps = 60


class GameLoop:
    def __init__(self):
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
        self.spawn_new = True
        self.game_over = False
        self.start_count = 0
        self.direction = ""
        self.score = 0
        file = open("./scores", "r")
        self.init_high = int(file.readline())
        file.close()
        self.high_score = self.init_high

    def set_up_game(self):
        self.game_logic = Logic()
        self.game_graphics = RenderGame()
    
    def play(self):
        run = True
        old_board = None


        while run:
            timer.tick(fps)
            screen.fill("gray")
            self.game_graphics.draw_board(screen, self.score, self.high_score)
            self.game_graphics.draw_pieces(self.board_values, screen)
            if self.spawn_new or self.start_count < 2:
                self.board_values, self.game_over = self.game_logic.new_pieces(self.board_values)
                print("Checking in main loop:", self.game_over)
                self.spawn_new = False
                self.start_count += 1
            if self.direction != "":
                old_board = copy.deepcopy(self.board_values)
                self.board_values, self.score = self.game_logic.take_turn(self.direction, self.board_values, self.score)
                self.direction = ""
                if self.start_count < 2:
                    self.spawn_new = True
                else:
                    self.spawn_new = self.board_values != old_board
                
            if self.game_over:
                self.game_graphics.draw_over(screen)
                if self.high_score > self.init_high:
                    file = open("./scores", "w")
                    file.write(f"{self.high_score}")
                    file.close()
                    self.init_high = self.high_score

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.direction = "DOWN"
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.direction = "RIGHT"

                    if self.game_over:
                        print("GameOver")
                        if event.key == pygame.K_RETURN:
                            self.board_values = [[0 for _ in range(4)] for _ in range(4)]
                            self.spawn_new = True
                            self.start_count = 0
                            self.score = 0
                            self.direction = ""
                            self.self.game_over = False

            if self.score > self.high_score:
                self.high_score = self.score

            pygame.display.flip()

        pygame.quit()
