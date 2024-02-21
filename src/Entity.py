from __future__ import annotations

import pygame
from pygame import Vector2 as Vec2

from src.Tilemap import Tilemap

G_FORCE = 0.1
TERMINAL_VELOCITY = 5


class Entity:
    def __init__(self, type: str, position: Vec2, size: Vec2) -> None:
        self._type = type
        self._size = size
        self._position = position
        self._velocity = Vec2(0, 0)

    def update(self, tilemap: Tilemap, movement: Vec2 = Vec2(0, 0)) -> None:
        frame_movement = movement + self._velocity

        self._position.x += frame_movement.x
        entity_rect = self.get_rect()

        for tile_rect in tilemap.get_physics_rects_around(self._position):
            if entity_rect.colliderect(tile_rect):
                if frame_movement.x > 0:
                    entity_rect.right = tile_rect.left
                elif frame_movement.x < 0:
                    entity_rect.left = tile_rect.right

                self._position.x = entity_rect.x

        self._position.y += frame_movement.y
        entity_rect = self.get_rect()

        for tile_rect in tilemap.get_physics_rects_around(self._position):
            if entity_rect.colliderect(tile_rect):
                if frame_movement.y > 0:
                    entity_rect.bottom = tile_rect.top
                elif frame_movement.y < 0:
                    entity_rect.top = tile_rect.bottom

                self._velocity.y = 0
                self._position.y = entity_rect.y

        self._velocity.y = min(TERMINAL_VELOCITY, self._velocity.y + G_FORCE)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self._position, self._size)

    def render(
        self,
        display: pygame.Surface,
        assets: dict[str, pygame.Surface],
        offset: Vec2 = Vec2(0, 0),
    ) -> None:
        display.blit(assets[self._type], self._position - offset)
