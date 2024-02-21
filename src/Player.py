from typing import Any

from pygame import Vector2 as Vec2

from src.Entity import Entity
from src.Tilemap import Tilemap


class Player(Entity):
    def __init__(self, assets: dict[str, Any], position: Vec2, size: Vec2) -> None:
        super().__init__(assets, "player", position, size)
        self._air_time = 0

    def update(self, tilemap: Tilemap, movement: Vec2 = Vec2(0, 0)) -> None:
        super().update(tilemap, movement)

        self._air_time += 1

        if self._collisions["down"]:
            self._air_time = 0

        if self._air_time > 4:
            self._set_action("jump")
        elif movement.x != 0:
            self._set_action("run")
        else:
            self._set_action("idle")

    def jump(self) -> None:
        self._velocity.y = -3
