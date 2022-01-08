import pygame
from Bubble import Bubble
import Colors

WIDTH, HEIGHT = 800, 760
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Buster")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

grid = []
def init_grid():
    counter = 0
    for y in range(40, HEIGHT - 40 - 3 * 40, 35):
        counter += 1
        line = []
        if counter % 2 == 1:
            for x in range(20 + 3 * 40, WIDTH - 3 * 40, 40):
                line.append(Bubble(Colors.random_color(), (x, y)))
        else:
            for x in range(40  + 3 * 40, WIDTH - 3 * 40, 40):
                line.append(Bubble(Colors.random_color(), (x, y)))
        grid.append(line)

def draw_window():
    WIN.blit(background, (0, 0))
    border = pygame.Rect(120, 20, WIDTH - 240, HEIGHT - 20)
    pygame.draw.rect(WIN, (200, 200, 200), border)
    for l in grid:
        for b in l:
            b.draw()
    pygame.display.update()

def main():
    pygame.init()
    stage = 'Start'
    clock = pygame.time.Clock()
    run = True
    Bubble.surface = WIN
    global background
    background = pygame.image.load('Resources/background.jpg').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    counter = -255
    while run:
        counter += 15
        if counter == 255:
            counter = -255
        clock.tick(FPS)
        for event in pygame.event.get():
            # clicked to start
            if stage == 'Start' and event.type == pygame.MOUSEBUTTONUP:
                init_grid()
                stage = 'InGame'
            if event.type == pygame.QUIT:
                run = False
        if stage == 'Start':
            msg_font = pygame.font.SysFont('Comic Sans MS', 40)
            text = msg_font.render('Click anywhere to start', True, Colors.colors['RED'])
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            if counter < 0:
                text.set_alpha(counter + 255)
            else:
                text.set_alpha(255 - counter)
            WIN.blit(background, (0, 0))
            WIN.blit(text, text_rect)
            pygame.display.update()
        elif stage == 'InGame':
            draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()