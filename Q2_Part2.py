# game.py

import pygame
import random
from setup import *  # Import everything from setup.py

# Main game loop
score = 0
running = True
spawn_timer = 0  # Timer to control tank spawn rate
health_spawn_timer = 0  # Timer to control health item spawn rate
level_completed_time = 0  # Timer for level completion messages
level_completed_message = ""
boss_spawned = False
win_message = ""
win_time = 0

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Spawn tanks at regular intervals
    if not boss_spawned:
        if spawn_timer <= 0:
            spawn_tank(score)  # Pass current score to adjust tank speed and health
            spawn_timer = 90  # Adjust for tank spawn rate (lower = faster spawning)
        else:
            spawn_timer -= 1

    # Spawn health items randomly
    if health_spawn_timer <= 0 and random.randint(0, HEALTH_ITEM_SPAWN_RATE) == 0:
        spawn_health_item()
        health_spawn_timer = 500  # Adjust for health item spawn rate
    else:
        health_spawn_timer -= 1

    # Update player, projectiles, health items
    player.update()
    projectiles.update()
    health_items.update()

    # Update tanks and check collision with player
    enemies.update()

    # Check collisions between projectiles and tanks
    for projectile in projectiles:
        hits = pygame.sprite.spritecollide(projectile, enemies, False)
        for tank in hits:
            tank.health -= 25  # Reduce tank health when hit by projectile
            projectile.kill()  # Remove projectile on hit
            if tank.health <= 0:
                tank.kill()
                score += 100  # Increase score for each destroyed tank

                # Check if boss is defeated
                if isinstance(tank, Boss):
                    win_message = "You Won!"
                    win_time = pygame.time.get_ticks()  # Record time when message is displayed

    # Check collisions between tanks and the player
    if pygame.sprite.spritecollide(player, enemies, False):
        player.health -= 1  # Reduce player health when tank touches player
        if player.health <= 0:
            running = False  # Game over when player health reaches 0

    # Check if player collects health item
    health_hits = pygame.sprite.spritecollide(player, health_items, True)
    for health_item in health_hits:
        player.increase_health()  # Increase player health when health item is collected

    # Check for level completion messages
    if score >= 1500 and level_completed_message == "":
        level_completed_message = "Level 01 Completed!"
        level_completed_time = pygame.time.get_ticks()
    elif score >= 3000 and level_completed_message == "":
        level_completed_message = "Level 02 Completed!"
        level_completed_time = pygame.time.get_ticks()

    # Close level completion message after reaching required scores
    if score >= 1700 and level_completed_message == "Level 01 Completed!":
        level_completed_message = ""
    if score >= 3200 and level_completed_message == "Level 02 Completed!":
        level_completed_message = ""

    # Check if "You Won!" message should be cleared and close the game
    if win_message:
        if pygame.time.get_ticks() - win_time > 2000:  # Display for 2 seconds
            running = False  # Close the game

    # Check for boss spawn
    if score >= 5000 and not boss_spawned:
        boss_spawned = True  # Stop spawning tanks and spawn boss
        enemies.empty()  # Remove all tanks
        spawn_boss()  # Spawn the boss

    # Drawing and rendering the game screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    player.draw_health_bar(screen)
    for tank in enemies:
        tank.draw_health_bar(screen)

    # Display score
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display level completion message if applicable
    if level_completed_message:
        message_surface = font.render(level_completed_message, True, WHITE)
        screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2))

    # Display win message if applicable
    if win_message:
        win_surface = font.render(win_message, True, WHITE)
        screen.blit(win_surface, (WIDTH // 2 - win_surface.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
