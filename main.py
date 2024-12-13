import pygame
from lib.Player import Player

# Initialize components and constants
WIDHT = 1000
HEIGHT = 700
pygame.init()
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Tower")
clock = pygame.time.Clock()
FPS = 60
BG = (60, 56, 54)

# Player initialization
player = Player()
playerGroup = pygame.sprite.Group()
playerGroup.add(player)

# Main Loop
running = True
while running:
    # Event/Input loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG)    
    playerGroup.update()
    playerGroup.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Exit
pygame.quit()
