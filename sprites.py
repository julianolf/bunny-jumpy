import pygame
import random
import settings
from pygame.math import Vector2


class Spritesheet(object):
    def __init__(self, filename):
        super(Spritesheet, self).__init__()
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width//2, height//2))
        image.set_colorkey(settings.BLACK)
        return image


class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.sprites,
        super(Player, self).__init__(self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.boosted = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (50, settings.HEIGHT * 3 / 4)
        self.pos = Vector2(50, settings.HEIGHT * 3 / 4)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.score = 0

    def load_images(self):
        self.standing_frames = [
            self.game.spritesheet.get_image(*t)
            for t in ((614, 1063, 120, 191), (690, 406, 120, 201))
        ]
        self.walk_frames_r = [
            self.game.spritesheet.get_image(*t)
            for t in ((678, 860, 120, 201), (692, 1458, 120, 207))
        ]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(
                pygame.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)

    def standing(self):
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(
                self, self.game.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if (self.pos.x < lowest.rect.right + 10
                        and self.pos.x > lowest.rect.left - 10):
                    if self.pos.y < lowest.rect.centery:
                        self.pos.y = lowest.rect.top
                        self.vel.y = 0
                        self.jumping = False
                        self.boosted = False

    def walk(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.acc.x = -settings.PLAYER_ACC
        if key[pygame.K_RIGHT]:
            self.acc.x = settings.PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * settings.PLAYER_FRICTION

        # motion equation
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + settings.PLAYER_ACC * self.acc

        # wrap around the sides of the screen
        if self.pos.x > settings.WIDTH + (self.rect.width / 2):
            self.pos.x = 0 - (self.rect.width / 2)
        if self.pos.x < 0 - (self.rect.width / 2):
            self.pos.x = settings.WIDTH + (self.rect.width / 2)

        # update walking status according to the x speed
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = settings.PLAYER_STRENGTH
            self.game.jump_sound.play()

    def cut_jump(self):
        if self.jumping and not self.boosted:
            if self.vel.y < -6:
                self.vel.y = -6

    def hit_powerup(self):
        for hit in pygame.sprite.spritecollide(self, self.game.powerups, True):
            if hit.type == 'boost':
                self.boosted = True
                self.vel.y = settings.BOOST_POWER
                self.game.powerup_sound.play()

    def animate(self):
        now = pygame.time.get_ticks()

        if self.jumping or self.boosted:
            if now - self.last_update > 100:
                self.last_update = now
                bottom = self.rect.bottom
                self.image = self.jump_frame
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    (self.current_frame + 1) % len(self.walk_frames_l))
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                elif self.vel.x < 0:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (
                    (self.current_frame + 1) % len(self.standing_frames))
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def update(self):
        # reset acceleration and gravity values
        self.acc = Vector2(0, settings.GRAVITY)

        # test if the player collided with any platform
        self.standing()

        # move left or right according to players command
        self.walk()

        # check for poweups
        self.hit_powerup()

        # animate player sprite
        self.animate()

        # update player position
        self.rect.midbottom = self.pos

        # when player gets close to the top initiate the view scrolling
        if self.rect.top <= settings.HEIGHT / 4:
            self.game.scroll(max(abs(self.vel.y), 2))

        # if the player falls the game is over
        if self.rect.bottom > settings.HEIGHT:
            self.game.over()


class Platform(pygame.sprite.Sprite):

    def __init__(self, game, pos=None):
        self.groups = game.sprites, game.platforms
        super(Platform, self).__init__(self.groups)
        self.game = game
        image_info = random.choice([(0, 288, 380, 94), (213, 1662, 201, 100)])
        self.image = self.game.spritesheet.get_image(*image_info)
        self.rect = self.image.get_rect()
        if not pos:
            pos = (
                random.randrange(0, settings.WIDTH - self.rect.width),
                random.randrange(-64, -32)
            )
        self.rect.x, self.rect.y = pos
        if random.randrange(100) < settings.POW_SPAWN_PCT:
            Pow(self.game, self)


class Pow(pygame.sprite.Sprite):

    def __init__(self, game, platform):
        self.groups = game.sprites, game.powerups
        super(Pow, self).__init__(self.groups)
        self.game = game
        self.platform = platform
        self.type = random.choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5

    def update(self):
        self.rect.bottom = self.platform.rect.top - 5
        if not self.game.platforms.has(self.platform):
            self.kill()
