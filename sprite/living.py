import pygame
import settings
import random
from pygame.math import Vector2
from sprite.items import Jetpack


class LivingBeing(pygame.sprite.Sprite):
    """Describes common behavior and attributes between living beings."""

    def __init__(self, image, pos, groups):
        """
        Args:
            image (pygame.Surface): Image surface loaded via pygame.image.load.
            pos (tuple): X and Y axis positions where the sprite will be draw.
            groups (list): A list of pygame.sprite.Group.
        """
        super(LivingBeing, self).__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.last_update = 0


class Player(LivingBeing):
    """
    Attributes:
        _layer (int): The layer where the player will be draw.
        image_names (list): List of Bunny image names.
    """
    _layer = settings.PLAYER_LAYER
    image_names = [
        'bunny1_stand.png', 'bunny1_ready.png', 'bunny1_jump.png',
        'bunny1_hurt.png', 'bunny1_walk1.png', 'bunny1_walk2.png'
    ]

    def __init__(self, game, images, pos=(0, 0), groups=[]):
        """
        Args:
            game (Game): A reference for the running game.
            images (list): List of image surfaces loaded via pygame.image.load.
            pos (tuple): X and Y axis positions where the Player will be draw.
            groups (list): A list of pygame.sprite.Group.
        """
        super(Player, self).__init__(images[0], pos, groups)
        self._image_frames(images)
        self.game = game
        self.walking = False
        self.jumping = False
        self.boosted = False
        self.alive = True
        self.score = 0
        self.current_frame = 0
        self.pos = Vector2(self.rect.x, self.rect.y)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def _image_frames(self, images):
        """Organize image frames in a dictionary.

        Args:
            images (list): List of image surfaces loaded via pygame.image.load.
        """
        self.image_frames = {
            'jump': images[2],
            'hurt': images[3],
            'stand': images[:2],
            'walkr': images[4:],
            'walkl': []
        }

        for frame in self.image_frames['walkr']:
            self.image_frames['walkl'].append(
                pygame.transform.flip(frame, True, False))

    def standing(self):
        """Check if the player is standing over a platform."""
        if self.vel.y > 0 and self.alive:
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
        """Move the player backwards/forwards if an arrow key was pressed."""
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
        """Perform a jump."""
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = settings.PLAYER_STRENGTH
            self.game.jump_sound.play()

    def cut_jump(self):
        """Shrink the jump."""
        if self.jumping and not self.boosted:
            if self.vel.y < -6:
                self.vel.y = -6

    def hit_powerup(self):
        """Check if the player hitted a powerup."""
        if self.alive:
            for hit in pygame.sprite.spritecollide(
                    self, self.game.powerups, True):
                if isinstance(hit, Jetpack):
                    self.boosted = True
                    self.vel.y = settings.BOOST_POWER
                    self.game.powerup_sound.play()

    def hit_enemy(self):
        """Check if the player hitted a enemy."""
        if self.alive:
            for hit in pygame.sprite.spritecollide(
                    self, self.game.enemies, False,
                    pygame.sprite.collide_mask):
                self.alive = False
                self.game.death_sound.play()

    def animate(self):
        """Switch between image frames."""
        now = pygame.time.get_ticks()

        if not self.alive:
            if now - self.last_update > 100:
                self.last_update = now
                bottom = self.rect.bottom
                self.image = self.image_frames['hurt']
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        elif self.jumping or self.boosted:
            if now - self.last_update > 100:
                self.last_update = now
                bottom = self.rect.bottom
                self.image = self.image_frames['jump']
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        elif self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 2
                bottom = self.rect.bottom
                direction = 'walkr' if self.vel.x > 0 else 'walkl'
                self.image = self.image_frames[direction][self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        elif not self.jumping and not self.walking:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 2
                bottom = self.rect.bottom
                self.image = self.image_frames['stand'][self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # update sprite mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Check if the player is alive and perform
        all animations like walking, jumping, etc."""

        # reset acceleration and gravity values
        self.acc = Vector2(0, settings.GRAVITY)

        # test if the player collided with any platform
        self.standing()

        # move left or right according to players command
        self.walk()

        # check for poweups
        self.hit_powerup()

        # check if hit a mob
        self.hit_enemy()

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

    @classmethod
    def new(cls, game):
        """Create a new instance of player.

        Args:
            game (Game): A reference for the running game.
        """
        images = [game.spritesheet.get_image(i) for i in cls.image_names]
        return cls(game, images, settings.PLAYER_INI_POS, [game.sprites])


class Enemy(LivingBeing):
    """Describes common behavior and attributes between enemies.

    Attributes:
        _layer (int): The layer where the enemy will be draw.
    """
    _layer = settings.ENEMIES_LAYER

    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)


class FlyMan(Enemy):
    """A flying enemy with a propeller in the head.
    This enemy crosses the screen horizontally in a random speed.

    Attributes:
        image_names (list): List of FlyMan image names.
    """
    image_names = [
        'flyMan_fly.png', 'flyMan_jump.png',
        'flyMan_stand.png', 'flyMan_still_fly.png',
        'flyMan_still_jump.png', 'flyMan_still_stand.png'
    ]

    def __init__(self, images, pos, groups):
        """
        Args:
            images (list): List of image surfaces loaded via pygame.image.load.
            pos (tuple): X and Y axis positions where the FlyMan will be draw.
            groups (list): A list of pygame.sprite.Group.
        """
        super(FlyMan, self).__init__(images[0], pos, groups)
        self.image_frames = images
        self.vx = random.randrange(1, 4)
        self.vy = 0
        self.dy = 0.5

        # if it starts on the right side of the screen
        if self.rect.x > settings.WIDTH / 2:
            self.vx *= -1  # invert direction

    def update(self):
        """Move FlyMan or kill it if leaves the screen."""
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect.y += self.vy

        # switch direction on Y axis if reached the boundaries
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1

        if self.rect.left > settings.WIDTH + 100 or self.rect.right < -100:
            self.kill()
        else:
            self.animate()

    def animate(self):
        """Switch between image frames."""
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update = now
            center = self.rect.center
            if self.dy < 0:  # going up
                if self.image == self.image_frames[0]:
                    self.image = self.image_frames[3]
                else:
                    self.image = self.image_frames[0]
            else:  # going down
                if self.image == self.image_frames[1]:
                    self.image = self.image_frames[4]
                else:
                    self.image = self.image_frames[1]
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = center
