from os import remove
import pygame
from pygame import time
from pygame.image import load
from Bubble import Bubble
from bubble_colors import *
from math import sqrt
from copy import deepcopy
from gamedata import *

# the grid of bubbles
grid = []

def init_grid(seed, origin):
    global shooter_ball, grid
    grid = []
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
    upper_rect = pygame.Rect(WIDTH/20 - radius, HEIGHT/20 - radius * 2, \
        board_width, radius)
    WIN.blit(board, (WIDTH/20 - radius, HEIGHT/20 - radius))
    pygame.draw.rect(WIN, non_colors['BLACK'], upper_rect)

def draw_info_text(color, msg_font, msg, origin, width, lines):
    text = msg_font.render(msg, True, color)
    text_rect = text.get_rect(center=(origin[0] + width / 2, origin[1] + radius\
         * lines))
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
    draw_info_text(non_colors['BLACK'], msg_font, 'Score:', (xo, yo),\
                    info_board_width, 4)
    draw_info_text(colors['RED'], msg_font, str(score), (xo, yo),\
                    info_board_width, 7)
    # elapsed time
    draw_info_text(non_colors['BLACK'], msg_font, 'Time:', (xo, yo),\
                    info_board_width, 12)
    mins, secs = elapsed_time // 60, elapsed_time % 60
    msg_font = pygame.font.SysFont('Comic Sans MS', 30)
    draw_info_text(colors['RED'], msg_font, f'{mins} m {secs} s', (xo, yo),\
                    info_board_width, 15)
    # next ball
    msg_font = pygame.font.SysFont('Comic Sans MS', 40)
    draw_info_text(non_colors['BLACK'], msg_font, 'Next:', (xo, yo), \
        info_board_width, 20)
    dummy_ball = Bubble(next_ball.color, (0, 0))
    dummy_ball.pos = (xo + info_board_width / 2, yo + radius * 23)
    dummy_ball.draw()

def draw_grid():
    for level in grid:
        for ball in level:
            ball.draw()

def draw_arrow():
    pygame.draw.line(WIN, non_colors['BLACK'], (shooter_ball.pos),\
                     shooter_ball.arrow_coord(), width = 2)

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
        draw_grid()
        # draw shooter ball
        if not shooting:
            draw_arrow()
        shooter_ball.draw()
    elif stage == 'GameWon':
        # fade counter
        counter += 15
        if counter == 255:
            counter = -255
        msg_font = pygame.font.SysFont('Comic Sans MS', 60)
        won = msg_font.render('You won!', True, colors['GREEN'])
        won_rect = won.get_rect(center=(WIDTH/2, HEIGHT/2))
        msg_font = pygame.font.SysFont('Comic Sans MS', 40)
        text = msg_font.render('Click anywhere to start', True, colors['RED'])
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT*6/8))
        if counter < 0:
            text.set_alpha(counter + 255)
        else:
            text.set_alpha(255 - counter)
        WIN.blit(background, (0, 0))
        WIN.blit(won, won_rect)
        WIN.blit(text, text_rect)
    elif stage == 'GameLost':
        # fade counter
        counter += 15
        if counter == 255:
            counter = -255
        msg_font = pygame.font.SysFont('Comic Sans MS', 60)
        won = msg_font.render('You lost!', True, colors['RED'])
        won_rect = won.get_rect(center=(WIDTH/2, HEIGHT/2))
        msg_font = pygame.font.SysFont('Comic Sans MS', 40)
        text = msg_font.render('Click anywhere to restart', True, colors['RED'])
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT*6/8))
        if counter < 0:
            text.set_alpha(counter + 255)
        else:
            text.set_alpha(255 - counter)
        WIN.blit(background, (0, 0))
        WIN.blit(won, won_rect)
        WIN.blit(text, text_rect)
    pygame.display.update()

def already_occupied(bubble, bubble_line):
    for b in bubble_line:
        if bubble.pos == b.pos:
            return True
    return False

def check_hit():
    global board_bounds
    grid_height = len(grid)
    for i in range(grid_height - 1, -1, -1):
        for bubble in grid[i]:
            if shooter_ball.hits(bubble):
                if i == grid_height - 1:
                    grid.append([])
                new_bubble = deepcopy(shooter_ball)
                if shooter_ball.pos[0] > bubble.pos[0]:
                    if bubble.pos[0] == board_bounds[1] - radius:
                        new_bubble.pos = (bubble.pos[0] - radius,
                                          bubble.pos[1] + 2 * radius)
                    else:
                        new_bubble.pos = (bubble.pos[0] + radius,
                                          bubble.pos[1] + 2 * radius)
                    if already_occupied(new_bubble, grid[i + 1]):
                        new_bubble.pos = (bubble.pos[0] + 2* radius,
                                          bubble.pos[1])
                else:
                    if bubble.pos[0] == board_bounds[0] + radius:
                        new_bubble.pos = (bubble.pos[0] + radius,
                                          bubble.pos[1] + 2 * radius)
                    else:
                        new_bubble.pos = (bubble.pos[0] - radius,
                                          bubble.pos[1] + 2 * radius)
                    if already_occupied(new_bubble, grid[i + 1]):
                        new_bubble.pos = (bubble.pos[0] - 2* radius,
                                          bubble.pos[1])
                grid[i + 1].append(new_bubble)
                return new_bubble
    return None

