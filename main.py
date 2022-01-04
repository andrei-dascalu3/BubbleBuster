import pygame
from Bubble import Bubble
import Colors

WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Buster")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

grid = []
def init_grid():
    counter = 0
    for y in range(20, HEIGHT - 40, 35):
        counter += 1
        line = []
        if counter % 2 == 1:
            for x in range(20, WIDTH - 40, 40):
                line.append(Bubble(Colors.random_color(), (x, y)))
        else:
            for x in range(40, WIDTH - 60, 40):
                line.append(Bubble(Colors.random_color(), (x, y)))
        grid.append(line)

def draw_window():
    WIN.fill(BLACK)
    for l in grid:
        for b in l:
            b.draw()
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    Bubble.surface = WIN
    init_grid()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()