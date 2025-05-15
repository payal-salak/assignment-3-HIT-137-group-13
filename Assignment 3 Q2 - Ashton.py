import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HIT137 Assignment 3 Question 2")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GREEN = (160, 238, 160)
LIGHT_BLUE = (0, 180, 238)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)

clock = pygame.time.Clock()
FPS = 60

#TODO: Create boss size
PLAYER_SIZE = (50, 60)
ENEMY_SIZE = (50, 60)
PROJECTILE_SIZE = (10, 5)
COLLECTIBLE_SIZE = (20, 20)

score = 0
level = 1
level_start_time = None
show_level_text = False
level_banner_text = ""

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(GREEN)
        self.base_colour = GREEN
        self.flash_colour = LIGHT_GREEN
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 50))
        self.speed = 5
        self.jump_speed = -15
        self.vel_y = 0
        self.on_ground = True
        self.health = 100
        self.lives = 3
        self.invulnerable = False
        self.invuln_time = 0
        self.can_shoot = True
        self.last_shot_time = 0
        self.show_reload_bar = False

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Prevent moving off the left side of the screen
        if self.rect.left < 0:
            self.rect.left = 0

        # Gravity
        self.vel_y += 1
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.on_ground = True
            self.vel_y = 0

        # Invulnerability timer
        if self.invulnerable and time.time() - self.invuln_time >= 0.5:
            self.invulnerable = False
            self.image.fill(self.base_colour)

        # Shooting cooldown
        if not self.can_shoot and time.time() - self.last_shot_time >= 0.8:
            self.can_shoot = True
            self.show_reload_bar = False

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_speed
            self.on_ground = False

    def shoot(self):
        if self.can_shoot:
            projectile = Projectile(self.rect.right, self.rect.centery)
            projectiles.add(projectile)
            self.can_shoot = False
            self.last_shot_time = time.time()
            self.show_reload_bar = True

    def take_damage(self, amount):
        if not self.invulnerable:
            self.health -= amount
            self.invulnerable = True
            self.invuln_time = time.time()
            self.image.fill(self.flash_colour)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(PROJECTILE_SIZE)
        self.image.fill(LIGHT_BLUE)
        self.rect = self.image.get_rect(midleft=(x, y))
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

#TODO: Create boss class. Use speed, durability, damage triangle.

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=50):
        super().__init__()
        self.image = pygame.Surface(ENEMY_SIZE)
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

#TODO: Add more collectables, extra life, 0 cooldown shooting, etc
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, kind="health"):
        super().__init__()
        self.image = pygame.Surface(COLLECTIBLE_SIZE)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.kind = kind

player = Player()
player_group = pygame.sprite.Group(player)
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

def spawn_enemies():
    enemy_health = 50 + ((level - 1) // 5) * 10
    for i in range(5 + level):
        enemy = Enemy(WIDTH + i * (random.randint(190,270)), HEIGHT - 109, health=enemy_health)
        enemies.add(enemy)

def spawn_collectibles():
    for i in range(3):
        collectible = Collectible(random.randint(200, WIDTH), HEIGHT - 70)
        collectibles.add(collectible)

spawn_enemies()
spawn_collectibles()

def draw_ui():
    pygame.draw.rect(screen, RED, (10, 10, 100, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, player.health, 20))
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 40))
    screen.blit(score_text, (WIDTH - 150, 10))

    # Draw reload bar
    if player.show_reload_bar:
        pygame.draw.rect(screen, WHITE, (player.rect.centerx - 25, player.rect.top - 10, 50, 5))
        elapsed = min(0.8, time.time() - player.last_shot_time)
        pygame.draw.rect(screen, LIGHT_BLUE, (player.rect.centerx - 25, player.rect.top - 10, int(50 * (elapsed / 0.8)), 5))

def draw_level_text():
    text = large_font.render(level_banner_text, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

def game_over_screen():
    screen.fill(BLACK)
    msg = font.render("Game Over! Press R to Restart", True, WHITE)
    info = font.render(f"Final Level: {level}    Final Score: {score}", True, WHITE)
    screen.blit(msg, (WIDTH // 2 - 150, HEIGHT // 2))
    screen.blit(info, (WIDTH // 2 - 150, HEIGHT // 2 + 40))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

running = True
while running:
    clock.tick(FPS)
    screen.fill((50, 50, 100))

    if show_level_text:
        draw_level_text()
        pygame.display.flip()
        if time.time() - level_start_time >= 3:
            show_level_text = False
        continue

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_z:
                player.shoot()

    player_group.update(keys)
    projectiles.update()
    enemies.update()

    # Projectile/Enemy Hits
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, False)
    for projectile, hit_enemies in hits.items():
        for enemy in hit_enemies:
            enemy.health -= 25
            if enemy.health <= 0:
                enemy.kill()
                score += 25

    #Projectile/Pickup hits
    pickup_hits = pygame.sprite.groupcollide(projectiles, collectibles, True, True)

    # Pickup effects
    for collectible in pygame.sprite.spritecollide(player, collectibles, True):
        if collectible.kind == "health":
            player.health = min(100, player.health + 10)

    # Scaling damage
    for enemy in pygame.sprite.spritecollide(player, enemies, True):
        damage = 15 + ((level - 1) // 5) * 10
        player.take_damage(damage)

    # Lost life, game over, and reset
    if player.health <= 0:
        player.lives -= 1
        player.health = 100
        score = max(0, score - 50)
        if player.lives <= 0:
            game_over_screen()
            player.lives = 3
            player.health = 100
            score = 0
            level = 1
        enemies.empty()
        collectibles.empty()
        spawn_enemies()
        spawn_collectibles()
        player.rect.x = 100
        if player.lives < 3: # Prevents this screen on game restart
            level_banner_text = f"Level {level} - You lost a life and 50 points."
            level_start_time = time.time()
        show_level_text = True

    # Level progression
    if player.rect.right >= WIDTH:
        level += 1
        player.rect.left = 0
        enemies.empty()
        collectibles.empty()
        spawn_enemies()
        spawn_collectibles()
        if level % 5 == 0:
            level_banner_text = f"Level {level} - The enemies' strength increases"
        else:
            level_banner_text = f"Level {level}"
        level_start_time = time.time()
        show_level_text = True

    player_group.draw(screen)
    projectiles.draw(screen)
    enemies.draw(screen)
    collectibles.draw(screen)
    draw_ui()

    pygame.display.flip()

pygame.quit()