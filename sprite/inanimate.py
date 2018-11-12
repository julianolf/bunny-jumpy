import pygame
import settings


class Inanimate(pygame.sprite.Sprite):
    """Describes common behavior and attributes between inanimate things."""

    def __init__(self, image, pos, groups):
        """
        Args:
            image (pygame.Surface): Image surface loaded via pygame.image.load.
            pos (tuple): X and Y axis positions where the sprite will be draw.
            groups (list): A list of pygame.sprite.Group.
        """
        super(Inanimate, self).__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Platform(Inanimate):
    """Describes platforms.

    Attributes:
        _layer (int): The layer where the platform will be draw.
    """
    _layer = settings.PLATFORM_LAYER

    def __init__(self, image, pos=(0, 0), groups=[]):
        """
        Args:
            image (pygame.Surface): Platform image surface.
            pos (tuple): X and Y axis positions.
            groups (list): The list of groups the platform belongs to.
        """
        super(Platform, self).__init__(image, pos, groups)


class Cloud(Inanimate):
    """Describes clouds.

    Attributes:
        _layer (int): The layer where the cloud will be draw.
        image_name (str): Cloud image name.
    """
    _layer = settings.CLOUD_LAYER
    image_name = 'cloud.png'

    def __init__(self, image, pos=(0, 0), groups=[]):
        """
        Args:
            image (pygame.Surface): Platform image surface.
            pos (tuple): X and Y axis positions.
            groups (list): The list of groups the platform belongs to.
        """
        super(Cloud, self).__init__(image, pos, groups)

    def update(self):
        """Kills the cloud when it reaches two times the screen height."""
        if self.rect.y > settings.HEIGHT * 2:
            self.kill()
