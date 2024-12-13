import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self, pos: tuple[int, int], mpos: tuple[int, int], speed: float
    ) -> None:
        super().__init__()
        self.image_original = pygame.image.load("img/BulletImage.png")
        self.image_original = pygame.transform.scale(self.image_original, (10, 20))
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.CenterVector = pygame.math.Vector2(self.rect.center)

        self.SPEED = speed

        # Rotate
        dx = mpos[0] - self.rect.centerx
        dy = mpos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image_original, (angle - 90))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.dirVector = pygame.Vector2(dx, dy).normalize()

    def update(self):
        self.CenterVector += self.dirVector * self.SPEED
        self.rect.centerx = round(self.CenterVector.x)
        self.rect.centery = round(self.CenterVector.y)
