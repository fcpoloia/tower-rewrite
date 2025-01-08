import json
from threading import Timer
import pygame
from lib import Enemies
from lib.HUD import ProgressBar
from lib.Player import Player
import constants

# Initialize components and constants
pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Tower")
clock = pygame.time.Clock()
FPS = 60
BG = (60, 56, 54)

# Player initialization
bulletGroup = pygame.sprite.Group()
player = Player(constants.center, bulletGroup, constants.PBaseDamage)
playerGroup = pygame.sprite.Group()
RealoadBar = ProgressBar(
    screen,
    (constants.WIDTH // 2 - 50, constants.HEIGHT // 2 + 10),
    (100, 20),
    (255, 255, 255),
    (0, 0, 0),
    player.BReload,
)
playerGroup.add(player)
enemyGroup = pygame.sprite.Group()


def SpawnEnemies():
    global enemyGroup
    global enemySpawTimer
    enemy = Enemies.Dummy("img/PlayerImage.png", 2, 5)
    enemyGroup.add(enemy)
    enemySpawTimer = Timer(constants.SpawnIntervalSec, SpawnEnemies)
    enemySpawTimer.start()


enemySpawTimer = Timer(constants.SpawnIntervalSec, SpawnEnemies)
enemySpawTimer.start()


# Load options files
def default():
    print("Key not bound")


def quit():
    global running
    enemySpawTimer.cancel()
    running = False


def loadInputMap(path):
    with open(path, "r") as f:
        raw_file = json.load(f)

    K_Map = {}
    F_Map = {
        "shoot": player.shoot,
        "quit": quit,
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

    enemiesShot = pygame.sprite.groupcollide(enemyGroup, bulletGroup, False, True)
    for e in enemiesShot:
        for b in enemiesShot[e]:
            e.HP -= b.DMG
            print(e.HP)
            if e.HP <= 0:
                enemyGroup.remove(e)

    screen.fill(BG)

    RealoadBar.draw(player.BReload - player.BReloadCur)

    playerGroup.update(mousePos)
    playerGroup.draw(screen)

    bulletGroup.update()
    bulletGroup.draw(screen)

    enemyGroup.update()
    enemyGroup.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Exit
enemySpawTimer.cancel()
pygame.quit()
