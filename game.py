import pygame
import pygame.freetype
import random
import settings
from sprite.living import Player, FlyMan
from sprite.inanimate import Platform, Cloud
from sprite.items import Jetpack
from sprite.spritesheet import Spritesheet
from os import path


class Game(object):
    """Game dynamic and rules."""

    def __init__(self):
        super(Game, self).__init__()
        # pygame initialization
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        # define basic counters, controllers and sprite groups
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # load external data
        self.load_data()

    def new(self):
        """(Re)Start the game."""
        self.new_highscore = 0
        self.enemies_timer = 0
        self.stage = 1
        self.sprites.empty()
        self.platforms.empty()
        self.clouds.empty()
        self.powerups.empty()
        self.enemies.empty()
        self.player = Player.new(
            self,
            pos=settings.PLAYER_INI_POS,
            groups=[self.sprites]
        )
        for pos in settings.PLATFORM_LIST:
            self.build_platform(pos)
        for pos in settings.CLOUD_LIST:
            self.build_cloud(pos)
        pygame.mixer.music.load(path.join(self._snd_path, settings.SND_MAIN))
        pygame.mixer.music.set_volume(1.)
        self.run()

    def run(self):
        """Stage loop."""
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(settings.FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

    def events(self):
        """Event handler.
        Decide which action perform based on window and keyboard events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.cut_jump()

    def update(self):
        """Update screen.
        Move sprites and/or create new when necessary."""

        # call the update method of all sprites
        self.sprites.update()

        # maybe spawn a new enemy
        self.spawn_enemies()

    def draw(self):
        """Put everything on screen."""
        self.screen.fill(settings.BGCOLOR)
        self.sprites.draw(self.screen)
        score = {
            'text': f'Score: {self.player.score}',
            'size': 18,
            'color': settings.WHITE,
            'pos': (settings.WIDTH / 2, 15)
        }
        self.draw_text(**score)
        pygame.display.flip()

    def draw_text(self, text, size, color, pos):
        """Draw text on screen."""
        font = pygame.freetype.SysFont(settings.FONT_NAME, size)
        text_surface, text_rect = font.render(text, pygame.Color(*color))
        text_rect.midtop = pos
        self.screen.blit(text_surface, text_rect)

    def update_scenario(self):
        """Create new platforms and add clouds."""
        missing = len(settings.PLATFORM_LIST) - len(self.platforms)
        if missing > 0:
            for _ in range(missing):
                self.build_platform()

        if random.randrange(100) < 5:
            self.build_cloud()

    def spawn_enemies(self):
        """Spawn a new enemy every ~5sec."""
        now = pygame.time.get_ticks()
        elapsed = now - self.enemies_timer
        variation = random.choice([-1000, -500, 0, 500, 1000])
        frequency = settings.MOB_FREQ + variation
        if elapsed > frequency:
            self.enemies_timer = now
            pos = (
                random.choice([-100, settings.WIDTH + 100]),
                random.randrange(settings.HEIGHT / 2)
            )
            groups = [self.sprites, self.enemies]
            FlyMan.new(self, pos=pos, groups=groups)

    def build_platform(self, pos=None):
        """Build a new platform with a chance of having a powerup."""
        if not pos:
            pos = (random.randrange(0, settings.WIDTH - 380),
                   random.randrange(-64, -32))

        plat_groups = [self.sprites, self.platforms]
        plat = Platform.new(self, pos=pos, groups=plat_groups)
        if random.randrange(100) < settings.POW_SPAWN_PCT:
            powr_groups = [self.sprites, self.powerups]
            Jetpack.new(
                self,
                platform=plat,
                groups=powr_groups
            )

    def build_cloud(self, pos=None):
        """Build a new cloud."""
        if not pos:
            pos = (random.randrange(settings.WIDTH - 260),
                   random.randrange(-500, -50))

        groups = [self.sprites, self.clouds]
        Cloud.new(self, pos=pos, groups=groups)

    def scroll(self, amount):
        """Simulate window scrolling by moving everything but the player down.
        Also adding new platforms and clouds if necessary."""
        self.update_scenario()

        for cloud in self.clouds:
            cloud.rect.y += max(amount // 2, 2)
        for enemy in self.enemies:
            enemy.rect.y += amount
        for platform in self.platforms:
            platform.rect.y += amount
            if platform.rect.top >= settings.HEIGHT:
                self.player.score += 1

    def over(self):
        """End the game.

        Move platforms up till they get off the screen and be destroyed.
        Verify is the highscore was beaten and go to the game over screen."""
        for sprite in self.sprites:
            sprite.rect.y -= max(self.player.vel.y, 10)
            if sprite.rect.bottom < 0:
                sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
            if self.player.score > self.highscore:
                self.new_highscore = self.player.score
                self.highscore = self.new_highscore
                self.save_highscore()
            self.over_screen()

    def splash_screen(self):
        """Show splash screen."""
        self.screen.fill(settings.BGCOLOR)
        text = [
            {
                'text': f'High score: {self.highscore}',
                'size': 16,
                'color': settings.WHITE,
                'pos': (settings.WIDTH / 2, 15)
            },
            {
                'text': settings.TITLE,
                'size': 50,
                'color': settings.WHITE,
                'pos': (settings.WIDTH / 2, settings.HEIGHT / 4)
            },
            {
                'text': '←   → move',
                'size': 16,
                'color': settings.WHITE,
                'pos': (settings.WIDTH / 2, settings.HEIGHT / 2)
            },
            {
                'text': '[space] jump',
                'size': 16,
                'color': settings.WHITE,
                'pos': (settings.WIDTH / 2, settings.HEIGHT / 2 + 40)
            },
            {
                'text': 'Press any key to start',
                'size': 16,
                'color': settings.WHITE,
                'pos': (settings.WIDTH / 2, settings.HEIGHT * 3 / 4)
            }
        ]
        for txt in text:
            self.draw_text(**txt)
        pygame.display.flip()
        pygame.mixer.music.load(path.join(self._snd_path, settings.SND_INTRO))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

    def over_screen(self):
        """Show game over screen."""
        self.screen.fill(settings.BGCOLOR)
        text = [
            {
                'text': 'GAME OVER',
                'size': 50,
                'color': settings.WHITE,
                'pos': (settings.WIDTH / 2, settings.HEIGHT / 4)
            },
            {
                'text': f'Score: {self.player.score}',
                'size': 16,
                'color': settings.WHITE,
                'pos': (settings.WIDTH / 2, settings.HEIGHT / 2)
            },
            {
                'text': 'Press any key to start again',
                'size': 16,
                'color': settings.WHITE,
                'pos': (settings.WIDTH / 2, settings.HEIGHT * 3 / 4)
            }
        ]
        if self.new_highscore:
            msg = 'NEW HIGH SCORE!'
        else:
            msg = f'High score: {self.highscore}'
        text.append({
            'text': msg,
            'size': 16,
            'color': settings.WHITE,
            'pos': (settings.WIDTH / 2, settings.HEIGHT / 2 + 40)
        })
        for txt in text:
            self.draw_text(**txt)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        """Wait for any key to be pressed or the window to be closed."""
        while True:
            self.clock.tick(settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    return

    def load_data(self):
        """Read the last highscore, image and audio files."""
        cur_dir = path.dirname(__file__)

        # load high score
        self._hs_file_path = path.join(cur_dir, settings.SCORE_FILE)
        try:
            f = open(self._hs_file_path, 'r')
            self.highscore = int(f.read())
        except Exception:
            self.highscore = 0

        # load spritesheet
        assets_path = path.join(cur_dir, 'assets')
        self.spritesheet = Spritesheet(
            path.join(assets_path, settings.SPRITESHEET))

        # load audio files
        self._snd_path = path.join(cur_dir, 'media')
        self.jump_sound = pygame.mixer.Sound(
            path.join(self._snd_path, settings.SND_JUMP))
        self.jump_sound.set_volume(0.3)
        self.powerup_sound = pygame.mixer.Sound(
            path.join(self._snd_path, settings.SND_POW))
        self.powerup_sound.set_volume(0.3)
        self.death_sound = pygame.mixer.Sound(
            path.join(self._snd_path, settings.SND_DEATH))
        self.death_sound.set_volume(0.3)

    def save_highscore(self):
        """Save highscore to an external file."""
        with open(self._hs_file_path, 'w') as f:
            f.write(str(self.highscore))
