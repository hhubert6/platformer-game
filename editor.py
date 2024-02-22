from __future__ import annotations

import sys

import pygame
from pygame import Vector2 as Vec2

from src.Tilemap import Tilemap
from src.utils import load_images


class Editor:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((960, 720))
        self.display = pygame.Surface((320, 240))
        self.display_center = Vec2(self.display.get_size()) / 2
        self.render_scale = self.display.get_width() / self.screen.get_width()

        self.assets = {
            # tiles graphics with variants
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone"),
            "decor": load_images("tiles/decor"),
            "large_decor": load_images("tiles/large_decor"),
            "spawners": load_images("tiles/spawners"),
        }

        self.tilemap = Tilemap(self.assets, tile_size=16)
        self.movement = [False, False, False, False]
        self.camera_offset = Vec2(0, 0)

        self.tiles = ["grass", "stone", "decor", "large_decor", "spawners"]
        self.current_type = 0
        self.current_variant = 0
        self.on_grid = True

        self.clicking = False
        self.right_clicking = False

    def run(self) -> None:
        clock = pygame.time.Clock()

        while True:
            # rendering
            self.display.fill((11, 100, 220))
            render_offset = self._update_camera()
            self.tilemap.render(self.display, render_offset)

            tile_img = self.assets[self.tiles[self.current_type]][
                self.current_variant
            ].copy()
            tile_img.set_alpha(150)
            self.display.blit(tile_img, (10, 10))

            mouse_pos = Vec2(pygame.mouse.get_pos()) * self.render_scale
            grid_pos = (mouse_pos + render_offset) // self.tilemap._tile_size

            if self.on_grid:
                self.display.blit(
                    tile_img, grid_pos * self.tilemap._tile_size - render_offset
                )
            else:
                self.display.blit(tile_img, mouse_pos)

            # adding tiles
            if self.clicking and self.on_grid:
                pos = int(grid_pos.x), int(grid_pos.y)
                self.tilemap._tiles[pos] = {
                    "type": self.tiles[self.current_type],
                    "variant": self.current_variant,
                    "pos": pos,
                }

            if self.right_clicking and self.on_grid:
                pos = int(grid_pos.x), int(grid_pos.y)
                if pos in self.tilemap._tiles:
                    del self.tilemap._tiles[pos]

            self._handle_events()
            self._update_screen()

            clock.tick(60)

    def _update_camera(self) -> Vec2:
        self.camera_offset += (
            Vec2(
                self.movement[1] - self.movement[0], self.movement[2] - self.movement[3]
            )
            * 3
        )
        return Vec2(int(self.camera_offset.x), int(self.camera_offset.y))

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movement[0] = True
                elif event.key == pygame.K_d:
                    self.movement[1] = True
                elif event.key == pygame.K_s:
                    self.movement[2] = True
                elif event.key == pygame.K_w:
                    self.movement[3] = True
                elif event.key == pygame.K_UP:
                    self.current_type = (self.current_type + 1) % len(self.tiles)
                    self.current_variant = 0
                elif event.key == pygame.K_DOWN:
                    self.current_type = (self.current_type - 1) % len(self.tiles)
                    self.current_variant = 0
                elif event.key == pygame.K_RIGHT:
                    self.current_variant = (self.current_variant + 1) % len(
                        self.assets[self.tiles[self.current_type]]
                    )
                elif event.key == pygame.K_LEFT:
                    self.current_variant = (self.current_variant - 1) % len(
                        self.assets[self.tiles[self.current_type]]
                    )
                elif event.key == pygame.K_g:
                    self.on_grid = not self.on_grid
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement[0] = False
                elif event.key == pygame.K_d:
                    self.movement[1] = False
                elif event.key == pygame.K_s:
                    self.movement[2] = False
                elif event.key == pygame.K_w:
                    self.movement[3] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True
                elif event.button == 3:
                    self.right_clicking = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                elif event.button == 3:
                    self.right_clicking = False

    def _update_screen(self) -> None:
        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
        )
        pygame.display.update()


if __name__ == "__main__":
    game = Editor()
    game.run()
