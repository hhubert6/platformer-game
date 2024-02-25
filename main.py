from __future__ import annotations

import math
import random
import sys

import pygame
from pygame import Vector2 as Vec2

from src.Animation import Animation
from src.Clouds import Clouds
from src.entities.Enemy import Enemy
from src.entities.Player import Player
from src.Particle import Particle
from src.Spark import Spark
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
            "projectile": load_image("projectile.png"),
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
        self.projectiles: list[list] = []  # projectile = [Vec2, direction, timer]
        self.sparks: list[Spark] = []
        self.enemies: list[Enemy] = []
        self.leaf_spawners: list[pygame.Rect] = []
        self.camera_offset = Vec2(0, 0)

        self.movement = [False, False]
        self.player = Player(self.assets, self.particles, Vec2(0, 0), Vec2(8, 15))

        self.load_level(0)

    def load_level(self, map_id: int) -> None:
        self.particles.clear()
        self.projectiles.clear()
        self.sparks.clear()
        self.enemies.clear()
        self.leaf_spawners.clear()
        self.camera_offset = Vec2(0, 0)

        self.tilemap.load(f"assets/maps/{map_id}.json")

        player_tile = next(self.tilemap.extract("spawners", 0))
        self.player.set_position(Vec2(player_tile["pos"]))

        for enemy in self.tilemap.extract("spawners", 1):
            self.enemies.append(
                Enemy(
                    self.assets,
                    self.projectiles,
                    self.sparks,
                    self.player,
                    Vec2(enemy["pos"]),
                    Vec2(8, 15),
                )
            )

        for tree in self.tilemap.extract("large_decor", variant=2, keep=True):
            x, y = tree["pos"]
            self.leaf_spawners.append(pygame.Rect(x + 4, y + 4, 23, 13))

    def run(self) -> None:
        clock = pygame.time.Clock()

        while True:
            # update each game element
            player_movement = Vec2(self.movement[1] - self.movement[0], 0)
            self.player.update(self.tilemap, player_movement)

            self.clouds.update()

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap)
                if self.player.is_dashing and self.player.rect.colliderect(enemy.rect):
                    self.enemies.remove(enemy)
                    self._graphical_explosion(Vec2(enemy.rect.center))
                    self.sparks.append(
                        Spark(Vec2(enemy.rect.center), 0, 5 + random.random())
                    )
                    self.sparks.append(
                        Spark(Vec2(enemy.rect.center), math.pi, 5 + random.random())
                    )

            for p in self.particles.copy():
                if p.type == "leaf":
                    p.position.x += math.sin(p.animation_frame * 0.035) * 0.3
                if p.update():
                    self.particles.remove(p)

            for projectile in self.projectiles.copy():
                projectile[0].x += projectile[1]
                projectile[2] += 1
                if self.tilemap.check_solid_tile(projectile[0]):
                    self.projectiles.remove(projectile)
                    for _ in range(4):
                        if projectile[1] < 0:
                            s = Spark(
                                projectile[0].copy(),
                                random.random() - 0.5,
                                2 + random.random(),
                            )
                            self.sparks.append(s)
                        if projectile[1] > 0:
                            s = Spark(
                                projectile[0].copy(),
                                random.random() - 0.5 + math.pi,
                                2 + random.random(),
                            )
                            self.sparks.append(s)

                if (
                    self.player.rect.collidepoint(projectile[0])
                    and not self.player.is_dashing
                ):
                    self.projectiles.remove(projectile)
                    self._graphical_explosion(projectile[0])

                if projectile[2] > 360:
                    self.projectiles.remove(projectile)

            for spark in self.sparks.copy():
                if spark.update():
                    self.sparks.remove(spark)

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
            for projectile in self.projectiles:
                img: pygame.Surface = self.assets["projectile"].copy()
                self.display.blit(
                    img,
                    (
                        projectile[0].x - img.get_width() / 2 - render_offset.x,
                        projectile[0].y - img.get_height() / 2 - render_offset.y,
                    ),
                )
            for spark in self.sparks:
                spark.render(self.display, render_offset)
            for particle in self.particles:
                particle.render(self.display, render_offset)

            self._handle_events()
            self._update_screen()

            clock.tick(60)

    def _graphical_explosion(self, position: Vec2) -> None:
        for _ in range(30):
            angle = random.random() * math.pi * 2
            s = Spark(
                position.copy(),
                angle,
                random.random() + 2,
            )
            self.sparks.append(s)

            speed = random.random() * 5
            p = Particle(
                self.assets,
                "particle",
                position.copy(),
                velocity=Vec2(
                    math.cos(angle + math.pi) * speed * 0.5,
                    math.sin(angle + math.pi) * speed * 0.5,
                ),
                frame=random.randint(0, 3),
            )
            self.particles.append(p)

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
