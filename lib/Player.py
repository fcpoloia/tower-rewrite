import pygame
import math
import constants

from lib.Bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        bulletGroup: pygame.sprite.Group,
        damage: int,
        health: int,
    ) -> None:
        super().__init__()
        self.image_base = pygame.image.load("img/PlayerBase.png")
        self.image_base = pygame.transform.scale(self.image_base, (80, 80))
        self.image_turret_original = pygame.image.load("img/PlayerImage.png")
        self.image_turret_original = pygame.transform.scale(
            self.image_turret_original, (100, 100)
        )
        self.image_turret = self.image_turret_original
        self.rect = self.image_base.get_rect()
        self.rect.center = pos
        self.original_pos = self.rect.topleft

        self.BSpeed = 5
        self.BReload = 120  # Number of frames
        self.BReloadCur = 0
        self.BDamage = damage

        self.PHealth = health
        self.PHealthMax = health

        # Imported
        self.mpos = (0, 0)
        self.BGroup = bulletGroup

    def shoot(self):
        if self.BReloadCur <= 0:
            self.BGroup.add(
                Bullet(self.rect.center, self.mpos, self.BSpeed, self.BDamage)
            )
            self.BReloadCur = self.BReload

    def rotate(self):
        dx = self.mpos[0] - self.rect.centerx
        dy = self.mpos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        self.image_turret = pygame.transform.rotate(
            self.image_turret_original, (angle - 180)
        )
        self.rect = self.image_turret.get_rect(center=self.rect.center)

    def update(self, mpos: tuple) -> None:
        """
        UPDATE variables and state of the player

        mpos - mouse position, it's better to keep it in `self` than for every function to need it as argument
        BReloadCur - current state of reload counter. Measured in frames
        """
        self.mpos = mpos
        if self.BReloadCur > 0:
            self.BReloadCur -= 1
        self.rotate()
        self.draw(constants.screen)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image_base, self.original_pos)
        surface.blit(self.image_turret, self.rect.topleft)
