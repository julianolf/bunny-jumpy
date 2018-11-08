import pygame
import settings
from sprites import Player, Platform


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

    def new(self):
        self.sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.sprites.add(self.player)
        self.build_platform(settings.PLATFORM_LIST)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(settings.FPS)
            self.events()
            self.update()
            self.draw()

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

    def update(self):
        self.sprites.update()

        if len(self.platforms) < len(settings.PLATFORM_LIST):
            missing = len(settings.PLATFORM_LIST) - len(self.platforms)
            self.build_platform(amount=missing)

    def draw(self):
        self.screen.fill(settings.BLACK)
        self.sprites.draw(self.screen)
        self.draw_text(
            str(self.player.score), 22, settings.WHITE,
            (settings.WIDTH / 2, 15))
        pygame.display.flip()

    def draw_text(self, text, size, color, pos):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = pos
        self.screen.blit(text_surface, text_rect)

    def build_platform(self, specs=None, amount=0):
        platforms = []
        if specs:
            if type(specs) == list:
                for spec in specs:
                    platforms.append(Platform(**spec))
            elif type(specs) == dict:
                platforms.append(Platform(**specs))
        else:
            if amount:
                for _ in range(amount):
                    platforms.append(Platform.random())
            else:
                platforms.append(Platform.random())
        for plat in platforms:
            self.platforms.add(plat)
            self.sprites.add(plat)

    def scroll(self, amount):
        self.player.pos.y += amount
        for plat in self.platforms:
            plat.rect.y += amount
            if plat.rect.top >= settings.HEIGHT:
                plat.kill()
                self.player.score += 10

    def start(self):
        pass

    def over(self):
        for sprite in self.sprites:
            sprite.rect.y -= max(self.player.vel.y, 10)
            if sprite.rect.bottom < 0:
                sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
