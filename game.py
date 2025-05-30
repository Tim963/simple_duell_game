import pygame
import sys
import random

# Initialisierung
pygame.init()

# Bildschirmdimensionen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Titel des Spiels
pygame.display.set_caption("1vs1 Duel")

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Spieler 1 (Rot)
player1 = pygame.Rect(100, 300, 30, 30)
player1_lives = 5
player1_cooldown = 0
player1_weapon = "pistol"
player1_bullet_speed = 7
player1_bullets_per_shot = 1

# Spieler 2 (Blau)
player2 = pygame.Rect(670, 300, 30, 30)
player2_lives = 5
player2_cooldown = 0
player2_weapon = "pistol"
player2_bullet_speed = 7
player2_bullets_per_shot = 1

# Geschwindigkeit
speed = 5

# Bullet-Liste
bullets = []

# Waffen
weapons = []
weapon_spawner = 0

# Leben
health_packs = []
health_spawner = 0

# Spielsschrift
font = pygame.font.Font(None, 74)

# Spiel über
game_over = False

# Waffentypen
weapon_types = [
    {"name": "machinegun", "color": MAGENTA, "speed": 10, "bullets": 1},
    {"name": "shotgun", "color": YELLOW, "speed": 5, "bullets": 5},
    {"name": "sniper", "color": CYAN, "speed": 15, "bullets": 1},
    {"name": "rocket", "color": RED, "speed": 3, "bullets": 1}
]

# Spiel-Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player1_cooldown <= 0:
                for _ in range(player1_bullets_per_shot):
                    spread = 0
                    if player1_weapon == "shotgun":
                        spread = random.uniform(-5, 5)
                    bullets.append([
                        player1.x + player1.width,
                        player1.y + player1.height // 2 + spread,
                        1,
                        player1_bullet_speed
                    ])
                player1_cooldown = 10
            if event.key == pygame.K_RETURN and player2_cooldown <= 0:
                for _ in range(player2_bullets_per_shot):
                    spread = 0
                    if player2_weapon == "shotgun":
                        spread = random.uniform(-5, 5)
                    bullets.append([
                        player2.x,
                        player2.y + player2.height // 2 + spread,
                        -1,
                        player2_bullet_speed
                    ])
                player2_cooldown = 10

    # Hintergrund
    screen.fill((0, 0, 0))

    # Spieler Aktionen
    keys = pygame.key.get_pressed()

    # Spieler 1 Steuerung (WASD)
    if keys[pygame.K_w]:
        player1.y -= speed
    if keys[pygame.K_s]:
        player1.y += speed
    if keys[pygame.K_a]:
        player1.x -= speed
    if keys[pygame.K_d]:
        player1.x += speed

    # Spieler 2 Steuerung (Pfeiltasten)
    if keys[pygame.K_UP]:
        player2.y -= speed
    if keys[pygame.K_DOWN]:
        player2.y += speed
    if keys[pygame.K_LEFT]:
        player2.x -= speed
    if keys[pygame.K_RIGHT]:
        player2.x += speed

    # reduce cooldown
    if player1_cooldown > 0:
        player1_cooldown -= 1
    if player2_cooldown > 0:
        player2_cooldown -= 1

    # Waffen und Leben spawnen
    weapon_spawner += 1
    if weapon_spawner >= 600:  # Alle 10 Sekunden
        weapon = random.choice(weapon_types)
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        weapons.append({"type": weapon, "rect": pygame.Rect(x, y, 20, 20)})
        weapon_spawner = 0

    health_spawner += 1
    if health_spawner >= 900:  # Alle 15 Sekunden
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        health_packs.append({"rect": pygame.Rect(x, y, 15, 15), "timer": 0})
        health_spawner = 0

    # <uint player1
    pygame.draw.rect(screen, RED, player1)
    # uint player2
    pygame.draw.rect(screen, BLUE, player2)

    # Bullets
    for bullet in bullets:
        if bullet[2] == 1:
            bullet[0] += bullet[3]
        else:
            bullet[0] -= bullet[3]

        # Überprüfe Treffer
        if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH:
            bullets.remove(bullet)
            continue

        bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1] - 2, 4, 4)
        if bullet_rect.colliderect(player1) or bullet_rect.colliderect(player2):
            if bullet[2] == 1:
                player2_lives -= 1
            else:
                player1_lives -= 1
            bullets.remove(bullet)

        pygame.draw.rect(screen, WHITE, (bullet[0] - 2, bullet[1] - 2, 4, 4))

    # Waffen
    for weapon in weapons:
        pygame.draw.rect(screen, weapon["type"]["color"], weapon["rect"])
        if weapon["rect"].colliderect(player1):
            player1_weapon = weapon["type"]["name"]
            player1_bullet_speed = weapon["type"]["speed"]
            player1_bullets_per_shot = weapon["type"]["bullets"]
            weapons.remove(weapon)
        if weapon["rect"].colliderect(player2):
            player2_weapon = weapon["type"]["name"]
            player2_bullet_speed = weapon["type"]["speed"]
            player2_bullets_per_shot = weapon["type"]["bullets"]
            weapons.remove(weapon)

    # Lebenspakete
    for health in health_packs:
        pygame.draw.rect(screen, GREEN, health["rect"])
        health["timer"] += 1
        if health["rect"].colliderect(player1):
            player1_lives += 1
            health_packs.remove(health)
        if health["rect"].colliderect(player2):
            player2_lives += 1
            health_packs.remove(health)
        if health["timer"] >= 600:  # 10 Sekunden
            health_packs.remove(health)

    # Lebensanzeige
    lives_text = font.render(f"{player1_lives} - {player2_lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH // 2 - lives_text.get_width() // 2, 20))

    # Waffenanzeige
    weapon1_text = font.render(player1_weapon, True, WHITE)
    screen.blit(weapon1_text, (player1.x, player1.y - 20))
    weapon2_text = font.render(player2_weapon, True, WHITE)
    screen.blit(weapon2_text, (player2.x, player2.y - 20))

    # Überprüfe auf Spielende
    if player1_lives <= 0:
        game_over = True
    if player2_lives <= 0:
        game_over = True

    if game_over:
        game_over_text = font.render(f"Game Over!", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
        if keys[pygame.K_r]:
            player1_lives = 5
            player2_lives = 5
            player1_weapon = "pistol"
            player1_bullet_speed = 7
            player1_bullets_per_shot = 1
            player2_weapon = "pistol"
            player2_bullet_speed = 7
            player2_bullets_per_shot = 1
            game_over = False

    # aktualisiere den Bildschirm
    pygame.display.flip()
    pygame.time.Clock().tick(60)
