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
AUTOTILE_NEIGHBOURS_OFFSETS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

AUTOTILE_RULES = {
    (2, 3): 0,
    (0, 2, 3): 1,
    (0, 3): 2,
    (0, 1, 3): 3,
    (0, 1): 4,
    (0, 1, 2): 5,
    (1, 2): 6,
    (1, 2, 3): 7,
    (0, 1, 2, 3): 8,
}

PHYSICS_TILES = {"grass", "stone"}
AUTOTILES_TYPES = {"grass", "stone"}


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

    def check_solid_tile(self, position: Vec2) -> bool:
        x, y = tuple(position // self._tile_size)
        key = int(x), int(y)
        return key in self._tiles and self._tiles[key]["type"] in PHYSICS_TILES

    def extract(self, type: str, variant: int, keep: bool = False) -> Iterator[dict]:
        for pos, tile in self._tiles.copy().items():
            if tile["type"] == type and tile["variant"] == variant:
                tile_copy = tile.copy()
                tile_copy["pos"] = (
                    tile["pos"][0] * self._tile_size,
                    tile["pos"][1] * self._tile_size,
                )
                if not keep:
                    del self._tiles[pos]
                yield tile_copy

        for tile in self._offgrid_tiles.copy():
            if tile["type"] == type and tile["variant"] == variant:
                if not keep:
                    self._offgrid_tiles.remove(tile)
                yield tile

    def load(self, path: str) -> None:
        self._tiles = {}
        self._offgrid_tiles = []

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

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            tilemap = {}
            for x, y in self._tiles:
                tilemap[f"{x};{y}"] = self._tiles[x, y]

            json.dump(
                {
                    "tile_size": self._tile_size,
                    "tilemap": tilemap,
                    "offgrid": self._offgrid_tiles,
                },
                f,
            )

    def autotile(self) -> None:
        for x, y in self._tiles:
            tile = self._tiles[x, y]

            if tile["type"] not in AUTOTILES_TYPES:
                continue

            neighbours = []

            for i, (offset_x, offset_y) in enumerate(AUTOTILE_NEIGHBOURS_OFFSETS):
                pos = x + offset_x, y + offset_y
                if pos in self._tiles and tile["type"] == self._tiles[pos]["type"]:
                    neighbours.append(i)

            neighbours = tuple(sorted(neighbours))

            if neighbours in AUTOTILE_RULES:
                tile["variant"] = AUTOTILE_RULES[neighbours]
