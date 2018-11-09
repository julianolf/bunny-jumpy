import pygame
import random
import settings
from sprites import Spritesheet, Player, Platform, Mob
from os import path


class Game(object):

    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.font_name = pygame.font.match_font(settings.FONT_NAME)
        self.load_data()

    def new(self):
        self.sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.player = Player(self)
        self.build_platform(settings.PLATFORM_LIST)
        self.new_highscore = 0
        self.mob_timer = 0
        pygame.mixer.music.load(path.join(self._snd_path, 'happytune.mp3'))
        pygame.mixer.music.set_volume(1.)
        self.run()

    def run(self):
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(settings.FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

    def events(self):
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
        self.sprites.update()

        # build new platforms if necessary
        if len(self.platforms) < len(settings.PLATFORM_LIST):
            missing = len(settings.PLATFORM_LIST) - len(self.platforms)
            self.build_platform(amount=missing)

        # spawn a new mob after ~5sec
        now = pygame.time.get_ticks()
        if (now - self.mob_timer >
                (settings.MOB_FREQ + random.choice(
                    [-1000, -500, 0, 500, 1000]))):
            self.mob_timer = now
            Mob(self)

    def draw(self):
        self.screen.fill(settings.BGCOLOR)
        self.sprites.draw(self.screen)
        self.draw_text(
            f'Score: {self.player.score}', 18, settings.WHITE,
            (settings.WIDTH / 2, 15))
        pygame.display.flip()

    def draw_text(self, text, size, color, pos):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = pos
        self.screen.blit(text_surface, text_rect)

    def build_platform(self, specs=None, amount=0):
        if specs:
            if type(specs) == list:
                for spec in specs:
                    Platform(self, **spec)
            elif type(specs) == dict:
                Platform(self, **specs)
        else:
            if amount:
                for _ in range(amount):
                    Platform(self)
            else:
                Platform(self)

    def scroll(self, amount):
        self.player.pos.y += amount
        for mob in self.mobs:
            mob.rect.y += amount
            if mob.rect.top >= settings.HEIGHT:
                mob.kill()
        for plat in self.platforms:
            plat.rect.y += amount
            if plat.rect.top >= settings.HEIGHT:
                plat.kill()
                self.player.score += 1

    def over(self):
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
        self.screen.fill(settings.BGCOLOR)
        self.draw_text(
            f'High score: {self.highscore}', 16, settings.WHITE,
            (settings.WIDTH/2, 15))
        self.draw_text(
            settings.TITLE, 50, settings.WHITE,
            (settings.WIDTH/2, settings.HEIGHT/4))
        self.draw_text(
            '←   → move', 16, settings.WHITE,
            (settings.WIDTH/2, settings.HEIGHT/2))
        self.draw_text(
            '[space] jump', 16, settings.WHITE,
            (settings.WIDTH/2, settings.HEIGHT/2+40))
        self.draw_text(
            'Press any key to start', 16, settings.WHITE,
            (settings.WIDTH/2, settings.HEIGHT*3/4))
        pygame.display.flip()
        pygame.mixer.music.load(path.join(self._snd_path, 'yippee.wav'))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

    def over_screen(self):
        self.screen.fill(settings.BGCOLOR)
        self.draw_text(
            'GAME OVER', 50, settings.WHITE,
            (settings.WIDTH/2, settings.HEIGHT/4))
        self.draw_text(
            f'Score: {self.player.score}', 16, settings.WHITE,
            (settings.WIDTH/2, settings.HEIGHT/2))
        self.draw_text(
            'Press any key to start again', 16, settings.WHITE,
            (settings.WIDTH/2, settings.HEIGHT*3/4))
        if self.new_highscore:
            msg = 'NEW HIGH SCORE!'
        else:
            msg = f'High score: {self.highscore}'
        self.draw_text(
            msg, 16, settings.WHITE,
            (settings.WIDTH/2, settings.HEIGHT/2+40))
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        while True:
            self.clock.tick(settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    return

    def load_data(self):
        cur_dir = path.dirname(__file__)

        # load high score saving file
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

        # load sounds
        self._snd_path = path.join(cur_dir, 'media')
        self.jump_sound = pygame.mixer.Sound(
            path.join(self._snd_path, 'jump.wav'))
        self.jump_sound.set_volume(0.3)
        self.powerup_sound = pygame.mixer.Sound(
            path.join(self._snd_path, 'powerup.wav'))
        self.powerup_sound.set_volume(0.3)
        self.death_sound = pygame.mixer.Sound(
            path.join(self._snd_path, 'death.wav'))
        self.death_sound.set_volume(0.3)

    def save_highscore(self):
        with open(self._hs_file_path, 'w') as f:
            f.write(str(self.highscore))
