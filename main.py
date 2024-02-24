from __future__ import annotations

import math
import random
import sys

import pygame
from pygame import Vector2 as Vec2

from src.Animation import Animation
from src.Clouds import Clouds
from src.Enemy import Enemy
from src.Particle import Particle
from src.Player import Player
from src.Tilemap import Tilemap
from src.utils import load_image, load_images


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((960, 720))
        self.display = pygame.Surface((320, 240))
        self.display_center = Vec2(self.display.get_size()) / 2

        self.assets = {
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            # tiles graphics with variants
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone"),
            "decor": load_images("tiles/decor"),
            "large_decor": load_images("tiles/large_decor"),
            "spawners": load_images("tiles/spawners"),
            # player graphics with animations
            "player": load_image("entities/player.png"),
            "player/idle": Animation(load_images("entities/player/idle"), duration=6),
            "player/run": Animation(load_images("entities/player/run"), duration=4),
            "player/jump": Animation(load_images("entities/player/jump")),
            "player/wall_slide": Animation(load_images("entities/player/wall_slide")),
            # enemies graphics
            "enemy/idle": Animation(load_images("entities/enemy/idle"), duration=6),
            "enemy/run": Animation(load_images("entities/enemy/run"), duration=4),
            "gun": load_image("gun.png"),
            # particles animations
            "particle/leaf": Animation(
                load_images("particles/leaf"), duration=20, loop=False
            ),
            "particle/particle": Animation(
                load_images("particles/particle"), loop=False
            ),
        }

        self.tilemap = Tilemap(self.assets, tile_size=16)
        self.clouds = Clouds(self.assets["clouds"])
        self.particles: list[Particle] = []
        self.camera_offset = Vec2(0, 0)

        self.movement = [False, False]
        self.player = Player(self.assets, self.particles, Vec2(0, 0), Vec2(8, 15))

        self.tilemap.load("assets/maps/0.json")

        player_tile = next(self.tilemap.extract("spawners", 0))
        self.player.set_position(Vec2(player_tile["pos"]))

        self.enemies: list[Enemy] = []
        for enemy in self.tilemap.extract("spawners", 1):
            self.enemies.append(Enemy(self.assets, Vec2(enemy["pos"]), Vec2(8, 15)))

        self.leaf_spawners: list[pygame.Rect] = []
        for tree in self.tilemap.extract("large_decor", variant=2, keep=True):
            x, y = tree["pos"]
            self.leaf_spawners.append(pygame.Rect(x + 4, y + 4, 23, 13))

    def run(self) -> None:
        clock = pygame.time.Clock()

        while True:
            # update each game element
            self.player.update(
                self.tilemap, Vec2(self.movement[1] - self.movement[0], 0)
            )
            self.clouds.update()

            for enemy in self.enemies:
                enemy.update(self.tilemap)

            for particle in self.particles.copy():
                to_remove = particle.update()

                if particle.type == "leaf":
                    particle.position.x += (
                        math.sin(particle.animation_frame * 0.035) * 0.3
                    )

                if to_remove:
                    self.particles.remove(particle)

            # spawn leafs
            for spawner in self.leaf_spawners:
                if random.random() * 39999 < spawner.width * spawner.height:
                    x = spawner.x + random.random() * spawner.width
                    y = spawner.y + random.random() * spawner.height
                    self.particles.append(
                        Particle(self.assets, "leaf", Vec2(x, y), Vec2(-0.1, 0.3))
                    )

            # render everything to the display
            self.display.blit(self.assets["background"], (0, 0))
            render_offset = self._update_camera()
            self.clouds.render(self.display, render_offset)
            self.tilemap.render(self.display, render_offset)
            for enemy in self.enemies:
                enemy.render(self.display, render_offset)
            self.player.render(self.display, render_offset)
            for particle in self.particles:
                particle.render(self.display, render_offset)

            self._handle_events()
            self._update_screen()

            clock.tick(60)

    def _update_camera(self) -> Vec2:
        self.camera_offset += (
            self.player.rect.center - self.display_center - self.camera_offset
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
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_j:
                    self.player.dash()
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
