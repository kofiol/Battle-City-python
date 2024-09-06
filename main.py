import pygame
import sys
import os

kofiol = '''
 d8b                  ,d8888b  d8,         d8b 
 ?88     made by      88P'    `8P          88P 
  88b              d888888P               d88  
  888  d88' d8888b   ?88'      88b d8888b 888  
  888bd8P' d8P' ?88  88P       88Pd8P' ?88?88  
 d88888b   88b  d88 d88       d88 88b  d88 88b 
d88' `?88b,`?8888P'd88'      d88' `?8888P'  88b
        --nothing ever lasts forever--
'''
print(kofiol)

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
font_path = os.path.join(os.path.dirname(__file__), 'resources/fonts/ps-2p-font.ttf')

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

# Load font
font = pygame.font.Font(font_path, 30)

# Variables
player_pos = [screen.get_width() // 2, screen.get_height() // 2]
player_angle = 0
player_speed = 5
bullet_speed = 10
clock = pygame.time.Clock()
bullet_delay = 1.5 * 1000  # 1.5 seconds in milliseconds
last_bullet_time = 0

# New function to determine which wall the tank is facing
def get_facing_wall(angle):
    normalized_angle = angle % 360
    if 45 <= normalized_angle < 135:
        return "top"
    elif 135 <= normalized_angle < 225:
        return "left"
    elif 225 <= normalized_angle < 315:
        return "bottom"
    else:
        return "right"

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, position):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=position)
        self.direction = direction
        self.speed = bullet_speed

    def update(self):
        if self.direction == "top":
            self.rect.y -= self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "bottom":
            self.rect.y += self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if self.rect.top < 0 or self.rect.bottom > screen.get_height() or \
           self.rect.left < 0 or self.rect.right > screen.get_width():
            self.kill()

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
    facing_wall = get_facing_wall(player_angle)
    bullet = Bullet(facing_wall, player_pos)
    bullets.add(bullet)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if keys[pygame.K_LEFT]:
        player_angle += 90
    if keys[pygame.K_RIGHT]:
        player_angle -= 90
    if keys[pygame.K_UP]:
        facing_wall = get_facing_wall(player_angle)
        movement = {
            "top": (0, -player_speed),
            "left": (-player_speed, 0),
            "bottom": (0, player_speed),
            "right": (player_speed, 0)
        }[facing_wall]
        
        new_pos = [player_pos[0] + movement[0], player_pos[1] + movement[1]]
        player_rect = pygame.Rect(new_pos[0], new_pos[1], player_tank.get_width(), player_tank.get_height())
        if not any(player_rect.colliderect(wall.rect) for wall in walls_sprites):
            player_pos[0] = new_pos[0]
            player_pos[1] = new_pos[1]
    if keys[pygame.K_SPACE] and current_time - last_bullet_time >= bullet_delay:
        shoot_bullet()
        last_bullet_time = current_time

    screen.fill((0, 0, 0))

    for wall in walls_sprites:
        screen.blit(wall.image, wall.rect.topleft)

    draw_rotated_image(player_tank, player_angle, player_pos)

    for bullet in bullets:
        bullet.update()
        screen.blit(bullet.image, bullet.rect.topleft)

    # Display reload or ready message
    if current_time - last_bullet_time < bullet_delay:
        text_surface = font.render('RELOADING', True, text_color)
    else:
        text_surface = font.render('READY TO SHOOT', True, text_color)
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(30)
