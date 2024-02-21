from __future__ import annotations

import pygame
from pygame import Vector2 as Vec2


class Entity:
    def __init__(self, type: str, position: Vec2, size: Vec2) -> None:
        self.type = type
        self.size = size
        self.position = position
        self.velocity = Vec2(0, 0)

    def update(self, movement: Vec2) -> None:
        self.position += movement + self.velocity
        self.velocity.y += 0.0

    def render(
        self, display: pygame.Surface, assets: dict[str, pygame.Surface]
    ) -> None:
        display.blit(assets[self.type], self.position)
