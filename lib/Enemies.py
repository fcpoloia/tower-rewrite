import pygame
import constants
import lib.HUD as HUD


class Dummy(pygame.sprite.Sprite):
    """
    This is a base class for all enemies

    PARAMS
    path - A path to sprite's image
    speed - number of pixel that a sprite will travel in one frame
    health - self explenatory
    initPos - a tuple with x and y coordinates of the sprite's initial position
    """

    def __init__(
        self,
        path: str,
        speed: int,
        health: int,
        initPos: tuple[int, int],
    ) -> None:
        super().__init__()

        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = initPos
        self.HPBar = HUD.ProgressBar(
            constants.screen,
            (self.rect.x, self.rect.bottom + 20),
            (self.rect.width, 10),
            (0, 0, 0),
            (255, 0, 0),
            health,
        )
        self.SPEED = speed
        self.HP = health

        self.PosVector = pygame.math.Vector2(self.rect.center)
        dx = constants.center[0] - self.rect.centerx
        dy = constants.center[1] - self.rect.centery
        self.dirVector = pygame.Vector2(dx, dy).normalize()

    def update(self):
        self.PosVector += self.dirVector * self.SPEED
        self.rect.centerx = round(self.PosVector.x)
        self.rect.centery = round(self.PosVector.y)
        self.HPBar.POSITION = (self.rect.x, self.rect.bottom + 20)
        self.HPBar.draw(self.HP)
