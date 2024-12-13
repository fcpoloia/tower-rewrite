import json
import sys
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
bulletGroup = pygame.sprite.Group()
player = Player((WIDHT // 2, HEIGHT // 2), bulletGroup)
playerGroup = pygame.sprite.Group()
playerGroup.add(player)


# Load options files
def default():
    print("Key not bound")


def loadInputMap(path):
    with open(path, "r") as f:
        raw_file = json.load(f)

    K_Map = {}
    F_Map = {
        "shoot": player.shoot,
        "quit": sys.exit,
    }
    for key, action in raw_file.items():
        K_Map[getattr(pygame, key)] = F_Map.get(action, default)
    return K_Map


configKeyMap = loadInputMap("options/keymaps.json")

# Main Loop
running = True
while running:
    # Event/Input loop
    mouseX, mouseY = pygame.mouse.get_pos()
    mousePos = (mouseX, mouseY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            action = configKeyMap.get(event.key, default)
            action()

    screen.fill(BG)
    playerGroup.update(mousePos)
    playerGroup.draw(screen)

    bulletGroup.update()
    bulletGroup.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Exit
pygame.quit()
