from pygame import draw

class Bubble:
    radius = 20
    surface = None
    def __init__(self, color, pos):
        self.pos = pos
        self.color = color
    
    def draw(self):
        draw.circle(self.surface, self.color, self.pos, self.radius - 1)
