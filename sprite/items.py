import pygame
import settings


class Powerup(pygame.sprite.Sprite):
    """Describes common behavior and attributes between powerups.

    Attributes:
        layer (int): The layer where the powerup will be draw.
    """
    _layer = settings.POWERUP_LAYER

    def __init__(self, image, platform, groups):
        """
        Args:
            image (pygame.Surface): Image surface loaded via pygame.image.load.
            platform (Platform): A platform where the powerup will be attached.
            groups (list): A list of pygame.sprite.Group.
        """
        super(Powerup, self).__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.platform = platform
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5

    def update(self):
        """Kills powerup if its platform does not exist anymore
        or update its position following the platform."""
        if self.platform and not self.platform.alive():
            self.kill()
        else:
            self.rect.bottom = self.platform.rect.top - 5

    @classmethod
    def new(cls, game, **kwargs):
        """Create a new instance of a power up.

        Args:
            game (Game): A reference for the running game.
        """
        image = game.spritesheet.get_image(cls.image_name)
        return cls(image, **kwargs)


class Jetpack(Powerup):
    """Describes a Jetpack.

    Attributes:
        image_name (str): Image name for the jetpack.
    """
    image_name = 'powerup_jetpack.png'

    def __init__(self, image, platform=None, groups=[]):
        super(Jetpack, self).__init__(image, platform, groups)
