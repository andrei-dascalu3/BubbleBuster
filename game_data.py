from Bubble import Bubble
import pygame
from bubble_colors import random_color

# game settings
WIDTH, HEIGHT = 800, 760
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Buster")
FPS = 60
grid = []
radius = Bubble.radius
board_width = 27 * radius
# game data
score = 0
start_time = 0
elapsed_time = 0
default_pos = (15 * radius, 36 * radius)
next_ball = Bubble(random_color(), default_pos)