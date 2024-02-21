from __future__ import annotations

import sys

import pygame
from pygame import Vector2 as Vec2

from src.Entity import Entity
from src.Tilemap import Tilemap
from src.utils import load_image, load_images


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.assets = {
            "player": load_image("entities/player.png"),
            "clouds": load_images("clouds"),
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone"),
        }

        self.tilemap = Tilemap(tile_size=16)

        self.movement = [False, False]
        self.player = Entity("player", Vec2(50, 50), Vec2(8, 15))

    def run(self) -> None:
        clock = pygame.time.Clock()

        while True:
            self.player.update(
                self.tilemap, Vec2(self.movement[1] - self.movement[0], 0)
            )

            self.display.fill((100, 100, 200))
            self.tilemap.render(self.display, self.assets)
            self.player.render(self.display, self.assets)

            self._handle_events()
            self._update_screen()

            clock.tick(60)

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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.movement[1] = False
                elif event.key == pygame.K_a:
                    self.movement[0] = False

    def _update_screen(self) -> None:
        self.screen.blit(
            pygame.transform.scale(
                self.display, (self.screen.get_width(), self.screen.get_height())
            ),
            (0, 0),
        )
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
