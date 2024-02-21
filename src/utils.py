import os

import pygame

IMAGES_DIR = "assets/images/"


def load_image(path: str) -> pygame.Surface:
    """Load image from assets/image/ directory

    Args:
        path (str): relative path to image in assets/image/

    Returns:
        pygame.Surface: loaded image
    """
    img = pygame.image.load(IMAGES_DIR + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path: str) -> list[pygame.Surface]:
    """Load images from assets/image/ directory

    Args:
        path (str): relative path to directory with images in assets/image/

    Returns:
        list[pygame.Surface]: list of loaded images
    """
    imgs = []

    for image_path in sorted(os.listdir(IMAGES_DIR + path)):
        imgs.append(load_image(path + "/" + image_path))

    return imgs
