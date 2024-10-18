import pygame
import random
import os

# Initialization Pygame
pygame.init()

# Set the working directory to where your assets are located
os.chdir(r"F:\CDU\HIT137 SOFTWARE NOW")

# Game Constants
SCREEN_WIDTH = 800 #game window width
SCREEN_HEIGHT = 560 #game window height
GROUND_HEIGHT = 60 #ground height in the game
JUMP_HEIGHT = -14 #jump velocity
FPS = 60 #frame per second
PLAYER_SPEED = 5 #player movement
MAX_LIVES = 3 #max number of lives of the player
MAX_HEALTH_PER_LIFE = 3 #health points per life
INITIAL_SPEED = -3 # Initial speed of enemies and object
ENEMY_HEALTH = 3 # Health of enemies
DIAMOND_POINTS = 150 # Points for collecting a diamond
OBSTACLES_PER_LEVEL = 24 # Number of enemies per level


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.WIDTH = 100
        self.HEIGHT = 130
        try:
            # background_img = pygame.image.load(r"F:\CDU\HIT137 SOFTWARE NOW\assets\background.jpg").convert()
            original_image = pygame.image.load(os.path.join('assets', 'player_one.png')).convert_alpha()
            self.image = pygame.transform.scale(original_image, (self.WIDTH, self.HEIGHT))
        except Exception as e:
            print(f"Player image error: {e}. Using placeholder.")
            self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        self.velocity_y = 0
        self.jumping = False
        self.lives = MAX_LIVES
        self.health = MAX_HEALTH_PER_LIFE
        self.last_hit = 0

    def update(self):
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_j] and not self.jumping:
            self.velocity_y = JUMP_HEIGHT
            self.jumping = True

# Apply gravity and update vertical position
        self.velocity_y += 0.8
        self.rect.y += self.velocity_y

        if self.rect.bottom > SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.velocity_y = 0
            self.jumping = False

        # Keep player within screen bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.WIDTH))

    def hit(self):
        # Reduce health if hit by an enemy (with 1 second invulnerability)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit > 1000:  # 1 second invulnerability
            self.health -= 1
            self.last_hit = current_time
            if self.health <= 0:
                self.lives -= 1
                if self.lives > 0:
                    self.health = MAX_HEALTH_PER_LIFE
                return True
        return False

    def heal(self):
        self.health = min(self.health + 1, MAX_HEALTH_PER_LIFE) # Heal player by increasing health but not exceeding max health


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.WIDTH = 40
        self.HEIGHT = 40
        try:
            original_image = pygame.image.load(os.path.join('assets', 'firee.png')).convert_alpha()
            self.image = pygame.transform.scale(original_image, (self.WIDTH, self.HEIGHT))
        except Exception as e:
            print(f"Firee image error: {e}. Using placeholder.")
            self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.image.fill(RED)

# Set initial position and speed of the projectile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, speed):
        super().__init__()
        self.WIDTH = 68
        self.HEIGHT = 95
        try:
            original_image = pygame.image.load(os.path.join('assets', 'enemy1.png')).convert_alpha()
            self.image = pygame.transform.scale(original_image, (self.WIDTH, self.HEIGHT))
        except Exception as e:
            print(f"Enemy image error: {e}. Using placeholder.")
            self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.image.fill(RED)

# Set initial position and speed of the enemy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        self.speed = speed
        self.health = ENEMY_HEALTH

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False


class HealthPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.WIDTH = 30
        self.HEIGHT = 30
        try:
            original_image = pygame.image.load(os.path.join('assets', 'health.png')).convert_alpha()
            self.image = pygame.transform.scale(original_image, (self.WIDTH, self.HEIGHT))
        except Exception as e:
            print(f"Health power up image error: {e}. Using placeholder.")
            self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.WIDTH = 30
        self.HEIGHT = 30
        try:
            original_image = pygame.image.load(os.path.join('assets', 'coin.png')).convert_alpha()
            self.image = pygame.transform.scale(original_image, (self.WIDTH, self.HEIGHT))
        except Exception as e:
            print(f"Coin image error: {e}. Using placeholder.")
            self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.image.fill((0, 255, 255))  # Cyan color for coin placeholder

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -2

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lost in the Jungle")
        self.clock = pygame.time.Clock()

        try:
            self.background = pygame.image.load(os.path.join('assets', 'background.jpg')).convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Background image error: {e}. Using color background.")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((135, 206, 235))

        try:
            original_life_image = pygame.image.load(os.path.join('assets', 'life.png')).convert_alpha()
            self.life_image = pygame.transform.scale(original_life_image, (30, 30))
        except Exception as e:
            print(f"Life image error: {e}. Using placeholder.")
            self.life_image = pygame.Surface((30, 30))
            self.life_image.fill(RED)

        self.running = True
        self.game_over = False
        self.reset_game()

    def reset_game(self):
        self.current_level = 1
        self.obstacles_remaining = OBSTACLES_PER_LEVEL
        self.current_speed = INITIAL_SPEED
        self.score = 0
        self.base_points = 50

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.health_powerups = pygame.sprite.Group()
        self.diamonds = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.spawn_timer = 0
        self.diamond_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.game_over:
                    self.reset_game()
                    self.game_over = False
                elif event.key == pygame.K_f and not self.game_over:
                    self.shoot_projectile()

    def shoot_projectile(self):
        projectile = Projectile(self.player.rect.right, self.player.rect.centery)
        self.all_sprites.add(projectile)
        self.projectiles.add(projectile)

    def spawn_enemy(self):
        if self.obstacles_remaining > 0:
            enemy = Enemy(SCREEN_WIDTH, self.current_speed)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
            self.obstacles_remaining -= 1

    def spawn_health_powerup(self):
        x = random.randint(0, SCREEN_WIDTH - 30)
        y = 0
        powerup = HealthPowerUp(x, y)
        self.all_sprites.add(powerup)
        self.health_powerups.add(powerup)

    def spawn_diamond(self):
        x = SCREEN_WIDTH
        y = random.randint(GROUND_HEIGHT, SCREEN_HEIGHT - GROUND_HEIGHT - 30)
        coin = Coin(x, y)
        self.all_sprites.add(coin)
        self.diamonds.add(coin)

    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            self.handle_collisions()

            self.spawn_timer += 1
            if self.spawn_timer >= 60 and self.obstacles_remaining > 0:
                self.spawn_timer = 0
                self.spawn_enemy()

            self.diamond_timer += 1
            if self.diamond_timer >= 180:  # Spawn a diamond every 3 seconds
                self.diamond_timer = 0
                self.spawn_diamond()

            if (self.obstacles_remaining <= 0 and len(self.enemies) == 0):
                self.advance_level()

    def advance_level(self):
        self.current_level += 1
        self.obstacles_remaining = OBSTACLES_PER_LEVEL
        self.current_speed = INITIAL_SPEED - (self.current_level - 1)
        self.base_points = int(self.base_points * 1.25)  # Increase points by 25%
        print(f"Level {self.current_level} - Speed: {abs(self.current_speed)} - Points per kill: {self.base_points}")
        self.spawn_health_powerup()

    def handle_collisions(self):
        # Player-Enemy collisions
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            if self.player.hit():
                if self.player.lives <= 0:
                    self.game_over = True

        # Projectile-Enemy collisions
        hits = pygame.sprite.groupcollide(self.projectiles, self.enemies, True, False)
        for projectile, enemies_hit in hits.items():
            for enemy in enemies_hit:
                if enemy.hit():
                    self.score += self.base_points

        # Player-HealthPowerUp collisions
        hits = pygame.sprite.spritecollide(self.player, self.health_powerups, True)
        for powerup in hits:
            self.player.heal()

        # Player-Diamond collisions
        hits = pygame.sprite.spritecollide(self.player, self.diamonds, True)
        for diamond in hits:
            self.score += DIAMOND_POINTS

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_ui()
        self.draw_health_bars()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_ui(self):
        font = pygame.font.Font(None, 32)

        # Create a semi-transparent background for UI
        ui_background = pygame.Surface((250, 120))
        ui_background.set_alpha(128)
        ui_background.fill((0, 0, 0))
        self.screen.blit(ui_background, (SCREEN_WIDTH - 260, 10))

        # Draw lives
        for i in range(self.player.lives):
            self.screen.blit(self.life_image, (SCREEN_WIDTH - 50 - i * 40, 20))

        # Draw level, score, and remaining enemies
        level_text = font.render(f'Level: {self.current_level}', True, WHITE)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        obstacles_text = font.render(f'Enemies: {self.obstacles_remaining}', True, WHITE)

        self.screen.blit(level_text, (SCREEN_WIDTH - 250, 20))
        self.screen.blit(score_text, (SCREEN_WIDTH - 250, 55))
        self.screen.blit(obstacles_text, (SCREEN_WIDTH - 250, 90))

    def draw_health_bars(self):
        # Player health bar
        pygame.draw.rect(self.screen, RED, (self.player.rect.x, self.player.rect.y - 10, self.player.WIDTH, 5))
        pygame.draw.rect(self.screen, GREEN, (self.player.rect.x, self.player.rect.y - 10,
                                              self.player.WIDTH * (self.player.health / MAX_HEALTH_PER_LIFE), 5))

        # Enemy health bars
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, RED, (enemy.rect.x, enemy.rect.y - 10, enemy.WIDTH, 5))
            pygame.draw.rect(self.screen, GREEN, (enemy.rect.x, enemy.rect.y - 10,
                                                  enemy.WIDTH * (enemy.health / ENEMY_HEALTH), 5))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        large_font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 36)

        text = large_font.render('Game Over!!', True, WHITE)
        level_text = small_font.render(f'Level Reached: {self.current_level}', True, WHITE)
        score_text = small_font.render(f'Final Score: {self.score}', True, WHITE)
        restart_text = small_font.render('Press Enter to Restart', True, WHITE)

        texts = [text, level_text, score_text, restart_text]
        for i, surface in enumerate(texts):
            bg_rect = surface.get_rect(center=(SCREEN_WIDTH // 2,
                                               SCREEN_HEIGHT // 2 - 60 + i * 40))
            self.screen.blit(surface, bg_rect)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