def remove_isolated(grid):
    if len(grid) == 1:
        return None
    for i in range(1, len(grid)):
        for current in grid[i]:
            safe = False
            for b in grid[i - 1]:
                if current.is_near(b):
                    safe = True
                    break
            if not safe:
                grid[i].remove(current)
        if grid[i] == []:
            grid.remove([])

def pop_bubbles(grid, start_bubble):
    global score
    queue = []
    row, col = None, None
    grid_height = len(grid)
    for i in range(grid_height):
        line_length = len(grid[i])
        for j in range(line_length):
            grid[i][j].is_visited = False
            if grid[i][j] == start_bubble:
                row, col = i, j
    counter = 0
    queue.append(grid[row][col])
    while queue != []:
        current = queue.pop(0)
        for line in grid:
            for bubble in line:
                if current.is_near(bubble, popping=True) and not bubble.is_visited:
                    bubble.is_visited = True
                    counter += 1
                    queue.append(bubble)
    if counter >= 3:
        for line in grid:
            for b in line:
                if b.is_visited:
                    score += 10
                    line.remove(b)
            if line == []:
                grid.remove(line)
    remove_isolated(grid)
    print(len(grid))

def main():
    global stage, counter, shooter_ball, next_ball, start_time, speed, level
    global score
    goals = [400, 600, 800, 1000]
    time_limits = [60, 90, 120, 150]
    stage = 'Start'
    level = 0
    counter = -255
    run = True
    shooting = False
    while run:
        clock.tick(FPS)
        if stage == 'InGame':
            if stage == 'InGame' and \
               score >= goals[level] and \
               elapsed_time < time_limits[level]:
                stage = 'GameWon'
                level += 1
            if stage == 'InGame' and \
               len(grid) >= 17:
                stage = 'GameLost'
            if shooting == True:
                speed = shooter_ball.move(speed, board_bounds)
                sticked_bubble = check_hit()
                if shooter_ball.pos[1] <= board_bounds[2] + radius or \
                sticked_bubble is not None:
                    # if it reaches level 0
                    if sticked_bubble == None:
                        x = (shooter_ball.pos[0] - board_bounds[0])// (radius * 2) \
                            * (radius * 2) + radius + board_bounds[0]
                        y = board_bounds[2] + radius
                        sticked_bubble = Bubble(shooter_ball.color, (x, y))
                        grid[0].append(sticked_bubble)
                    shooting = False
                    pop_bubbles(grid, sticked_bubble)
                    shooter_ball = deepcopy(next_ball)
                    next_ball = Bubble(random_color(), default_pos)
        for event in pygame.event.get():
            # clicked to start
            if stage == 'Start' and event.type == pygame.MOUSEBUTTONUP:
                init_grid('level-' + str(level), (WIDTH/20, HEIGHT/20))
                stage = 'InGame'
                start_time = pygame.time.get_ticks()
            if stage == 'InGame' and event.type == pygame.MOUSEBUTTONDOWN and \
                not shooting:
                shooting = True
                (headx, heady) = shooter_ball.arrow_coord()
                distx = shooter_ball.pos[0] - headx
                disty = shooter_ball.pos[1] - heady
                speed = (distx, disty)
            if stage == 'GameWon' and event.type == pygame.MOUSEBUTTONDOWN:
                init_grid('level-' + str(level), (WIDTH/20, HEIGHT/20))
                stage = 'InGame'
                start_time = pygame.time.get_ticks()
                score = 0
            if stage == 'GameLost' and event.type == pygame.MOUSEBUTTONDOWN:
                init_grid('level-' + str(level), (WIDTH/20, HEIGHT/20))
                stage = 'InGame'
                start_time = pygame.time.get_ticks()
                score = 0
            if event.type == pygame.QUIT:
                run = False
        draw_window(stage, shooting)
    pygame.quit()

if __name__ == "__main__":
    # game settings
    pygame.init()
    icon = pygame.image.load('Resources/logo.png').convert()
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    Bubble.surface = WIN
    # background
    background = pygame.image.load('Resources/background.jpg').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    # main function
    main()