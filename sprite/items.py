import pygame
import settings


class Item(pygame.sprite.Sprite):
    """Describes common behavior and attributes between items.

    Attributes:
        layer (int): The layer where the item will be draw.
    """
    _layer = settings.ITEMS_LAYER

    def __init__(self, image, platform, groups):
        """
        Args:
            image (pygame.Surface): Image surface loaded via pygame.image.load.
            platform (Platform): A platform where the item will be attached.
            groups (list): A list of pygame.sprite.Group.
        """
        super(Item, self).__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.platform = platform
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5

    def update(self):
        """Kills item if its platform does not exist anymore
        or update its position following the platform."""
        if self.platform and not self.platform.alive():
            self.kill()
        else:
            self.rect.bottom = self.platform.rect.top - 5

    @classmethod
    def new(cls, game, **kwargs):
        """Create a new instance of a item.

        Args:
            game (Game): A reference for the running game.
        """
        image = game.spritesheet.get_image(cls.image_name)
        return cls(image, **kwargs)


class Carrot(Item):
    """Describes a Carrot.

    Attributes:
        image_name (str): Image name for the carrot.
    """
    image_name = 'carrot.png'

    def __init__(self, image, platform=None, groups=[]):
        """
        Args:
            image (pygame.Surface): Image surface loaded via pygame.image.load.
            platform (Platform): A platform where the carrot will be attached.
            groups (list): A list of pygame.sprite.Group.
        """
        super(Carrot, self).__init__(image, platform, groups)


class Powerup(Item):
    """Describes common behavior and attributes between powerups."""

    def __init__(self, image, platform, groups):
        """
        Args:
            image (pygame.Surface): Image surface loaded via pygame.image.load.
            platform (Platform): A platform where the powerup will be attached.
            groups (list): A list of pygame.sprite.Group.
        """
        super(Powerup, self).__init__(image, platform, groups)


class Jetpack(Powerup):
    """Describes a Jetpack.

    Attributes:
        image_name (str): Image name for the jetpack.
    """
    image_name = 'powerup_jetpack.png'

    def __init__(self, image, platform=None, groups=[]):
        """
        Args:
            image (pygame.Surface): Image surface loaded via pygame.image.load.
            platform (Platform): A platform where the jetpack will be attached.
            groups (list): A list of pygame.sprite.Group.
        """
        super(Jetpack, self).__init__(image, platform, groups)
