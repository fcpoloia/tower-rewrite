import pygame
from typing import Callable


class ProgressBar:
    def __init__(
        self,
        surface: pygame.SurfaceType,
        pos: tuple[int, int],
        dims: tuple[int, int],
        bg: tuple[int, int, int],
        fg: tuple[int, int, int],
        maxVal: int,
    ) -> None:
        self.screen = surface
        self.POSITION = pos  # 0-x 1-y
        self.DIMENSIONS = dims  # 0-width 1-height
        self.bg = bg
        self.fg = fg
        self.val = 0  # Placeholder
        self.maxVal = maxVal
        self.progressWidth = (self.val / self.maxVal) * self.DIMENSIONS[0]

        # Two rectangles
        self.bgRect = (
            self.POSITION[0],
            self.POSITION[1],
            self.DIMENSIONS[0],
            self.DIMENSIONS[1],
        )
        self.fgRect = (
            self.POSITION[0],
            self.POSITION[1],
            self.progressWidth,
            self.DIMENSIONS[1],
        )

    def update(self, val: int):
        self.val = val
        self.progressWidth = (self.val / self.maxVal) * self.DIMENSIONS[0]
        self.bgRect = (
            self.POSITION[0],
            self.POSITION[1],
            self.DIMENSIONS[0],
            self.DIMENSIONS[1],
        )
        self.fgRect = (
            self.POSITION[0],
            self.POSITION[1],
            self.progressWidth,
            self.DIMENSIONS[1],
        )

    def draw(self, val: int):
        self.update(val)
        # Background
        pygame.draw.rect(
            self.screen,
            self.bg,
            self.bgRect,
        )
        # Foreground
        pygame.draw.rect(
            self.screen,
            self.fg,
            self.fgRect,
        )


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        path: str,
        action: Callable,
        pos: tuple[int, int],
        dims: tuple[int, int],
    ) -> None:
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, dims)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.action = action
