"""
This module is responsible for rendering all the data in the UI
"""
import pygame

colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    "light text": (249, 246, 242),
    "dark text": (119, 110, 101),
    "other": (0, 0, 0),
    "bg": (255, 230, 153),
}


class RenderGame:
    """ This is the rendering module that gets called in the Gameloop """

    def __init__(self):
        self.font = pygame.font.Font("freesansbold.ttf", 24)

    def draw_board(self, screen, score, high_score):
        """ This function simply renders the board (as a canvas) and the scores """
        pygame.draw.rect(screen, colors["bg"], [100, 200, 400, 400], 0, 10)
        score_text = self.font.render(f"Score: {score}", True, "black")
        high_score_text = self.font.render(
            f"High Score: {high_score}", True, "black")
        screen.blit(score_text, (110, 20))
        screen.blit(high_score_text, (110, 70))

    def draw_over(self, screen):
        """ This function is the game_over screen (doesn't work yet) """
        print("GameOVerv function")
        pygame.draw.rect(screen, "black", [50, 50, 300, 100], 0, 10)
        game_over_text1 = self.font.render("Game Over!", True, "white")
        game_over_text2 = self.font.render(
            "Press Enter to Restart", True, "white")
        screen.blit(game_over_text1, (130, 65))
        screen.blit(game_over_text2, (70, 105))

    def draw_pieces(self, board, screen):
        """ This method draws every piece when the game board is updated """
        for i in range(4):
            for j in range(4):
                value = board[i][j]
                if value > 8:
                    value_color = colors["light text"]
                else:
                    value_color = colors["dark text"]
                if value <= 2048:
                    color = colors[value]
                else:
                    color = colors["other"]
                coordinate = (j * 95 + 120, i * 95 + 220, 75, 75)
                pygame.draw.rect(screen, color, coordinate, 0, 5)
                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font(
                        "freesansbold.ttf", 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(
                        center=(j * 95 + 157, i * 95 + 257))
                    screen.blit(value_text, text_rect)
                    pygame.draw.rect(screen, "black", coordinate, 2, 5)
