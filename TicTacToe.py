import pygame
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((620, 578))
pygame.display.set_caption("TICTACTOE")
font = pygame.font.SysFont(None, 60)

# Load images
img_x = pygame.image.load("images\\img_x.png")
img_o = pygame.image.load("images\\img_o.png")
img_grid = pygame.image.load("images\\grid2.png")
img_win_x = pygame.image.load("images\\win_x.jpg")
img_win_o = pygame.image.load("images\\win_o.jpg")
img_tie = pygame.image.load("images\\win_t.jpg")

# Box positions
box_positions = [
    (63, 46), (231, 46), (404, 46),
    (63, 210), (231, 210), (404, 210),
    (63, 380), (231, 380), (404, 380)
]
boxes = [pygame.Rect(x, y, 155, 151) for (x, y) in box_positions]

# Game state
board = [0] * 9  # 0: empty, 1: X, 2: O
running = True
turn = 1
game_mode = None  # "1P" or "2P"
start_screen = True
game_over = False

def reset_game():
    global board, turn, game_over, game_mode, start_screen
    board = [0] * 9
    turn = 1
    game_over = False
    game_mode = None
    start_screen = True

def check_win(b):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for i, j, k in wins:
        if b[i] == b[j] == b[k] != 0:
            return b[i]
    if all(x != 0 for x in b):
        return 3  # Tie
    return 0

def draw_board():
    screen.blit(img_grid, (0, 0))
    for i, mark in enumerate(board):
        if mark == 1:
            screen.blit(img_x, box_positions[i])
        elif mark == 2:
            screen.blit(img_o, box_positions[i])

def minimax(b, is_max):
    winner = check_win(b)
    if winner == 1: return -1
    if winner == 2: return 1
    if winner == 3: return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == 0:
                b[i] = 2
                best = max(best, minimax(b, False))
                b[i] = 0
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == 0:
                b[i] = 1
                best = min(best, minimax(b, True))
                b[i] = 0
        return best

def best_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == 0:
            board[i] = 2
            score = minimax(board, False)
            board[i] = 0
            if score > best_score:
                best_score = score
                move = i
    if move != -1:
        board[move] = 2

def draw_start_screen():
    screen.fill((30, 30, 30))
    title = font.render("TIC TAC TOE", True, (255, 255, 255))
    btn1 = font.render("1 Player", True, (0, 0, 0))
    btn2 = font.render("2 Player", True, (0, 0, 0))

    btn1_rect = pygame.Rect(180, 220, 260, 60)
    btn2_rect = pygame.Rect(180, 320, 260, 60)

    pygame.draw.rect(screen, (200, 200, 200), btn1_rect)
    pygame.draw.rect(screen, (200, 200, 200), btn2_rect)

    screen.blit(title, (190, 100))
    screen.blit(btn1, (btn1_rect.x + 50, btn1_rect.y + 5))
    screen.blit(btn2, (btn2_rect.x + 50, btn2_rect.y + 5))

    return btn1_rect, btn2_rect

def draw_end_screen(winner):
    if winner == 1:
        screen.blit(img_win_x, (0, 0))
    elif winner == 2:
        screen.blit(img_win_o, (0, 0))
    elif winner == 3:
        screen.blit(img_tie, (0, 0))

    # "Play Again" and "Quit" buttons (rounded)
    again_rect = pygame.Rect(170, 490, 140, 50)
    quit_rect = pygame.Rect(310, 490, 140, 50)

    pygame.draw.rect(screen, (255, 255, 255), again_rect, border_radius=30)
    pygame.draw.rect(screen, (255, 80, 80), quit_rect, border_radius=30)

    again_text = font.render("Play", True, (0, 0, 0))
    quit_text = font.render("Quit", True, (0, 0, 0))

    screen.blit(again_text, (again_rect.x + 35, again_rect.y + 5))
    screen.blit(quit_text, (quit_rect.x + 35, quit_rect.y + 5))

    return again_rect, quit_rect

# MAIN LOOP
while running:
    if start_screen:
        btn1_rect, btn2_rect = draw_start_screen()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn1_rect.collidepoint(event.pos):
                    game_mode = "1P"
                    start_screen = False
                elif btn2_rect.collidepoint(event.pos):
                    game_mode = "2P"
                    start_screen = False

    elif game_over:
        winner = check_win(board)
        again_btn, quit_btn = draw_end_screen(winner)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if again_btn.collidepoint(event.pos):
                    reset_game()
                elif quit_btn.collidepoint(event.pos):
                    running = False

    else:
        result = check_win(board)
        if result != 0:
            game_over = True
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                for i, box in enumerate(boxes):
                    if box.collidepoint(pos) and board[i] == 0:
                        board[i] = turn
                        if game_mode == "1P":
                            if check_win(board) == 0:
                                best_move()
                        else:
                            turn = 3 - turn
                        break

        draw_board()
        pygame.display.update()
