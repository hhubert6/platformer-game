from typing import Any

from pygame import Vector2 as Vec2

from src.Entity import Entity
from src.Tilemap import Tilemap


class Player(Entity):
    def __init__(self, assets: dict[str, Any], position: Vec2, size: Vec2) -> None:
        super().__init__(assets, "player", position, size)
        self._air_time = 0
        self._jumps = 1
        self._wall_slide = False

    def update(self, tilemap: Tilemap, movement: Vec2 = Vec2(0, 0)) -> None:
        super().update(tilemap, movement)

        if self._velocity.x > 0:
            self._velocity.x = max(self._velocity.x - 0.1, 0)
        elif self._velocity.x < 0:
            self._velocity.x = min(self._velocity.x + 0.1, 0)

        self._air_time += 1

        if self._collisions["down"]:
            self._air_time = 0
            self._jumps = 1

        self._wall_slide = False

        if self._air_time > 4:
            if self._collisions["right"] or self._collisions["left"]:
                self._wall_slide = True
                self._flip = self._collisions["left"]
                self._velocity.y = min(self._velocity.y, 0.5)
                self._set_action("wall_slide")
            else:
                self._set_action("jump")
        elif movement.x != 0:
            self._set_action("run")
        else:
            self._set_action("idle")

    def jump(self) -> None:
        if self._wall_slide:
            if self._flip and self._last_movement.x < 0:
                self._velocity.x = 3.5
            elif not self._flip and self._last_movement.x > 0:
                self._velocity.x = -3.5
            self._velocity.y = -2.5
            self._jumps = max(self._jumps - 1, 0)
        elif self._jumps > 0:
            self._velocity.y = -3
            self._jumps -= 1
