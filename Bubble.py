from pygame import draw

class Bubble:
    radius = 20
    surface = None
    draw_factor = 0.6
    def __init__(self, color, pos):
        self.pos = pos
        self.color = color
    
    def draw(self):
        darkened_color = tuple(a * b for a, b in zip(self.color, (0.8, 0.8, 0.8)))
        # outer shade
        draw.circle(self.surface, darkened_color, self.pos, self.radius - 1)
        # inner shade
        draw.circle(self.surface, self.color, self.pos, self.radius * self.draw_factor)
        shine_pos = tuple(a + b for a, b in zip(self.pos, (-self.radius * 0.5, self.radius * 0.5)))
        shine_color = tuple(a + 100 if a < 235 else 255 for a in self.color)
        # shine spot
        draw.circle(self.surface, shine_color, shine_pos, self.radius * 0.2)
