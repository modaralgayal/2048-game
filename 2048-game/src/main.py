import random

import pygame

pygame.init()


WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048 Game")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 24)


# Draw Canvas
def draw_board():
    pygame.draw.rect(screen, colors["bg"], [0, 0, 400, 400], 0, 10)
    pass


# Different Tile colors
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

# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]


# Draw Tiles for each turn
def draw_pieces(board):
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
            coordinate = [j * 95 + 20, i * 95 + 20, 75, 75]
            pygame.draw.rect(screen, color, coordinate, 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font("freesansbold.ttf", 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(
                    screen, "black", [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5
                )


# Gameloop
run = True

while run:
    timer.tick(fps)
    screen.fill("gray")
    draw_board()
    draw_pieces(board_values)
    if spawn_new:
        board_values = new_pieces(board_values)
        spawn_new = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
