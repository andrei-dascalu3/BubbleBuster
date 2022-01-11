import pygame
from pygame.image import load
from Bubble import Bubble
from bubble_colors import *
from math import sqrt
from copy import deepcopy
from game_data import *

def init_grid(seed, origin):
    global shooter_ball
    config_file = open('GridConfigs/' + seed + '.txt', 'r')
    lines = config_file.readlines()
    odd = 1
    posy = origin[1]
    for line in lines:
        odd = (odd + 1) % 2
        posx = origin[0] + radius * odd
        row = []
        for ch in line:
            if ch == 'o':
                row.append(Bubble(random_color(), (posx, posy)))
                posx += radius * 2
            elif ch == '-':
                posx += radius * 2
        grid.append(row)
        posy += radius * 2

    # create shooter ball
    shooter_ball = Bubble(random_color(), default_pos)

def draw_board():
    global board
    board = pygame.Surface((board_width, HEIGHT))
    board.set_alpha(200)
    board.fill(non_colors['DARK_GRAY'])
    upper_rect = pygame.Rect(WIDTH/20 - radius, HEIGHT/20 - radius * 2, board_width, radius)
    WIN.blit(board, (WIDTH/20 - radius, HEIGHT/20 - radius))
    pygame.draw.rect(WIN, non_colors['BLACK'], upper_rect)

def draw_info_text(color, msg_font, msg, origin, width, lines):
    text = msg_font.render(msg, True, color)
    text_rect = text.get_rect(center=(origin[0] + width / 2, origin[1] + radius * lines))
    WIN.blit(text, text_rect)

def draw_info():
    info_board_width = 9 * radius
    info_board = pygame.Surface((info_board_width, HEIGHT))
    info_board.set_alpha(200)
    info_board.fill(non_colors['DARK_GRAY'])
    upper_rect = pygame.Rect(30 * radius, 0, info_board_width, radius)
    WIN.blit(info_board, (30 * radius, 0))
    pygame.draw.rect(WIN, non_colors['BLACK'], upper_rect)

    xo, yo = (30 * radius, radius)
    msg_font = pygame.font.SysFont('Comic Sans MS', 40)
    # score
    draw_info_text(non_colors['BLACK'], msg_font, 'Score:', (xo, yo), info_board_width, 4)
    draw_info_text(colors['RED'], msg_font, str(score), (xo, yo), info_board_width, 7)
    # elapsed time
    draw_info_text(non_colors['BLACK'], msg_font, 'Time:', (xo, yo), info_board_width, 12)
    mins, secs = elapsed_time // 60, elapsed_time % 60
    draw_info_text(colors['RED'], msg_font, f'{mins} m {secs} s', (xo, yo), info_board_width, 15)
    # next ball
    draw_info_text(non_colors['BLACK'], msg_font, 'Next:', (xo, yo), info_board_width, 20)
    dummy_ball = Bubble(next_ball.color, (0, 0))
    dummy_ball.pos = (xo + info_board_width / 2, yo + radius * 23)
    dummy_ball.draw()

def draw_arrow():
    global shooter_ball
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] == shooter_ball.pos[0]:
        headx = shooter_ball.pos[0]
        heady = shooter_ball.pos[1] - 3 * radius
    else:
        xc, yc = mouse_pos
        xb, yb = shooter_ball.pos
        m = (yc - yb) / (xc - xb)
        heady = -sqrt(((3 * radius * m) ** 2) / (m**2 + 1)) + yb
        if xc < xb:
            headx = -sqrt(9 * (radius ** 2) - ((3 * radius * m) ** 2) / (m**2 + 1)) + xb
        else:
            headx = sqrt(9 * (radius ** 2) - ((3 * radius * m) ** 2) / (m**2 + 1)) + xb
    if heady > shooter_ball.pos[1] - radius:
        heady = shooter_ball.pos[1] - radius
    pygame.draw.line(WIN, non_colors['BLACK'], (shooter_ball.pos), (headx, heady), width = 2)

def draw_window(stage, shooting):
    global board, counter, elapsed_time
    if stage == 'Start':
        # fade counter
        counter += 15
        if counter == 255:
            counter = -255
        logo = pygame.image.load('Resources/logo.png').convert_alpha()
        logo_rect = logo.get_rect(center=(WIDTH/2, HEIGHT/2))
        msg_font = pygame.font.SysFont('Comic Sans MS', 40)
        text = msg_font.render('Click anywhere to start', True, colors['RED'])
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT*6/8))
        if counter < 0:
            text.set_alpha(counter + 255)
        else:
            text.set_alpha(255 - counter)
        WIN.blit(background, (0, 0))
        WIN.blit(logo, logo_rect)
        WIN.blit(text, text_rect)
    elif stage == 'InGame':
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        WIN.blit(background, (0, 0))
        draw_board()
        draw_info()
        # draw the grid
        for level in grid:
            for ball in level:
                ball.draw()
        # draw shooter ball
        if not shooting:
            draw_arrow()
        shooter_ball.draw()
    pygame.display.update()

def main():
    global stage, counter, shooter_ball, next_ball
    stage = 'Start'
    counter = -255
    run = True
    shooting = False
    while run:
        clock.tick(FPS)
        if shooting == True:
            new_pos = (shooter_ball.pos[0], shooter_ball.pos[1] - radius)
            shooter_ball.pos = new_pos
            if shooter_ball.pos[1] <= 0:
                shooting = False
                shooter_ball = deepcopy(next_ball)
                next_ball = Bubble(random_color(), default_pos)
        for event in pygame.event.get():
            # clicked to start
            if stage == 'Start' and event.type == pygame.MOUSEBUTTONUP:
                init_grid('level-1', (WIDTH/20, HEIGHT/20))
                stage = 'InGame'
            if stage == 'InGame' and event.type == pygame.MOUSEBUTTONDOWN:
                shooting = True
            if event.type == pygame.QUIT:
                run = False
        draw_window(stage, shooting)
    pygame.quit()

if __name__ == "__main__":
    # game settings
    pygame.init()
    clock = pygame.time.Clock()
    Bubble.surface = WIN
    icon = pygame.image.load('Resources/logo.png').convert()
    pygame.display.set_icon(icon)
    # background
    background = pygame.image.load('Resources/background.jpg').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    # main function
    main()