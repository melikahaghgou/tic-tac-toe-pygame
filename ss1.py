

import pygame
import sys

pygame.init()

pygame.key.set_repeat(400, 35)

WIDTH, HEIGHT = 540, 680
HEADER_HEIGHT = 160
BOARD_SIZE = 540
CELL_SIZE = BOARD_SIZE // 3

BG_COLOR = (15, 17, 26)
CARD_COLOR = (23, 26, 38)
GRID_LINE_COLOR = (42, 46, 68)
HOVER_COLOR = (30, 34, 52)
INPUT_BG = (19, 21, 32)
INPUT_BORDER = (55, 62, 90)
INPUT_ACTIVE = (0, 229, 255)

COLOR_X = (255, 75, 110)
COLOR_O = (0, 229, 255)
COLOR_TEXT = (240, 243, 250)
COLOR_MUTED = (110, 115, 135)
COLOR_BUTTON = (38, 43, 64)
COLOR_BUTTON_HOVER = (58, 65, 96)
COLOR_WIN_X = (50, 24, 36)
COLOR_WIN_O = (18, 45, 55)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Modern Neon Edition")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("segoeui,arial", 28, bold=True)
font_sub = pygame.font.SysFont("segoeui,arial", 15)
font_label = pygame.font.SysFont("segoeui,arial", 16, bold=True)
font_input = pygame.font.SysFont("segoeui,arial", 18)
font_score = pygame.font.SysFont("segoeui,arial", 16, bold=True)
font_btn = pygame.font.SysFont("segoeui,arial", 15, bold=True)
font_msg = pygame.font.SysFont("segoeui,arial", 22, bold=True)

state = "MENU"
player1_name = ""
player2_name = ""
active_input = 1
board = [[0] * 3 for _ in range(3)]
current_player = 1
game_over = False
winner = None
winning_cells = []
score_x = 0
score_o = 0

