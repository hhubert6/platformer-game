import math

import pygame
from pygame import Vector2 as Vec2


class Spark:
    def __init__(self, position: Vec2, angle: float, speed: float) -> None:
        self._position = position
        self._angle = angle
        self._speed = speed
        self._norm_velocity = Vec2(math.cos(self._angle), math.sin(self._angle))

    def update(self) -> bool:
        self._position.x += self._norm_velocity.x * self._speed
        self._position.y += self._norm_velocity.y * self._speed

        self._speed = max(self._speed - 0.1, 0)
        return self._speed == 0

    def render(self, display: pygame.Surface, offset: Vec2 = Vec2(0, 0)) -> None:
        points: list[Vec2] = []
        for angle, factor in [(0, 3), (90, 0.5), (180, 3), (270, 0.5)]:
            points.append(
                self._position
                + self._norm_velocity.rotate(angle) * self._speed * factor
                - offset
            )

        pygame.draw.polygon(display, (255, 255, 255), points)
