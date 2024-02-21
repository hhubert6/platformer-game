from __future__ import annotations

import pygame


class Animation:
    def __init__(
        self, images: list[pygame.Surface], duration: int = 5, loop=True
    ) -> None:
        self._images = images
        self._duration = duration
        self._loop = loop
        self._done = False
        self._frames = 0

    def img(self) -> pygame.Surface:
        return self._images[int(self._frames / self._duration)]

    def update(self) -> None:
        if self._loop:
            self._frames = (self._frames + 1) % (self._duration * len(self._images))
        else:
            self._frames = min(self._frames + 1, self._duration * len(self._images) - 1)
            if self._frames >= self._duration * len(self._images) - 1:
                self._done = True

    def copy(self) -> Animation:
        return Animation(self._images, self._duration)
