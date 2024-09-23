import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

bg = pygame.image.load('bg.png')

#PLAYER

playerImg = pygame.image.load('rocket.png')
playerX = 340
playerY = 500
playerX_change = 0

#ENEMY
enemyImgs = []
enemyXs = []
enemyYs = []
enemyX_changes = []
enemyY_changes = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg = pygame.image.load('ufo.png')
    enemyX = random.randint(0, 745)
    enemyY = random.randint(50, 150)
    enemyX_change = 4
    enemyY_change = 40
    enemyImgs.append(enemyImg)
    enemyXs.append(enemyX)
    enemyYs.append(enemyY)
    enemyX_changes.append(enemyX_change)
    enemyY_changes.append(enemyY_change)

#BULLET
bullet = pygame.image.load('paintball.png')
bulletX = 0
bulletY = 495
bulletY_change = 10
bullet_state = "ready"

#SCORE
score=0
font  = pygame.font.Font('freesansbold.ttf', 32)

textX=10
textY=10

#BACKGROUND MUSIC and SOUND
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound('laser.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')

def show_score(x, y):
    score_display = font.render("Score: " + str(score), True, (250, 200, 0))
    screen.blit(score_display, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    if bullet_state == "fire":
        screen.blit(bullet, (x + 20, y -5))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** 0.5
    if distance < 27:
        return True
    else:
        return False

running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_KP0):
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound.play()
                    bullet_state = "fire"
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0           
   
    playerX += playerX_change
    if playerX <=0:
        playerX = 0 
    elif playerX >= 735:
        playerX = 735 
    player(playerX, playerY)

    for i in range(num_of_enemies):
        if enemyYs[i] >= 480:
            for j in range(num_of_enemies):
                enemyYs[j] = 2000
            game_over = pygame.font.Font('freesansbold.ttf', 64).render("GAME OVER", True, (250, 200, 0))
            screen.blit(game_over, (200, 250))
            break
        enemyXs[i] += enemyX_changes[i]
        if enemyXs[i] <=0:
            enemyX_changes[i] = 2
            enemyYs[i] += enemyY_changes[i]
        elif enemyXs[i] >= 735:
            enemyX_changes[i] = -2
            enemyYs[i] += enemyY_changes[i]
        collision = isCollision(enemyXs[i], enemyYs[i], bulletX, bulletY)
        if collision:
            bulletY = 495
            bullet_state = "ready"
            enemyXs[i] = random.randint(0, 745)
            enemyYs[i] = random.randint(50, 150)
            score+=1
            explosion_sound.play()
        show_score(textX, textY)
        enemy(enemyXs[i], enemyYs[i])

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 20:
        bulletY = 495
        bullet_state = "ready"
    
    pygame.display.update()