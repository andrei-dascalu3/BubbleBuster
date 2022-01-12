import random
'''
Dictionaries of colors used in drawing operations.
'''
colors = {
        'RED': (255, 0, 0), \
        'GREEN': (0, 255, 0), \
        'BLUE': (0, 0, 255), \
        'YELLOW': (255, 255, 0), \
        'CYAN': (0, 255, 255), \
        'MAGENTA': (255, 0, 255)
        }

non_colors = {
        'WHITE': (255, 255, 255),
        'BLACK': (0, 0, 0),
        'LIGHT_GRAY': (200, 200, 200),
        'DARK_GRAY': (100, 100, 100)
        }

def random_color():
   '''
   Returns a random color from the custom dictionary.

   Parameters:
        None

   Returns:
        tuple: Color chosen
   '''
   return random.choice(list(colors.values()))