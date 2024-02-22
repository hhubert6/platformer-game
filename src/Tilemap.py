from __future__ import annotations

import json
from typing import Any, Iterator

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
    def __init__(self, assets: dict[str, Any], tile_size: int = 16) -> None:
        self._assets = assets
        self._tile_size = tile_size
        self._tiles: dict[tuple[int, int], dict] = {}
        self._offgrid_tiles = []

    def render(
        self,
        display: pygame.Surface,
        offset: Vec2 = Vec2(0, 0),
    ) -> None:
        self._render_offgrid_tiles(display, offset)
        self._render_grid_tiles(display, offset)

    def _render_offgrid_tiles(
        self,
        display: pygame.Surface,
        offset: Vec2,
    ) -> None:
        for tile in self._offgrid_tiles:
            pos = Vec2(tile["pos"]) - offset
            display.blit(self._assets[tile["type"]][tile["variant"]], pos)

    def _render_grid_tiles(
        self,
        display: pygame.Surface,
        offset: Vec2,
    ) -> None:
        for x in range(
            int(offset.x) // self._tile_size,
            int(offset.x + display.get_width()) // self._tile_size + 1,
        ):
            for y in range(
                int(offset.y) // self._tile_size,
                int(offset.y + display.get_height()) // self._tile_size + 1,
            ):
                pos = x, y
                if pos in self._tiles:
                    tile = self._tiles[pos]
                    dest = Vec2(pos) * self._tile_size - offset
                    display.blit(self._assets[tile["type"]][tile["variant"]], dest)

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

    def load(self, path: str):
        self._tiles = {}

        with open(path, "r") as f:
            data = json.load(f)

            self._tile_size = data["tile_size"]

            for key in data["tilemap"]:
                tile = data["tilemap"][key]
                pos = tuple(tile["pos"])
                self._tiles[pos] = tile

            for tile in data["offgrid"]:
                tile["pos"] = tuple(tile["pos"])
                self._offgrid_tiles.append(tile)
