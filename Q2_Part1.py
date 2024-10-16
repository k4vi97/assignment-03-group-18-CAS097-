# game_objects.py

import pygame
import random

# Game constants
WIDTH = 800  # Screen width
HEIGHT = 600  # Screen height
PLAYER_SPEED = 5  # Speed at which the player moves
PROJECTILE_SPEED = 7  # Speed of projectiles shot by the player
INITIAL_ENEMY_SPEED = 3  # Initial speed of the enemy tanks

# Colors
WHITE = (255, 255, 255)  # Background color
BLACK = (0, 0, 0)  # Default text color
GREEN = (0, 255, 0)  # Health bar color when health is full
RED = (255, 0, 0)  # Health bar color when health is low

# Player class handles player-specific attributes and behaviors
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("man.png")  # Load player image
        self.rect = self.image.get_rect()  # Get the rectangle boundary of the image
        self.rect.center = (x, y)  # Position player at the specified x, y coordinates
        self.health = 100  # Initialize player health
        self.lives = 3  # Player starts with 3 lives
        self.speed = PLAYER_SPEED  # Movement speed of player

    # Update method handles player movement
    def update(self):
        keys = pygame.key.get_pressed()  # Get currently pressed keys
        if keys[pygame.K_w] and self.rect.top > 0:  # Move up if within screen boundary
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:  # Move down if within screen boundary
            self.rect.y += self.speed

    # Shoot method creates a new projectile instance
    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)  # Position projectile at player's right side
        return projectile

    # Draw health bar above player sprite
    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 100, 5))  # Background bar (red)
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))  # Foreground bar (green)

# Projectile class for bullets or projectiles shot by the player
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))  # Define a small rectangle as the projectile shape
        self.image.fill(RED)  # Set projectile color to red
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Position projectile at player's shooting location
        self.speed = PROJECTILE_SPEED  # Set projectile movement speed

    # Update method for moving the projectile across the screen
    def update(self):
        self.rect.x += self.speed  # Move projectile to the right
        if self.rect.x > WIDTH:  # Remove projectile if it goes off screen
            self.kill()

# Tank class for enemy tanks
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load("tank.png")  # Load tank image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Position tank at specified x, y coordinates
        self.speed = speed  # Set tank speed based on score
        self.health = 50  # Initialize tank health

    # Update method for moving the tank across the screen
    def update(self):
        self.rect.x -= self.speed  # Move tank to the left
        if self.rect.right < 0:  # Remove tank if it goes off screen
            self.kill()

    # Draw health bar above tank sprite
    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 50, 5))  # Background bar (red)
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))  # Foreground bar (green)

# Function to determine tank speed based on score, making game more difficult over time
def get_tank_speed(score):
    if score >= 5000:
        return 6  # Fastest speed for high scores
    elif score >= 4000:
        return 5  # Faster speed for mid-high scores
    elif score >= 2000:
        return 4  # Moderate speed for mid-level scores
    else:
        return INITIAL_ENEMY_SPEED  # Default speed for low scores

# Function to create a new tank with speed determined by score
def spawn_tank(score):
    tank_speed = get_tank_speed(score)  # Determine speed based on score
    # Position the tank slightly off-screen to the right at a random height
    tank = Tank(WIDTH + 50, random.randint(50, HEIGHT - 50), tank_speed)
    return tank
