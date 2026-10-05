# Activity 2: Interactive Game Architecture: Game Loop, Custom Sprites, & Collision Detection

import pygame
import random
import sys

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Activity 2: Sprite System & Collision Arena')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# ---------------------------------------------------------
# CUSTOM SPRITE ENCAPSULATIONS
# ---------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (44, 94, 138), (20, 20), 20)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5
        
    def update(self):
        """Task 2.2: Continuous keyboard steering and screen boundary clamping."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: 
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH: 
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0: 
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT: 
            self.rect.y += self.speed


class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((220, 50, 50))
        self.rect = self.image.get_rect(
            topleft=(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
        )
        # Task 2.1: Give target obstacles basic roaming characteristics
        self.vel_x = random.choice([-2, -1, 1, 2])
        self.vel_y = random.choice([-2, -1, 1, 2])

    def update(self):
        """Handle roaming positioning and flip directional velocity on boundary hit."""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.vel_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.vel_y *= -1


class Particle(pygame.sprite.Sprite):
    """Task 2.4: Translucent impact particles using alpha fading surfaces."""
    def __init__(self, x, y):
        super().__init__()
        self.size = random.randint(6, 12)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        self.color = (255, 140, 0) 
        self.alpha = 255
        pygame.draw.circle(self.image, (*self.color, self.alpha), (self.size // 2, self.size // 2), self.size // 2)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.fade_speed = random.randint(8, 15)

    def update(self):
        """Advance positioning vectors and decrement alpha visibility properties."""
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)
        
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.kill()  
        else:
            self.image.fill((0, 0, 0, 0)) 
            pygame.draw.circle(self.image, (*self.color, self.alpha), (self.size // 2, self.size // 2), self.size // 2)

# ---------------------------------------------------------
# INITIALIZE MANAGED ENGINE COMPONENT GROUPS
# ---------------------------------------------------------

player_group = pygame.sprite.GroupSingle()
player = Player()
player_group.add(player)

target_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

for _ in range(8):
    target_group.add(Target())

# Task 2.3
score = 0
health = 100

# ---------------------------------------------------------
# MAIN GAME RENDER LIFECYCLE LOOP
# ---------------------------------------------------------

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player_group.update()
    target_group.update()
    particle_group.update()

    # Task 2.3
    collided_targets = pygame.sprite.spritecollide(player, target_group, True)
    for hit in collided_targets:
        score += 10
        health -= 5  
        
        for _ in range(12):
            particle_group.add(Particle(hit.rect.centerx, hit.rect.centery))
            
        target_group.add(Target())

    screen.fill((30, 30, 40)) 

    target_group.draw(screen)
    player_group.draw(screen)
    particle_group.draw(screen)

    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    
    hud_color = (100, 255, 100) if health > 30 else (255, 50, 50)
    health_surf = font.render(f"Health: {max(0, health)}%", True, hud_color)
    
    screen.blit(score_surf, (20, 20))
    screen.blit(health_surf, (SCREEN_WIDTH - 160, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
