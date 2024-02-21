import random

import pygame
from pygame import Vector2 as Vec2


class _Cloud:
    def __init__(
        self, position: Vec2, speed: float, image: pygame.Surface, depth: float
    ) -> None:
        self._position = position
        self._speed = speed
        self._image = image
        self._depth = depth

    def update(self) -> None:
        self._position.x += self._speed * self._depth

    def render(self, display: pygame.Surface, offset: Vec2) -> None:
        render_position = self._position - offset * self._depth
        x = (
            render_position.x % (display.get_width() + self._image.get_width())
            - self._image.get_width()
        )
        y = (
            render_position.y % (display.get_height() + self._image.get_height())
            - self._image.get_height()
        )
        display.blit(self._image, (x, y))


class Clouds:
    def __init__(self, cloud_images, count=16) -> None:
        self._clouds: list[_Cloud] = []

        for _ in range(count):
            pos = Vec2(random.random() * 999, random.random() * 999)
            speed = random.random() * 0.05 + 0.1
            img = random.choice(cloud_images)
            depth = random.random() * 0.6 + 0.2

            self._clouds.append(_Cloud(pos, speed, img, depth))

        self._clouds.sort(key=lambda x: x._depth)

    def update(self) -> None:
        for cloud in self._clouds:
            cloud.update()

    def render(self, display: pygame.Surface, offset: Vec2 = Vec2(0, 0)):
        for cloud in self._clouds:
            cloud.render(display, offset)
