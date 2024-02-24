import pygame
from pygame import Vector2 as Vec2

from src.Animation import Animation


class Particle:
    def __init__(
        self,
        assets: dict,
        type: str,
        position: Vec2,
        velocity: Vec2 = Vec2(0, 0),
        frame=0,
    ) -> None:
        self.type = type
        self.position = position
        self._velocity = velocity
        self._animation: Animation = assets["particle/" + type].copy()
        self._animation._frame = frame

    def update(self) -> bool:
        self.position += self._velocity
        self._animation.update()
        return self._animation.done

    def render(self, display: pygame.Surface, offset: Vec2) -> None:
        img = self._animation.img()
        display.blit(
            img,
            self.position - offset - Vec2(img.get_size()) // 2,
        )

    @property
    def animation_frame(self) -> int:
        return self._animation._frame
