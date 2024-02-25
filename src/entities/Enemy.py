import math
import random
from typing import Any

import pygame
from pygame import Surface
from pygame import Vector2 as Vec2

from src.entities.Entity import Entity
from src.entities.Player import Player
from src.Spark import Spark
from src.Tilemap import Tilemap


class Enemy(Entity):
    def __init__(
        self,
        assets: dict[str, Any],
        projectiles: list[list],
        sparks: list[Spark],
        player: Player,
        position: Vec2,
        size: Vec2,
    ) -> None:
        super().__init__(assets, "enemy", position, size)
        self._projectiles = projectiles
        self._sparks = sparks
        self._player = player
        self._walking = 0

    def update(self, tilemap: Tilemap) -> None:
        movement = Vec2(0, 0)

        if self._walking > 0:
            check_offset = Vec2((-8 if self._flip else 8), 16)
            check_offset2 = Vec2((-8 if self._flip else 8), 0)

            is_groud_ahead = tilemap.check_solid_tile(self.rect.center + check_offset)
            is_wall_ahead = tilemap.check_solid_tile(self.rect.center + check_offset2)

            if is_groud_ahead and not is_wall_ahead:
                movement.x = -0.5 if self._flip else 0.5
            else:
                self._flip = not self._flip

            self._walking -= 1

            if self._walking == 0:
                self._shoot()
        elif random.random() < 0.01:
            self._walking = random.randint(30, 120)

        super().update(tilemap, movement)

        if movement.x != 0:
            self._set_action("run")
        else:
            self._set_action("idle")

    def _shoot(self) -> None:
        dist = self._player._position - self._position

        if abs(dist.y) < 16:
            if self._flip and dist.x < 0:
                pos = Vec2(self.rect.centerx - 7, self.rect.centery)
                dir = -1.5
                self._projectiles.append([pos, dir, 0])

                for _ in range(4):
                    self._sparks.append(
                        Spark(
                            pos.copy(),
                            random.random() - 0.5 + math.pi,
                            2 + random.random(),
                        )
                    )
            if not self._flip and dist.x > 0:
                pos = Vec2(self.rect.centerx + 7, self.rect.centery)
                dir = 1.5
                self._projectiles.append([pos, dir, 0])

                for _ in range(4):
                    self._sparks.append(
                        Spark(
                            pos.copy(),
                            random.random() - 0.5,
                            2 + random.random(),
                        )
                    )

    def render(self, display: Surface, offset: Vec2 = Vec2(0, 0)) -> None:
        super().render(display, offset)

        x, y = self.rect.center
        gun_img = pygame.transform.flip(self._assets["gun"], self._flip, False)
        gun_x_offset = -gun_img.get_width() - 4 if self._flip else 4

        display.blit(gun_img, Vec2(x + gun_x_offset, y) - offset)
