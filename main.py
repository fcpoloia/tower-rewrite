import pygame

#Initialize components and constants
WIDHT = 1000
HEIGHT = 700
pygame.init()
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Tower")
clock = pygame.time.Clock()
FPS = 60
BG = (60, 56, 54)

#Main Loop
running = True
while running:
    #Event/Input loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG)
    pygame.display.flip()
    clock.tick(FPS)

#Exit
pygame.quit()
