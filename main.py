import pygame
import sys
import os
import math

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("tanks")

# Colors
text_color = (211, 211, 211)

# Resources
image_path = os.path.join(os.path.dirname(__file__), 'resources/textures/tank-art.png')
player_tank_path = os.path.join(os.path.dirname(__file__), 'resources/textures/1.png')
wall_image_path = os.path.join(os.path.dirname(__file__), 'resources/textures/brick-wall.png')
bullet_image_path = os.path.join(os.path.dirname(__file__), 'resources/textures/bullet-1.png')
music_path = os.path.join(os.path.dirname(__file__), 'resources/music/background-music.mp3')

# Load resources
image = pygame.image.load(image_path)
player_tank = pygame.image.load(player_tank_path)
wall_image = pygame.image.load(wall_image_path)
bullet_image = pygame.image.load(bullet_image_path)

# Resize images
scale_factor = 0.5
image_size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
image = pygame.transform.scale(image, image_size)
player_tank = pygame.transform.scale(player_tank, (50, 50))
wall_image = pygame.transform.scale(wall_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (20, 20))

# Load sounds
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)

# Variables
player_pos = [screen.get_width() // 2, screen.get_height() // 2]
player_angle = 0
player_speed = 5
bullet_speed = 10
frame_rate = 17
clock = pygame.time.Clock()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, position):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=position)
        self.angle = angle
        self.velocity = pygame.math.Vector2(bullet_speed, 0).rotate(-angle)
        self.bounces = 1

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.bounces <= 0:
            self.kill()

    def bounce(self):
        self.bounces -= 1
        self.velocity = pygame.math.Vector2(-self.velocity.x, -self.velocity.y)

# Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = wall_image
        self.rect = self.image.get_rect(topleft=position)

# Create walls
def create_walls():
    wall_blocks = []
    block_size = wall_image.get_size()
    for x in range(0, screen.get_width(), block_size[0]):
        wall_blocks.append(Wall((x, 0)))
        wall_blocks.append(Wall((x, screen.get_height() - block_size[1])))
    for y in range(0, screen.get_height(), block_size[1]):
        wall_blocks.append(Wall((0, y)))
        wall_blocks.append(Wall((screen.get_width() - block_size[0], y)))
    return wall_blocks

walls_sprites = pygame.sprite.Group(create_walls())
bullets = pygame.sprite.Group()

def draw_rotated_image(image, angle, pos):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=pos).center)
    screen.blit(rotated_image, new_rect.topleft)

def shoot_bullet():
    bullet = Bullet(player_angle, player_pos)
    bullets.add(bullet)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle += 5
    if keys[pygame.K_RIGHT]:
        player_angle -= 5
    if keys[pygame.K_UP]:
        movement_vector = pygame.math.Vector2(0, -player_speed).rotate(-player_angle)
        new_pos = [player_pos[0] + movement_vector.x, player_pos[1] + movement_vector.y]
        player_rect = pygame.Rect(new_pos[0], new_pos[1], player_tank.get_width(), player_tank.get_height())
        if not any(player_rect.colliderect(wall.rect) for wall in walls_sprites):
            player_pos[0] = new_pos[0]
            player_pos[1] = new_pos[1]
    if keys[pygame.K_DOWN]:
        movement_vector = pygame.math.Vector2(0, player_speed).rotate(-player_angle)
        new_pos = [player_pos[0] + movement_vector.x, player_pos[1] + movement_vector.y]
        player_rect = pygame.Rect(new_pos[0], new_pos[1], player_tank.get_width(), player_tank.get_height())
        if not any(player_rect.colliderect(wall.rect) for wall in walls_sprites):
            player_pos[0] = new_pos[0]
            player_pos[1] = new_pos[1]
    if keys[pygame.K_SPACE]:
        shoot_bullet()

    screen.fill((0, 0, 0))

    for wall in walls_sprites:
        screen.blit(wall.image, wall.rect.topleft)

    draw_rotated_image(player_tank, player_angle, player_pos)

    for bullet in bullets:
        bullet.update()
        if pygame.sprite.spritecollideany(bullet, walls_sprites):
            bullet.bounce()
        screen.blit(bullet.image, bullet.rect.topleft)

    pygame.display.flip()
    clock.tick(frame_rate)