input1_rect = pygame.Rect(WIDTH // 2 - 140, 260, 280, 44)
input2_rect = pygame.Rect(WIDTH // 2 - 140, 355, 280, 44)
start_btn_rect = pygame.Rect(WIDTH // 2 - 90, 445, 180, 45)
reset_btn_rect = pygame.Rect(WIDTH // 2 - 55, 112, 110, 34)

def check_winner():
    global winner, winning_cells
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            winner = board[i][0]
            winning_cells = [(i, 0), (i, 1), (i, 2)]
            return True
        if board[0][i] == board[1][i] == board[2][i] != 0:
            winner = board[0][i]
            winning_cells = [(0, i), (1, i), (2, i)]
            return True

    if board[0][0] == board[1][1] == board[2][2] != 0:
        winner = board[0][0]
        winning_cells = [(0, 0), (1, 1), (2, 2)]
        return True

    if board[0][2] == board[1][1] == board[2][0] != 0:
        winner = board[0][2]
        winning_cells = [(0, 2), (1, 1), (2, 0)]
        return True

    return False

def is_draw():
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                return False
    return True

def reset_round():
    global board, current_player, game_over, winner, winning_cells
    board = [[0] * 3 for _ in range(3)]
    current_player = 1
    game_over = False
    winner = None
    winning_cells = []

def start_match():
    global state, player1_name, player2_name
    player1_name = player1_name.strip() if player1_name.strip() else "Player 1"
    player2_name = player2_name.strip() if player2_name.strip() else "Player 2"
    state = "GAME"

def draw_x(center, size=42, color=COLOR_X, width=9):
    x, y = center
    pygame.draw.line(screen, color, (x - size, y - size), (x + size, y + size), width)
    pygame.draw.line(screen, color, (x - size, y + size), (x + size, y - size), width)

def draw_o(center, radius=44, color=COLOR_O, width=8):
    pygame.draw.circle(screen, color, center, radius, width)

def render_menu(mouse_pos):
    screen.fill(BG_COLOR)

    title_surf = font_title.render("TIC TAC TOE", True, COLOR_TEXT)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 85))

    sub_surf = font_sub.render("Enter player names to start the match", True, COLOR_MUTED)
    screen.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, 130))

    cursor_visible = (pygame.time.get_ticks() // 500) % 2 == 0

    lbl1 = font_label.render("Player 1 (X):", True, COLOR_X)
    screen.blit(lbl1, (input1_rect.x, input1_rect.y - 24))
    b1_color = INPUT_ACTIVE if active_input == 1 else INPUT_BORDER
    pygame.draw.rect(screen, INPUT_BG, input1_rect, border_radius=8)
    pygame.draw.rect(screen, b1_color, input1_rect, 2, border_radius=8)

    if player1_name:
        txt1 = font_input.render(player1_name, True, COLOR_TEXT)
        screen.blit(txt1, (input1_rect.x + 14, input1_rect.y + 11))
        if active_input == 1 and cursor_visible:
            cx = input1_rect.x + 14 + txt1.get_width() + 2
            pygame.draw.line(screen, COLOR_TEXT, (cx, input1_rect.y + 10), (cx, input1_rect.y + 34), 2)
    else:
        ph1 = font_input.render("Type name here...", True, COLOR_MUTED)
        screen.blit(ph1, (input1_rect.x + 14, input1_rect.y + 11))
        if active_input == 1 and cursor_visible:
            pygame.draw.line(screen, COLOR_TEXT, (input1_rect.x + 14, input1_rect.y + 10), (input1_rect.x + 14, input1_rect.y + 34), 2)

    lbl2 = font_label.render("Player 2 (O):", True, COLOR_O)
    screen.blit(lbl2, (input2_rect.x, input2_rect.y - 24))
    b2_color = INPUT_ACTIVE if active_input == 2 else INPUT_BORDER
    pygame.draw.rect(screen, INPUT_BG, input2_rect, border_radius=8)
    pygame.draw.rect(screen, b2_color, input2_rect, 2, border_radius=8)

    if player2_name:
        txt2 = font_input.render(player2_name, True, COLOR_TEXT)
        screen.blit(txt2, (input2_rect.x + 14, input2_rect.y + 11))
        if active_input == 2 and cursor_visible:
            cx = input2_rect.x + 14 + txt2.get_width() + 2
            pygame.draw.line(screen, COLOR_TEXT, (cx, input2_rect.y + 10), (cx, input2_rect.y + 34), 2)
    else:
        ph2 = font_input.render("Type name here...", True, COLOR_MUTED)
        screen.blit(ph2, (input2_rect.x + 14, input2_rect.y + 11))
        if active_input == 2 and cursor_visible:
            pygame.draw.line(screen, COLOR_TEXT, (input2_rect.x + 14, input2_rect.y + 10), (input2_rect.x + 14, input2_rect.y + 34), 2)

    btn_clr = COLOR_BUTTON_HOVER if start_btn_rect.collidepoint(mouse_pos) else COLOR_BUTTON
    pygame.draw.rect(screen, btn_clr, start_btn_rect, border_radius=10)
    pygame.draw.rect(screen, INPUT_BORDER, start_btn_rect, 1, border_radius=10)
    btn_txt = font_btn.render("START MATCH", True, COLOR_TEXT)
    screen.blit(btn_txt, (start_btn_rect.centerx - btn_txt.get_width() // 2, start_btn_rect.centery - btn_txt.get_height() // 2))

def render_hud(mouse_pos):
    pygame.draw.rect(screen, CARD_COLOR, (0, 0, WIDTH, HEADER_HEIGHT))
    pygame.draw.line(screen, GRID_LINE_COLOR, (0, HEADER_HEIGHT), (WIDTH, HEADER_HEIGHT), 2)

    p1_str = f"{player1_name} (X): {score_x}"
    p2_str = f"{player2_name} (O): {score_o}"
    s1 = font_score.render(p1_str, True, COLOR_X)
    s2 = font_score.render(p2_str, True, COLOR_O)
    screen.blit(s1, (24, 20))
    screen.blit(s2, (WIDTH - 24 - s2.get_width(), 20))

    if not game_over:
        curr_name = player1_name if current_player == 1 else player2_name
        turn_txt = f"{curr_name}'s Turn"
        turn_color = COLOR_X if current_player == 1 else COLOR_O
        t_surf = font_msg.render(turn_txt, True, turn_color)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, 60))
    else:
        if winner == 1:
            msg = f"{player1_name} Won the Game!"
            clr = COLOR_X
        elif winner == 2:
            msg = f"{player2_name} Won the Game!"
            clr = COLOR_O
        else:
            msg = "Match Drawn!"
            clr = COLOR_MUTED
        w_surf = font_msg.render(msg, True, clr)
        screen.blit(w_surf, (WIDTH // 2 - w_surf.get_width() // 2, 60))

    btn_color = COLOR_BUTTON_HOVER if reset_btn_rect.collidepoint(mouse_pos) else COLOR_BUTTON
    pygame.draw.rect(screen, btn_color, reset_btn_rect, border_radius=8)
    pygame.draw.rect(screen, GRID_LINE_COLOR, reset_btn_rect, 1, border_radius=8)
    btn_text = font_btn.render("Reset (R)", True, COLOR_TEXT)
    screen.blit(btn_text, (reset_btn_rect.centerx - btn_text.get_width() // 2, reset_btn_rect.centery - btn_text.get_height() // 2))

def render_board(mouse_pos):
    hover_cell = None
    if not game_over and mouse_pos[1] > HEADER_HEIGHT:
        c = mouse_pos[0] // CELL_SIZE
        r = (mouse_pos[1] - HEADER_HEIGHT) // CELL_SIZE
        if 0 <= r < 3 and 0 <= c < 3 and board[r][c] == 0:
            hover_cell = (r, c)

    for r in range(3):
        for c in range(3):
            rect = pygame.Rect(c * CELL_SIZE, HEADER_HEIGHT + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (r, c) == hover_cell:
                pygame.draw.rect(screen, HOVER_COLOR, rect)
            if (r, c) in winning_cells:
                glow = COLOR_WIN_X if winner == 1 else COLOR_WIN_O
                pygame.draw.rect(screen, glow, rect)

    for i in range(1, 3):
        pygame.draw.line(screen, GRID_LINE_COLOR, (i * CELL_SIZE, HEADER_HEIGHT), (i * CELL_SIZE, HEIGHT), 3)
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, HEADER_HEIGHT + i * CELL_SIZE), (WIDTH, HEADER_HEIGHT + i * CELL_SIZE), 3)

    for r in range(3):
        for c in range(3):
            cx = c * CELL_SIZE + CELL_SIZE // 2
            cy = HEADER_HEIGHT + r * CELL_SIZE + CELL_SIZE // 2
            if board[r][c] == 1:
                draw_x((cx, cy))
            elif board[r][c] == 2:
                draw_o((cx, cy))

while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if input1_rect.collidepoint(event.pos):
                    active_input = 1
                elif input2_rect.collidepoint(event.pos):
                    active_input = 2
                elif start_btn_rect.collidepoint(event.pos):
                    start_match()

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_TAB):
                    active_input = 2
                elif event.key == pygame.K_UP:
                    active_input = 1
                elif event.key == pygame.K_RETURN:
                    if active_input == 1:
                        active_input = 2
                    else:
                        start_match()
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == 1:
                        player1_name = player1_name[:-1]
                    else:
                        player2_name = player2_name[:-1]
                else:
                    if len(event.unicode) > 0 and event.unicode.isprintable():
                        if active_input == 1 and len(player1_name) < 14:
                            player1_name += event.unicode
                        elif active_input == 2 and len(player2_name) < 14:
                            player2_name += event.unicode

        elif state == "GAME":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_round()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if reset_btn_rect.collidepoint(event.pos):
                    reset_round()
                elif not game_over and event.pos[1] > HEADER_HEIGHT:
                    c = event.pos[0] // CELL_SIZE
                    r = (event.pos[1] - HEADER_HEIGHT) // CELL_SIZE
                    if 0 <= r < 3 and 0 <= c < 3 and board[r][c] == 0:
                        board[r][c] = current_player
                        if check_winner():
                            game_over = True
                            if winner == 1:
                                score_x += 1
                            else:
                                score_o += 1
                        elif is_draw():
                            game_over = True
                        else:
                            current_player = 2 if current_player == 1 else 1

    if state == "MENU":
        render_menu(mouse_pos)
    else:
        screen.fill(BG_COLOR)
        render_board(mouse_pos)
        render_hud(mouse_pos)

    pygame.display.flip()
    clock.tick(60)
