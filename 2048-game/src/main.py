import copy
import random

import pygame

pygame.init()


WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048 Game")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 24)


# Draw Canvas
def draw_board():
    pygame.draw.rect(screen, colors["bg"], [100, 200, 400, 400], 0, 10)
    score_text = font.render(f"Score: {score}", True, "black")
    high_score_text = font.render(f"High Score: {high_score}", True, "black")
    screen.blit(score_text, (110, 20))
    screen.blit(high_score_text, (110, 70))
    pass


# take your turn based on direction
# Make these eventually into 4 different functions se they can be called seperately
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == "UP":
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        # Here we move the piece upwards by however many zeros (empty spaces) have been found above.
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if (
                        board[i - shift - 1][j] == board[i - shift][j]
                        and not merged[i - shift][j]
                        and not merged[i - shift - 1][j]
                    ):
                        # If the piece above has the same value as the moved piece, they
                        # merge and the piece gets double its value
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == "DOWN":
        # check this if an error occurs
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if (
                        board[2 - i + shift][j] == board[3 - i + shift][j]
                        and not merged[3 - i + shift][j]
                        and not merged[2 - i + shift][j]
                    ):
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == "LEFT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if (
                    board[i][j - shift] == board[i][j - shift - 1]
                    and not merged[i][j - shift - 1]
                    and not merged[i][j - shift]
                ):
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == "RIGHT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if (
                        board[i][4 - j + shift] == board[i][3 - j + shift]
                        and not merged[i][4 - j + shift]
                        and not merged[i][3 - j + shift]
                    ):
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True

    return board


# draw game over and restart test
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))



# spawn new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full_board = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2

    if count < 1:
        full_board = True
        print("Board is full")
    return board, full_board


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
game_over = False
spawn_new = True
start_count = 0
direction = ""
score = 0
file = open("./scores", "r")
init_high = int(file.readline())
file.close()
high_score = init_high


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
            coordinate = (j * 95 + 120, i * 95 + 220, 75, 75)
            pygame.draw.rect(screen, color, coordinate, 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font("freesansbold.ttf", 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 157, i * 95 + 257))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, "black", coordinate, 2, 5)


# Gameloop
run = True
old_board = None

while run:
    timer.tick(fps)
    screen.fill("gray")
    draw_board()
    draw_pieces(board_values)
    if spawn_new or start_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        start_count += 1
    if direction != "":
        old_board = copy.deepcopy(board_values)
        board_values = take_turn(direction, board_values)
        direction = ""
        if start_count < 2:
            spawn_new = True
        else:
            spawn_new = board_values != old_board
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open("./scores", "w")
            file.write(f"{high_score}")
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                direction = "UP"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                direction = "DOWN"
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                direction = "RIGHT"
            
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    start_count = 0
                    score = 0
                    direction = ""
                    game_over = False
    
    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()
