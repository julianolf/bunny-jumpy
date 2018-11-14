# general
TITLE = 'Bunny Jumpy'
FONT_NAME = 'arial'

# screen and sprites
FPS = 60
WIDTH = 480
HEIGHT = 640
TILE_SIZE = 32

# external files
SCORE_FILE = '.highestscore'
SPRITESHEET = 'spritesheet.png'
SND_INTRO = 'yippee.wav'
SND_MAIN = 'happytune.mp3'
SND_JUMP = 'jump.wav'
SND_POW = 'powerup.wav'
SND_DEATH = 'death.wav'

# player properties
PLAYER_INI_POS = (50, HEIGHT * 3 / 4)
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_STRENGTH = -20
GRAVITY = 0.8

# enemy properties
MOB_FREQ = 5000

# items properties
BOOST_POWER = -60
POW_SPAWN_PCT = 7

# initial platforms
PLATFORM_LIST = [
    (5, HEIGHT - 60),
    (WIDTH / 2 - 50, HEIGHT * 3 / 4),
    (125, HEIGHT - 350),
    (280, 200),
    (175, 100)
]

# initial clouds
CLOUD_LIST = [
    (15, 15), (WIDTH * 3 / 4, 50), (WIDTH / 2, HEIGHT / 2),
    (50, HEIGHT * 2 / 3), (WIDTH * 3 / 4, HEIGHT * 2 / 3 + 20)
]

# layers
PLAYER_LAYER = 2
ENEMIES_LAYER = 2
PLATFORM_LAYER = 1
POWERUP_LAYER = 1
CLOUD_LAYER = 0

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTBLUE = (0, 190, 240)
BGCOLOR = LIGHTBLUE
