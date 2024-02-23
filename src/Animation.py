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
        self._frame = 0

    def img(self) -> pygame.Surface:
        return self._images[int(self._frame / self._duration)]

    def update(self) -> None:
        if self._loop:
            self._frame = (self._frame + 1) % (self._duration * len(self._images))
        else:
            self._frame = min(self._frame + 1, self._duration * len(self._images) - 1)
            if self._frame >= self._duration * len(self._images) - 1:
                self._done = True

    def copy(self) -> Animation:
        return Animation(self._images, self._duration, self._loop)

    @property
    def done(self) -> bool:
        return self._done
