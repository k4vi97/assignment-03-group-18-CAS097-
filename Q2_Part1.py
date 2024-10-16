import pygame
import random
 
# Game constants
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 5
PROJECTILE_SPEED = 7
INITIAL_ENEMY_SPEED = 3  # Initial speed of the tanks
 
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("man.png")  # Load player image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health = 100  # Player health
        self.lives = 3
        self.speed = PLAYER_SPEED
 
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 0:  # Move up
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:  # Move down
            self.rect.y += self.speed
 
    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)
        return projectile
 
    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 100, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))
 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = PROJECTILE_SPEED
 
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()
 
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load("tank.png")  # Load tank image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed  # Speed of the tank
        self.health = 50  # Tank health
 
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()  # Remove tank if it goes off the left side of the screen
 
    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 50, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))
 
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("boss.png")  # Load boss image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2  # Boss moves slower than tanks
        self.health = 100  # Boss health is double that of a normal tank
 
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()  # Remove boss if it goes off the left side of the screen
 
    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 100, 5))  # Boss health bar is larger
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))
 
def get_tank_speed(score):
    if score >= 5000:
        return 6  # Fastest speed
    elif score >= 4000:
        return 5  # Faster speed
    elif score >= 2000:
        return 4  # Fast speed
    else:
        return INITIAL_ENEMY_SPEED  # Default speed
 
def spawn_tank(score):
    tank_speed = get_tank_speed(score)  # Determine speed based on score
    tank = Tank(WIDTH + 50, random.randint(50, HEIGHT - 50), tank_speed)  # Tanks spawn off the right side
    return tank