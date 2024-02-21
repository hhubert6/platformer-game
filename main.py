from __future__ import annotations

import sys

import pygame
from pygame import Vector2 as Vec2

from Clouds import Clouds
from src.Entity import Entity
from src.Tilemap import Tilemap
from src.utils import load_image, load_images


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.display_center = Vec2(self.display.get_size()) / 2

        self.assets = {
            "player": load_image("entities/player.png"),
            "clouds": load_images("clouds"),
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone"),
            "background": load_image("background.png"),
        }

        self.tilemap = Tilemap(tile_size=16)
        self.clouds = Clouds(self.assets["clouds"])

        self.movement = [False, False]
        self.player = Entity("player", Vec2(50, 50), Vec2(8, 15))

        self.camera_offset = Vec2(0, 0)

    def run(self) -> None:
        clock = pygame.time.Clock()

        while True:
            # update each game element
            self.player.update(
                self.tilemap, Vec2(self.movement[1] - self.movement[0], 0)
            )
            self.clouds.update()

            # render everything to the display
            self.display.blit(self.assets["background"], (0, 0))
            render_offset = self._update_camera()
            self.clouds.render(self.display, render_offset)
            self.tilemap.render(self.display, self.assets, render_offset)
            self.player.render(self.display, self.assets, render_offset)

            self._handle_events()
            self._update_screen()

            clock.tick(60)

    def _update_camera(self) -> Vec2:
        self.camera_offset += (
            self.player.get_rect().center - self.display_center - self.camera_offset
        ) / 20
        return Vec2(int(self.camera_offset.x), int(self.camera_offset.y))

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.movement[1] = True
                elif event.key == pygame.K_a:
                    self.movement[0] = True
                elif event.key == pygame.K_w:
                    self.player._velocity.y = -3
                elif event.key == pygame.K_SPACE:
                    self.player._velocity.y = -3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.movement[1] = False
                elif event.key == pygame.K_a:
                    self.movement[0] = False

    def _update_screen(self) -> None:
        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
        )
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
