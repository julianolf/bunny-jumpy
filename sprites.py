import pygame
import random
import settings
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game
        self.image = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (settings.WIDTH / 2, settings.HEIGHT / 2)
        self.pos = Vector2(settings.WIDTH / 2, settings.HEIGHT / 2)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.score = 0

    def standing(self):
        if self.vel.y > 0:
            for hit in pygame.sprite.spritecollide(
                    self, self.game.platforms, False):
                self.pos.y = hit.rect.top
                self.vel.y = 0
                break

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
        self.pos += self.vel + settings.PLAYER_ACC * self.acc

        # wrap around the sides of the screen
        if self.pos.x > settings.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = settings.WIDTH

    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = settings.PLAYER_STRENGTH

    def update(self):
        # reset acceleration and gravity values
        self.acc = Vector2(0, settings.GRAVITY)

        # test if the player collided with any platform
        self.standing()

        # move left or right according to players command
        self.walk()

        # update player position
        self.rect.midbottom = self.pos

        # when player gets close to the top initiate the view scrolling
        if self.rect.top <= settings.HEIGHT / 4:
            self.game.scroll(abs(self.vel.y))

        # if the player falls the game is over
        if self.rect.bottom > settings.HEIGHT:
            self.game.over()


class Platform(pygame.sprite.Sprite):

    def __init__(self, size=(0, 0), pos=(0, 0)):
        super(Platform, self).__init__()
        self.image = pygame.Surface(size)
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    @classmethod
    def random(cls):
        size = (
            random.randrange(
                settings.TILE_SIZE * 4,
                settings.WIDTH - (settings.TILE_SIZE * 6),
                settings.TILE_SIZE
            ),
            settings.TILE_SIZE
        )
        pos = (
            random.randrange(0, settings.WIDTH - size[0], settings.TILE_SIZE),
            random.randrange(
                -(settings.TILE_SIZE * 2),
                -settings.TILE_SIZE
            )
        )
        return cls(size=size, pos=pos)
