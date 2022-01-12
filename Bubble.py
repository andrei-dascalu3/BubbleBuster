from pygame import draw, mouse
from math import sqrt

class Bubble:
    '''
    A class to represent each bubble.

    Attributes:
        radius : int
            radius of the circle
        surface : Surface
            surface to be drawn onto
        draw_factor : float
            factor for color shading

    Methods:
        draw():
            Draws the bubble.
        hits(bubble):
            Checks if it hits another bubble.
        arrow_coord():
            Returns coord of arrow-head indicating direction.
        move():
            Changes position of bubble to simulate throw.
        is_near(popping=False):
            Checks if the bubble is neighbouring other bubbles.
    
    '''
    radius = 20
    surface = None
    draw_factor = 0.6
    def __init__(self, color, pos):
        """
        Constructs all the necessary attributes for the bubble object.

        Parameters:
            color : tuple
                color of bubble
            pos : tuple
                position on surface
        """
        self.pos = pos
        self.color = color
        self.is_visited = False
    
    def draw(self):
        '''
        Draws the bubble. Bubble has a main part, shaade and shine spot.

        Parameters:
            None

        Returns:
            None
        '''
        darkened_color = tuple(a * b for a, b in zip(self.color, \
                                (0.8, 0.8, 0.8)))
        # outer shade
        draw.circle(self.surface, darkened_color, self.pos, self.radius - 1)
        # inner shade
        draw.circle(self.surface, self.color, self.pos, \
                    self.radius * self.draw_factor)
        shine_pos = tuple(a + b for a, b in zip(self.pos, \
                            (-self.radius * 0.5, self.radius * 0.5)))
        shine_color = tuple(a + 100 if a < 235 else 255 for a in self.color)
        # shine spot
        draw.circle(self.surface, shine_color, shine_pos, self.radius * 0.2)
    
    def hits(self, bubble):
        '''
        Checks if it hits another bubble. Returns True if it does

        Parameters:
            bubble : Bubble

        Returns:
            bool
        '''
        dist2 = (self.pos[0] - bubble.pos[0])**2 + \
                (self.pos[1] - bubble.pos[1])**2
        rad_sum2 = (self.radius * 2)**2
        if dist2 < rad_sum2 + 4:
            return True
        return False

    def arrow_coord(self):
        '''
        Returns coord of arrow-head indicating direction, XY coordinates.

        Parameters:
            None

        Returns:
            tuple of int
        '''
        mouse_pos = mouse.get_pos()
        if mouse_pos[1] > self.pos[1] - self.radius:
            mouse_pos = (mouse_pos[0], self.pos[1] - self.radius)
        if mouse_pos[0] == self.pos[0]:
            headx = self.pos[0]
            heady = self.pos[1] - 2 * self.radius
        else:
            xc, yc = mouse_pos
            xb, yb = self.pos
            m = (yc - yb) / (xc - xb)
            heady = -sqrt(((2 * self.radius * m) ** 2) / (m**2 + 1)) + yb
            if xc < xb:
                headx = -sqrt(4 * (self.radius ** 2) - 
                        ((2 * self.radius * m) ** 2) / (m**2 + 1)) + xb
            else:
                headx = sqrt(4 * (self.radius ** 2) - 
                        ((2 * self.radius * m) ** 2) / (m**2 + 1)) + xb
        return (headx, heady)

    def move(self, speed, bounds):
        '''
        Changes position of bubble to simulate throw.

        Parameters:
            speed : int
            bounds : list of int
                left, right and upper bounds to be taken into consideration

        Returns:
            int
        '''
        new_pos = (self.pos[0] - speed[0], self.pos[1] - speed[1])
        self.pos = new_pos
        left_bound, right_bound = bounds[0], bounds[1]
        if self.pos[0] <= left_bound + self.radius or \
           self.pos[0] >= right_bound - self.radius:
            speed = (-speed[0], speed[1])
        return speed

    def is_near(self, bubble, popping=False):
        '''
        Checks if the bubble is neighbouring other bubbles.

        Parameters:
            bubble : Bubble
            popping : bool, optional
                used when color is also taken into consideration

        Returns:
            int
        '''
        # on same level
        if (self.pos[0] + 2 * self.radius == bubble.pos[0] or \
           self.pos[0] - 2 * self.radius == bubble.pos[0]) and \
           self.pos[1] == bubble.pos[1]:
            if popping:
                return self.color == bubble.color
            return True
        # upper level
        if (self.pos[0] + self.radius == bubble.pos[0] or \
           self.pos[0] - self.radius == bubble.pos[0]) and \
           self.pos[1] + 2 * self.radius == bubble.pos[1]:
            if popping:
                return self.color == bubble.color
            return True
        # lower level
        if (self.pos[0] + self.radius == bubble.pos[0] or \
           self.pos[0] - self.radius == bubble.pos[0]) and \
           self.pos[1] - 2 * self.radius == bubble.pos[1]:
            if popping:
                return self.color == bubble.color
            return True
        return False