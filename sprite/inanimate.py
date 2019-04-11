import random

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
        image_names (list): List of image names that
                            will be render inside the sprite.
    """

    _layer = settings.PLATFORM_LAYER
    image_names = [
        "ground_cake.png",
        "ground_cake_broken.png",
        "ground_cake_small.png",
        "ground_cake_small_broken.png" "ground_sand.png",
        "ground_sand_broken.png",
        "ground_sand_small.png",
        "ground_sand_small_broken.png" "ground_snow.png",
        "ground_snow_broken.png",
        "ground_snow_small.png",
        "ground_snow_small_broken.png" "ground_wood.png",
        "ground_wood_broken.png",
        "ground_wood_small.png",
        "ground_wood_small_broken.png" "ground_grass.png",
        "ground_grass_broken.png",
        "ground_grass_small.png",
        "ground_grass_small_broken.png" "ground_stone.png",
        "ground_stone_broken.png",
        "ground_stone_small.png",
        "ground_stone_small_broken.png",
    ]

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
        if not image_name:
            image_name = random.choice(cls.image_names)
        image = game.spritesheet.get_image(image_name)
        return cls(image, **kwargs)


class Spring(Inanimate):
    """Describes springs.

    Attributes:
        _layer (int): The layer where the spring will be draw.
        image_names (list): List of image names that
                            will be render inside the sprite.
    """

    _layer = settings.PLATFORM_LAYER
    image_names = ["spring.png", "spring_in.png", "spring_out.png"]

    def __init__(self, images, platform, pos=(0, 0), groups=[]):
        """
        Args:
            images (list): List of spring image surfaces.
            platform (Platform): A platform where the spring will be attached.
            pos (tuple): X and Y axis positions.
            groups (list): The list of groups the spring belongs to.
        """
        super(Spring, self).__init__(images[0], pos, groups)
        self.frames = images
        self.platform = platform
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top
        self.fired = False
        self.last_update = 0

    def animate(self):
        """Switch between image frames."""
        now = pygame.time.get_ticks()

        if self.fired:
            if now - self.last_update > 100:
                self.last_update = now
                centerx = self.rect.centerx
                bottom = self.rect.bottom
                index = (self.frames.index(self.image) + 1) % 3
                self.image = self.frames[index]
                self.rect = self.image.get_rect()
                self.rect.centerx = centerx
                self.rect.bottom = bottom
                self.fired = bool(index)

    def update(self):
        """Kills spring if its platform does not exist anymore
        or update its position following the platform."""
        if self.platform and not self.platform.alive():
            self.kill()
        else:
            self.rect.bottom = self.platform.rect.top

        # animate spring sprite
        self.animate()

    @classmethod
    def new(cls, game, platform, **kwargs):
        """Create a new instance of a spring.

        Args:
            game (Game): A reference for the running game.
            platform (Platform): A platform where the spring will be attached.
        """
        images = [game.spritesheet.get_image(img) for img in cls.image_names]
        return cls(images, platform, **kwargs)


class Cloud(Inanimate):
    """Describes clouds.

    Attributes:
        _layer (int): The layer where the cloud will be draw.
        image_name (str): Cloud image name.
    """

    _layer = settings.CLOUD_LAYER
    image_name = "cloud.png"

    def __init__(self, image, pos=(0, 0), groups=[]):
        """
        Args:
            image (pygame.Surface): Cloud image surface.
            pos (tuple): X and Y axis positions.
            groups (list): The list of groups the cloud belongs to.
        """
        super(Cloud, self).__init__(image, pos, groups)

    def update(self):
        """Kills the cloud when it reaches two times the screen height."""
        if self.rect.y > settings.HEIGHT * 2:
            self.kill()

    @classmethod
    def new(cls, image, **kwargs):
        """Create a new instance of a cloud.

        Args:
            image (pygame.Surface): Cloud image surface.
        """
        width = image.get_width()
        height = image.get_height()
        scale = random.randint(30, 101) / 100
        size = (int(width * scale), int(height * scale))
        img = pygame.transform.scale(image, size)
        return cls(img, **kwargs)
