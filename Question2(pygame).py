# GROUP NAME : CAS/DAN GROUP-13
# GROUP MEMBERS: 389249 PAYAL
#                391075 AMANPARTEEK SINGH
#                390786 ANSHUL
#                361253 ASHTON SEARLE
#                391273 KOMALPREET KAUR

# Importing Required Libraries
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5
JUMP_STRENGTH = 20
GRAVITY = 1
PROJECTILE_SPEED = 15
ENEMY_SPEED_BASE = 2
COLLECTIBLE_SIZE = 25
FONT_NAME = pygame.font.match_font('arial')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 70)
BLUE = (50, 130, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARKRED = (139, 0, 0)
GREY = (100, 100, 100)

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animal Hero: Rabbit vs Humans")
clock = pygame.time.Clock()

# Load background image
try:
    background_img = pygame.image.load('images/background.png').convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    background_img = None  # fallback: no background image

# Load sounds (placeholder using Pygame beep substitute)
try:
     shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
     enemy_hit_sound = pygame.mixer.Sound('sounds/hit.wav')
     collectible_sound = pygame.mixer.Sound('sounds/collect.wav')
except:
    shoot_sound = None
    enemy_hit_sound = None
    collectible_sound = None

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def draw_health_bar(surface, x, y, pct, width=100, height=10):
    if pct < 0:
        pct = 0
    fill = (pct / 100) * width
    outline_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/rabbit.png').convert_alpha()  # Load rabbit image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
        self.health = 100
        self.lives = 3
        self.score = 0
        self.is_jumping = False
        self.jump_vel = JUMP_STRENGTH
        self.vel_y = 0
        self.on_ground = True
        self.projectile_cooldown = 0
        self.direction = 1   # 1 = facing right, -1 = facing left

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = 1

        # Jump
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = -JUMP_STRENGTH
            self.on_ground = False

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        dy = self.vel_y

        # Collision with platforms (ground)
        self.rect.x += dx
        self.collide(dx, 0, platforms)
        self.rect.y += dy
        self.collide(0, dy, platforms)

        # Keep player inside screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Cooldown for shooting
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

    def collide(self, dx, dy, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if dx > 0:
                    self.rect.right = p.rect.left
                if dx < 0:
                    self.rect.left = p.rect.right
                if dy > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.vel_y = 0
                if dy < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

    def shoot(self, projectiles_group):
        if self.projectile_cooldown == 0:
            proj = Projectile(self.rect.centerx, self.rect.centery, self.direction)
            projectiles_group.add(proj)
            self.projectile_cooldown = 20  # cooldown frames
            if shoot_sound:
                shoot_sound.play()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((15,5))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = PROJECTILE_SPEED * direction
        self.damage = 25

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100, speed=ENEMY_SPEED_BASE, boss=False):
        super().__init__()
        self.image = pygame.image.load('images/enemy.png').convert_alpha()  # Load human image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.speed = speed
        self.boss = boss

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, kind='health'):
        super().__init__()
        self.kind = kind
        if kind == 'health':
            # Use carrot image instead of colored surface
            try:
                self.image = pygame.image.load('images/carrot1.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (60, 60))
            except:
                self.image = pygame.Surface((60, 60))
                self.image.fill(BLUE)
        elif kind == 'life':
            self.image = pygame.Surface((COLLECTIBLE_SIZE, COLLECTIBLE_SIZE))
            self.image.fill(YELLOW)
        else:
            self.image = pygame.Surface((COLLECTIBLE_SIZE, COLLECTIBLE_SIZE))
            self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def game_over_screen(screen, score):
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH//2, SCREEN_HEIGHT//4, RED)
    draw_text(screen, f"Score: {score}", 36, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, WHITE)
    draw_text(screen, "Press R to Restart or Q to Quit", 24, SCREEN_WIDTH//2, SCREEN_HEIGHT * 3//4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    # Groups
    player_group = pygame.sprite.Group()
    projectiles_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    collectibles_group = pygame.sprite.Group()
    platforms_group = pygame.sprite.Group()

    # Create ground platform
    ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
    platforms_group.add(ground)

    # Player
    player = Player(100, SCREEN_HEIGHT - 100)
    player_group.add(player)

    level = 1
    spawn_counter = 0
    collectible_counter = 0
    enemy_freq = 90  # frames
    running = True
    boss_defeated = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Shoot projectile on key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    player.shoot(projectiles_group)

        # Spawn enemies periodically increasing difficulty per level
        spawn_counter += 1
        if spawn_counter >= max(30, enemy_freq - level * 15):
            spawn_counter = 0
            # Create normal enemies for levels 1 and 2
            if level < 3:
                e = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT - 100, health=50 + level*20,speed=ENEMY_SPEED_BASE + level)
                enemies_group.add(e)
            else:
                # Level 3: spawn boss once only
                if not boss_defeated and len(enemies_group) == 0:
                    boss = Enemy(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 120, health=300, speed=1, boss=True)
                    enemies_group.add(boss)

        collectible_counter += 1
        if collectible_counter > 300:
            collectible_counter = 0
            kind = random.choice(['health', 'life'])
            c = Collectible(random.randint(50, SCREEN_WIDTH-50), SCREEN_HEIGHT - 100, kind)
            collectibles_group.add(c)

        # Update sprites
        player_group.update(platforms_group)
        projectiles_group.update()
        enemies_group.update()
        collectibles_group.update()

        # Check projectile collisions with enemies
        for proj in projectiles_group:
            hit_enemies = pygame.sprite.spritecollide(proj, enemies_group, False)
            for enemy in hit_enemies:
                proj.kill()
                killed = enemy.take_damage(proj.damage)
                if enemy_hit_sound:
                    enemy_hit_sound.play()
                if killed:
                    player.score += 100 if not enemy.boss else 1000
                    if enemy.boss:
                        boss_defeated = True
                        pygame.time.delay(1000)
                        if level < 3:
                            level += 1
                            player.health = 100
                            player.rect.x = 100
                            enemies_group.empty()
                            collectibles_group.empty()

        # Check player collisions with enemies (damage and push back)
        enemy_hits = pygame.sprite.spritecollide(player, enemies_group, False)
        for enemy in enemy_hits:
            player.health -= 1
            if player.rect.x < enemy.rect.x:
                player.rect.x -= 10
            else:
                player.rect.x += 10
            if player.health <= 0:
                player.lives -= 1
                player.health = 100
                player.rect.x = 100
                if player.lives <= 0:
                    # Game over
                    game_over_screen(screen, player.score)
                    # Reset game
                    player.lives = 3
                    player.score = 0
                    level = 1
                    boss_defeated = False
                    enemies_group.empty()
                    collectibles_group.empty()

        # Check player collisions with collectibles
        collected = pygame.sprite.spritecollide(player, collectibles_group, True)
        for item in collected:
            if collectible_sound:
                collectible_sound.play()
            if item.kind == 'health':
                player.health += 25
                if player.health > 100:
                    player.health = 100
                player.score += 50
            elif item.kind == 'life':
                player.lives += 1
                player.score += 100

        # Fill screen with background image or fallback color
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill((30, 30, 60))

        # Draw groups
        platforms_group.draw(screen)
        collectibles_group.draw(screen)
        enemies_group.draw(screen)
        projectiles_group.draw(screen)
        player_group.draw(screen)

        # HUD
        draw_text(screen, f'Score: {player.score}', 24, SCREEN_WIDTH//2, 10)
        draw_text(screen, f'Lives: {player.lives}', 24, 70, 10)
        draw_health_bar(screen, 120, 10, player.health)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
