from __future__ import annotations

import pygame


class Tilemap:
    def __init__(self, tile_size: int = 16) -> None:
        self.tile_size = tile_size
        self.tiles: dict[tuple[int, int], dict] = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tiles[(10, 3 + i)] = {"type": "stone", "variant": 0}
            self.tiles[(3 + i, 10)] = {"type": "grass", "variant": 0}

    def render(
        self, display: pygame.Surface, assets: dict[str, list[pygame.Surface]]
    ) -> None:
        for tile in self.offgrid_tiles:
            display.blit(assets[tile["type"]][tile["variant"]], tile["pos"])

        for pos in self.tiles:
            tile = self.tiles[pos]
            dest = pos[0] * self.tile_size, pos[1] * self.tile_size
            display.blit(assets[tile["type"]][tile["variant"]], dest)
