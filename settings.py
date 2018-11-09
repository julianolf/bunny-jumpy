# general
TITLE = 'Jumpy!'
FONT_NAME = 'arial'
SCORE_FILE = '.highestscore'
SPRITESHEET = 'spritesheet.png'

# screen and sprites
FPS = 60
WIDTH = 480
HEIGHT = 640
TILE_SIZE = 32

# player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_STRENGTH = -20
GRAVITY = 0.8

# game properties
BOOST_POWER = -60
POW_SPAWN_PCT = 7

# initial platforms
PLATFORM_LIST = [
    {'pos': (5, HEIGHT - 60)},
    {'pos': (WIDTH / 2 - 50, HEIGHT * 3 / 4)},
    {'pos': (125, HEIGHT - 350)},
    {'pos': (280, 200)},
    {'pos': (175, 100)}
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
