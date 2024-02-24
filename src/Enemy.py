import random
from typing import Any

import pygame
from pygame import Surface
from pygame import Vector2 as Vec2

from src.Entity import Entity
from src.Tilemap import Tilemap


class Enemy(Entity):
    def __init__(self, assets: dict[str, Any], position: Vec2, size: Vec2) -> None:
        super().__init__(assets, "enemy", position, size)
        self._walking = 0

    def update(self, tilemap: Tilemap) -> None:
        movement = Vec2(0, 0)

        if self._walking > 0:
            check_offset = Vec2((-8 if self._flip else 8), 16)

            if tilemap.check_solid_tile(self.rect.center + check_offset):
                movement.x = -0.5 if self._flip else 0.5
            else:
                self._flip = not self._flip

            self._walking -= 1
        else:
            if random.random() < 0.01:
                self._walking = random.randint(30, 120)

        super().update(tilemap, movement)

        if movement.x != 0:
            self._set_action("run")
        else:
            self._set_action("idle")

    def render(self, display: Surface, offset: Vec2 = Vec2(0, 0)) -> None:
        super().render(display, offset)

        x, y = self.rect.center
        gun_img = pygame.transform.flip(self._assets["gun"], self._flip, False)
        gun_x_offset = -gun_img.get_width() - 4 if self._flip else 4

        display.blit(gun_img, Vec2(x + gun_x_offset, y) - offset)
