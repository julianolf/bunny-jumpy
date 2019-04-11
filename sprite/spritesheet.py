from xml.dom import minidom

import pygame

import settings


class Spritesheet(object):
    """Manage image spritesheets."""

    def __init__(self, file_name, color_key=settings.BLACK):
        """
        Args:
            file_name (str): Spritesheet (full path) file name.
        """
        super(Spritesheet, self).__init__()
        self.image = pygame.image.load(file_name).convert()
        self.info = minidom.parse(file_name.replace(".png", ".xml"))
        self.color_key = color_key

    def get_info(self, image_name):
        """Get image position and size.

        Return where in the spritesheet the image starts and what is its size.

        Args:
            image_name (str): The image name.

        Returns:
            Four values are returned (x, y, width, height).
            x (int): X axis value.
            y (int): Y axis value.
            width (int): Image size horizontally.
            height (int): Image size vertically.

        Raises:
            ValueError: If no entry was found for image_name.
        """
        nodes = self.info.getElementsByTagName("SubTexture")
        for node in nodes:
            if node.getAttribute("name") == image_name:
                return map(
                    int,
                    (
                        node.getAttribute("x"),
                        node.getAttribute("y"),
                        node.getAttribute("width"),
                        node.getAttribute("height"),
                    ),
                )
        raise ValueError(f"{image_name} not found in spritesheet.")

    def get_image(self, image_name):
        """Get image by name.

        Args:
            image_name (str): The image name.

        Returns:
            A pygame.Surface instance representing the image.
        """
        x, y, width, height = self.get_info(image_name)
        image = pygame.Surface((width, height))
        image.blit(self.image, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(
            image, (width * 2 // 5, height * 2 // 5)
        )
        image.set_colorkey(self.color_key)
        return image
