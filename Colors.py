import random
colors = {
        'RED': (255, 0, 0), \
        'GREEN': (0, 255, 0), \
        'BLUE': (0, 0, 255), \
        'YELLOW': (255, 255, 0), \
        'CYAN': (0, 255, 255), \
        'MAGENTA': (255, 0, 255)
        }
        
def random_color():
    return random.choice(list(colors.values()))