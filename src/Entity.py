from __future__ import annotations

from typing import Any

import pygame
from pygame import Vector2 as Vec2

from src.Animation import Animation
from src.Tilemap import Tilemap

G_FORCE = 0.1
TERMINAL_VELOCITY = 5


class Entity:
    def __init__(
        self, assets: dict[str, Any], entity_type: str, position: Vec2, size: Vec2
    ) -> None:
        self._assets = assets
        self._type = entity_type
        self._size = size
        self._position = position
        self._velocity = Vec2(0, 0)
        self._collisions = {"up": False, "down": False, "right": False, "left": False}

        self._action = ""
        self._anim_offset = Vec2(-3, -3)
        self._flip = False
        self._set_action("idle")

    def _set_action(self, action: str) -> None:
        if self._action != action:
            self._action = action
            self._animation: Animation = self._assets[self._type + "/" + action].copy()

    def update(self, tilemap: Tilemap, movement: Vec2 = Vec2(0, 0)) -> None:
        for key in self._collisions:
            self._collisions[key] = False

        frame_movement = movement + self._velocity

        if frame_movement.x > 0:
            self._flip = False
        elif frame_movement.x < 0:
            self._flip = True

        self._position.x += frame_movement.x
        entity_rect = self.get_rect()

        for tile_rect in tilemap.get_physics_rects_around(self._position):
            if entity_rect.colliderect(tile_rect):
                if frame_movement.x > 0:
                    entity_rect.right = tile_rect.left
                    self._collisions["right"] = True
                elif frame_movement.x < 0:
                    entity_rect.left = tile_rect.right
                    self._collisions["left"] = True

                self._position.x = entity_rect.x

        self._position.y += frame_movement.y
        entity_rect = self.get_rect()

        for tile_rect in tilemap.get_physics_rects_around(self._position):
            if entity_rect.colliderect(tile_rect):
                if frame_movement.y > 0:
                    entity_rect.bottom = tile_rect.top
                    self._collisions["down"] = True
                elif frame_movement.y < 0:
                    entity_rect.top = tile_rect.bottom
                    self._collisions["up"] = True

                self._position.y = entity_rect.y

        self._velocity.y = min(TERMINAL_VELOCITY, self._velocity.y + G_FORCE)

        if self._collisions["up"] or self._collisions["down"]:
            self._velocity.y = 0

        self._animation.update()

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self._position, self._size)

    def render(
        self,
        display: pygame.Surface,
        offset: Vec2 = Vec2(0, 0),
    ) -> None:
        img = pygame.transform.flip(self._animation.img(), self._flip, False)
        display.blit(img, self._position - offset + self._anim_offset)
