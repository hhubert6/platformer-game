from __future__ import annotations

from typing import Iterator

import pygame
from pygame import Vector2 as Vec2

NEIGHBOURS_OFFSETS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

PHYSICS_TILES = {"grass", "stone"}


class Tilemap:
    def __init__(self, tile_size: int = 16) -> None:
        self._tile_size = tile_size
        self._tiles: dict[tuple[int, int], dict] = {}
        self._offgrid_tiles = []

        for i in range(10):
            self._tiles[(10, 3 + i)] = {
                "type": "stone",
                "variant": 0,
                "pos": (10, 3 + i),
            }
            self._tiles[(3 + i, 10)] = {
                "type": "grass",
                "variant": 0,
                "pos": (3 + i, 10),
            }

    def render(
        self,
        display: pygame.Surface,
        assets: dict[str, list[pygame.Surface]],
        offset: Vec2 = Vec2(0, 0),
    ) -> None:
        for tile in self._offgrid_tiles:
            pos = Vec2(tile["pos"]) - offset
            display.blit(assets[tile["type"]][tile["variant"]], pos)

        for pos in self._tiles:
            tile = self._tiles[pos]
            dest = Vec2(pos) * self._tile_size - offset
            display.blit(assets[tile["type"]][tile["variant"]], dest)

    def _get_tiles_around(self, position: Vec2) -> Iterator[dict]:
        tile_x = int(position.x // self._tile_size)
        tile_y = int(position.y // self._tile_size)

        for offset_x, offset_y in NEIGHBOURS_OFFSETS:
            tile_pos = tile_x + offset_x, tile_y + offset_y

            if tile_pos in self._tiles:
                yield self._tiles[tile_pos]

    def get_physics_rects_around(self, position: Vec2) -> Iterator[pygame.Rect]:
        for tile in self._get_tiles_around(position):
            if tile["type"] in PHYSICS_TILES:
                rect_pos = Vec2(tile["pos"]) * self._tile_size
                yield pygame.Rect(rect_pos, (self._tile_size, self._tile_size))
