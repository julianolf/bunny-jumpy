import pygame
import settings
import random


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
        image_names (list): List of image names that
                            will be render inside the sprite.
    """
    _layer = settings.PLATFORM_LAYER
    image_names = {
        'cake': [
            'ground_cake.png', 'ground_cake_broken.png',
            'ground_cake_small.png', 'ground_cake_small_broken.png'
        ],
        'sand': [
            'ground_sand.png', 'ground_sand_broken.png',
            'ground_sand_small.png', 'ground_sand_small_broken.png'
        ],
        'snow': [
            'ground_snow.png', 'ground_snow_broken.png',
            'ground_snow_small.png', 'ground_snow_small_broken.png'
        ],
        'wood': [
            'ground_wood.png', 'ground_wood_broken.png',
            'ground_wood_small.png', 'ground_wood_small_broken.png'
        ],
        'grass': [
            'ground_grass.png', 'ground_grass_broken.png',
            'ground_grass_small.png', 'ground_grass_small_broken.png'
        ],
        'stone': [
            'ground_stone.png', 'ground_stone_broken.png',
            'ground_stone_small.png', 'ground_stone_small_broken.png'
        ]
    }

    def __init__(self, image, pos=(0, 0), groups=[]):
        """
        Args:
            image (pygame.Surface): Platform image surface.
            pos (tuple): X and Y axis positions.
            groups (list): The list of groups the platform belongs to.
        """
        super(Platform, self).__init__(image, pos, groups)

    def update(self):
        """Kills the platform when it gets off the screen."""
        if self.rect.top >= settings.HEIGHT:
            self.kill()

    @classmethod
    def new(cls, game, image_name=None, **kwargs):
        """Create a new instance of a platform.

        Args:
            game (Game): A reference for the running game.
            image_name (str): Type and image name separeted by a pipe.
        """
        if image_name:
            tp, nm = image_name.split('|')
        else:
            tp = random.choice(list(cls.image_names.keys()))
            nm = random.choice(cls.image_names[tp])
        image = game.spritesheet.get_image(nm)
        return cls(image, **kwargs)


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

    @classmethod
    def new(cls, game, **kwargs):
        """Create a new instance of a cloud.

        Args:
            game (Game): A reference for the running game.
        """
        image = game.spritesheet.get_image(cls.image_name)
        return cls(image, **kwargs)
