import pygame
import settings
import random


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
