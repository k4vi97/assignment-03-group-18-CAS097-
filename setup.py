# setup.py
 
import pygame
import random
 
# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5
PROJECTILE_SPEED = 7
INITIAL_ENEMY_SPEED = 3 * 1.25  # Normal speed increased by 1.25
BOSS_HEALTH_MULTIPLIER = 2.25  # Boss health multiplier
HEALTH_ITEM_SPAWN_RATE = 500  # Chance to spawn health item
 
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player vs Tanks")
clock = pygame.time.Clock()
 
# Game objects
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
        all_sprites.add(projectile)
        projectiles.add(projectile)
 
    def draw_health_bar(self, screen):
        # Draw health bar for the player
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 100, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))
 
    def increase_health(self):
        self.health = min(100, self.health + 25)  # Increase health by 0.25x (25%)
 
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
    def __init__(self, x, y, speed, health):
        super().__init__()
        self.image = pygame.image.load("tank.png")  # Load tank image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed  # Speed of the tank
        self.health = health  # Tank health
 
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()  # Remove tank if it goes off the left side of the screen
 
    def draw_health_bar(self, screen):
        # Draw health bar for the tank
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 50, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))
 
class Boss(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, INITIAL_ENEMY_SPEED, 50 * BOSS_HEALTH_MULTIPLIER)
        self.image = pygame.image.load("boss.png")  # Load boss image
        self.direction = random.choice([-1, 1])
 
    def update(self):
        self.rect.x -= self.speed
        self.rect.y += self.direction * random.randint(1, 5)  # Move up or down randomly
        if self.rect.y <= 0 or self.rect.bottom >= HEIGHT:
            self.direction *= -1  # Reverse direction if it hits screen boundaries
        if self.rect.right < 0:
            self.kill()
 
class HealthItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("health.png")  # Load health item image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
    def update(self):
        self.rect.x -= 3  # Slowly move the health item to the left
        if self.rect.right < 0:
            self.kill()
 
# Create game objects
all_sprites = pygame.sprite.Group()
player = Player(50, HEIGHT // 2)  # Player starts on the left
all_sprites.add(player)
 
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
health_items = pygame.sprite.Group()
 
# Tank speed and health based on score
def get_tank_speed(score):
    if score >= 5000:
        return 6  # Fastest speed
    elif score >= 4000:
        return 5  # Faster speed
    elif score >= 2300:
        return INITIAL_ENEMY_SPEED * 2  # Double speed
    elif score >= 2000:
        return 4  # Fast speed
    else:
        return INITIAL_ENEMY_SPEED  # Default speed
 
def get_tank_health(score):
    if score >= 3000:
        return 50 * 1.75  # 1.75x health after score 3000
    elif score >= 1500:
        return 50 * 1.5  # 1.5x health after score 1500
    else:
        return 50  # Normal health
 
def spawn_tank(score):
    tank_speed = get_tank_speed(score)
    tank_health = get_tank_health(score)
    tank = Tank(WIDTH + 50, random.randint(50, HEIGHT - 50), tank_speed, tank_health)  # Tanks spawn off the right side
    all_sprites.add(tank)
    enemies.add(tank)
 
def spawn_boss():
    boss = Boss(WIDTH + 50, HEIGHT // 2)  # Boss spawns at the center
    all_sprites.add(boss)
    enemies.add(boss)
 
def spawn_health_item():
    health_item = HealthItem(WIDTH + 50, random.randint(50, HEIGHT - 50))  # Health item spawns randomly
    all_sprites.add(health_item)
    health_items.add(health_item)