import json
from threading import Timer
import pygame
from lib import Enemies
from lib.HUD import ProgressBar, Button
from lib.Player import Player
import constants
import random

# Initialize components and constants
pygame.init()
pygame.display.set_caption("Tower")
clock = pygame.time.Clock()
FPS = 60
BG = (60, 56, 54)

# Player initialization
bulletGroup = pygame.sprite.Group()
player = Player(constants.center, bulletGroup, constants.PBaseDamage, 100)
playerGroup = pygame.sprite.Group()
RealoadBar = ProgressBar(
    constants.screen,
    (constants.WIDTH // 2 - 50, constants.HEIGHT // 2 + 40),
    (100, 20),
    (255, 255, 255),
    (0, 0, 0),
    player.BReload,
)
HPBar = ProgressBar(
    constants.screen,
    (constants.WIDTH // 2 - 50, constants.HEIGHT // 2 + 60),
    (100, 20),
    (0, 0, 0),
    (0, 255, 0),
    player.PHealthMax,
)
playerGroup.add(player)
enemyGroup = pygame.sprite.Group()


def SpawnEnemies():
    global enemyGroup
    global enemySpawTimer
    initPos = (0, 0)
    side = random.choice(constants.sides)
    if side == "horizontal":
        initPos = (
            random.choice([0, constants.WIDTH]),
            random.randint(0, constants.HEIGHT),
        )
    else:
        initPos = (
            random.randint(0, constants.WIDTH),
            random.choice([0, constants.HEIGHT]),
        )
    enemy = Enemies.Fodder(initPos)
    enemyGroup.add(enemy)
    enemySpawTimer = Timer(constants.SpawnIntervalSec, SpawnEnemies)
    enemySpawTimer.start()


enemySpawTimer = Timer(constants.SpawnIntervalSec, SpawnEnemies)


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


# Add this function after the sprite group declarations
def isOffScreen(sprite):
    return (
        sprite.rect.right < 0
        or sprite.rect.left > constants.WIDTH
        or sprite.rect.bottom < 0
        or sprite.rect.top > constants.HEIGHT
    )


# Main Menu HUD
def switchStateGame():
    global state
    global enemySpawTimer
    enemySpawTimer.start()
    state = "game"


PlayButton = Button("img/PlayButton.png", switchStateGame, (50, 50), (300, 150))
QuitButton = Button("img/QuitButton.png", quit, (50, 210), (300, 150))
buttons = pygame.sprite.Group()
buttons.add(PlayButton)
buttons.add(QuitButton)


# Game States
def menu():
    global mousePos
    global mouseDown
    constants.screen.fill(BG)
    # Draw menu here
    constants.screen.blit(PlayButton.image, PlayButton.rect)
    constants.screen.blit(QuitButton.image, QuitButton.rect)
    for button in buttons:
        if button.rect.collidepoint(mousePos) and mouseDown:
            button.action()


def game():
    # Collision detection
    enemiesShot = pygame.sprite.groupcollide(enemyGroup, bulletGroup, False, True)
    for e in enemiesShot:
        for b in enemiesShot[e]:
            e.HP -= b.DMG
            if e.HP <= 0:
                e.kill()

    playerHit = pygame.sprite.groupcollide(playerGroup, enemyGroup, False, True)
    if playerHit:
        player.PHealth -= len(playerHit)
        print(player.PHealth)

    # Remove off-screen bullets
    for bullet in bulletGroup:
        if isOffScreen(bullet):
            bullet.kill()

    # Remove off-screen enemies
    for enemy in enemyGroup:
        if isOffScreen(enemy):
            enemy.kill()

    constants.screen.fill(BG)

    RealoadBar.draw(player.BReload - player.BReloadCur)
    HPBar.draw(player.PHealth)

    playerGroup.update(mousePos)

    bulletGroup.update()
    bulletGroup.draw(constants.screen)

    enemyGroup.update()
    enemyGroup.draw(constants.screen)


StateMap = {
    "menu": menu,
    "game": game,
}

mousePos = (0, 0)
mouseDown = False
# Main Loop
running = True
state = "menu"
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseDown = True

    StateMap[state]()

    pygame.display.flip()
    clock.tick(FPS)

# Exit
enemySpawTimer.cancel()
pygame.quit()
