import os

import pygame

IMAGES_DIR = "../assets/images"


def load_image(image_path: str) -> pygame.Surface:
    img = pygame.image.load(IMAGES_DIR + "/" + image_path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(images_path: str) -> list[pygame.Surface]:
    imgs = []

    for image_path in os.listdir(IMAGES_DIR + "/" + images_path):
        imgs.append(load_image(image_path))

    return imgs


load_images("clouds")
