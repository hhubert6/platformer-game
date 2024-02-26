import math
import random
from typing import Any

from pygame import Surface
from pygame import Vector2 as Vec2

from src.entities.Entity import Entity
from src.Particle import Particle
from src.Tilemap import Tilemap


class Player(Entity):
    def __init__(
        self,
        assets: dict[str, Any],
        particles: list[Particle],
        position: Vec2,
        size: Vec2,
    ) -> None:
        super().__init__(assets, "player", position, size)
        self._particles = particles
        self._air_time = 0
        self._jumps = 1
        self._wall_slide = False
        self._dashing = 0
        self._dead = False

    def set_position(self, position: Vec2) -> None:
        self._position = position
        self._dead = False
        self._air_time = 0

    def update(self, tilemap: Tilemap, movement: Vec2 = Vec2(0, 0)) -> None:
        super().update(tilemap, movement)

        if self._velocity.x > 0:
            self._velocity.x = max(self._velocity.x - 0.1, 0)
        elif self._velocity.x < 0:
            self._velocity.x = min(self._velocity.x + 0.1, 0)

        self._air_time += 1

        if self._air_time > 120:
            self._dead = True

        if self._collisions["down"]:
            self._air_time = 0
            self._jumps = 1

        self._wall_slide = False

        if self._air_time > 4:
            if self._collisions["right"] or self._collisions["left"]:
                self._wall_slide = True
                self._flip = self._collisions["left"]
                self._velocity.y = min(self._velocity.y, 0.5)
                self._set_action("wall_slide")
            else:
                self._set_action("jump")
        elif movement.x != 0:
            self._set_action("run")
        else:
            self._set_action("idle")

        if self._dashing == 60 or self._dashing == 50:
            for _ in range(20):
                self._particles.append(self._get_dash_particle())

        if self._dashing > 0:
            self._dashing -= 1

        if self._dashing > 50:
            self._velocity.x = 8 * (-1 if self._flip else 1)
            if self._dashing == 51:
                self._velocity.x *= 0.1

            self._particles.append(self._get_trace_particle())

    def render(self, display: Surface, offset: Vec2 = Vec2(0, 0)) -> None:
        if self._dashing <= 50:
            return super().render(display, offset)

    def _get_dash_particle(self) -> Particle:
        angle = random.random() * math.pi * 2
        speed = random.random() * 0.5 + 0.5

        return Particle(
            self._assets,
            "particle",
            position=Vec2(self.rect.center),
            velocity=Vec2(math.cos(angle) * speed, math.sin(angle) * speed),
            frame=random.randint(0, 3),
        )

    def _get_trace_particle(self) -> Particle:
        speed = random.random() * 3

        return Particle(
            self._assets,
            "particle",
            position=Vec2(self.rect.center),
            velocity=Vec2(speed * (-1 if self._flip else 1), 0),
            frame=random.randint(0, 3),
        )

    def jump(self) -> None:
        if self._wall_slide:
            if self._flip and self._last_movement.x < 0:
                self._velocity.x = 3.5
            elif not self._flip and self._last_movement.x > 0:
                self._velocity.x = -3.5
            self._velocity.y = -2.5
            self._jumps = max(self._jumps - 1, 0)
        elif self._jumps > 0:
            self._velocity.y = -3
            self._jumps -= 1

    def dash(self) -> None:
        if self._dashing == 0:
            self._dashing = 60

    @property
    def is_dashing(self) -> bool:
        return self._dashing >= 50

    @property
    def is_dead(self) -> bool:
        return self._dead
