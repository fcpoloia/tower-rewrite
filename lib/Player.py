import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__()
        self.image_original = pygame.image.load("img/PlayerImage.png")
        self.image_original = pygame.transform.scale(self.image_original, (50, 50))
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def rotate(self, mpos: tuple):
        dx = mpos[0] - self.rect.centerx
        dy = mpos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image_original, (angle - 90))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, mpos: tuple) -> None:
        self.rotate(mpos)
