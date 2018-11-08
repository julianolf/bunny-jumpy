# general
TITLE = 'Jumpy!'
FONT_NAME = 'arial'
SCORE_FILE = '.highestscore'

# screen and sprites
FPS = 60
WIDTH = 480
HEIGHT = 640
TILE_SIZE = 32

# player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_STRENGTH = -15
GRAVITY = 0.5

# initial platforms [(size, position),]
PLATFORM_SIZE = (WIDTH//3, TILE_SIZE)
PLATFORM_SIZE_SMALL = (WIDTH//5, TILE_SIZE)
PLATFORM_LIST = [
    {
        'size': (WIDTH, TILE_SIZE),
        'pos': (0, HEIGHT-TILE_SIZE)
    },
    {
        'size': PLATFORM_SIZE,
        'pos': (WIDTH-(PLATFORM_SIZE[0]*2), HEIGHT*3/4)
    },
    {
        'size': PLATFORM_SIZE,
        'pos': (WIDTH-(PLATFORM_SIZE[0]*3), HEIGHT*2/4)
    },
    {
        'size': PLATFORM_SIZE_SMALL,
        'pos': (0, HEIGHT/4)
    },
    {
        'size': PLATFORM_SIZE_SMALL,
        'pos': (WIDTH-PLATFORM_SIZE_SMALL[0], HEIGHT/4)
    }
]

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
