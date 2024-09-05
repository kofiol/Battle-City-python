import pygame
import sys
import os
import time


asciiartkofiol = '''
#  --------------  #
#  made by kofiol  #
#  --------------  #
'''
print(asciiartkofiol)

pygame.init()


screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("tanks")


text_color = (211, 211, 211)


image_path = os.path.join(os.path.dirname(__file__), 'resources/textures/tank-art.png')
player_tank_path = os.path.join(os.path.dirname(__file__), 'resources/textures/1.png')
wall_image_path = os.path.join(os.path.dirname(__file__), 'resources/textures/brick-wall.png')
music_path = os.path.join(os.path.dirname(__file__), 'resources/music/background-music.mp3')


image = pygame.image.load(image_path)
player_tank = pygame.image.load(player_tank_path)
wall_image = pygame.image.load(wall_image_path)


scale_factor = 0.5
image_size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
image = pygame.transform.scale(image, image_size)
player_tank = pygame.transform.scale(player_tank, (50, 50))
wall_image = pygame.transform.scale(wall_image, (50, 50))


player_pos = [screen.get_width() // 2, screen.get_height() // 2]
player_angle = 0
player_speed = 5


frame_rate = 17
clock = pygame.time.Clock()


pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)  

def create_walls():
    wall_blocks = []
    block_size = wall_image.get_size()
    for x in range(0, screen.get_width(), block_size[0]):
        wall_blocks.append(pygame.Rect(x, 0, block_size[0], block_size[1]))
        wall_blocks.append(pygame.Rect(x, screen.get_height() - block_size[1], block_size[0], block_size[1]))
    for y in range(0, screen.get_height(), block_size[1]):
        wall_blocks.append(pygame.Rect(0, y, block_size[0], block_size[1]))
        wall_blocks.append(pygame.Rect(screen.get_width() - block_size[0], y, block_size[0], block_size[1]))
    return wall_blocks

wall_blocks = create_walls()

def draw_walls():
    for wall in wall_blocks:
        screen.blit(wall_image, wall.topleft)

def draw_rotated_image(image, angle, pos):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=pos).center)
    screen.blit(rotated_image, new_rect.topleft)

def check_collision(rect, blocks):
    for block in blocks:
        if rect.colliderect(block):
            return True
    return False

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
        if not check_collision(player_rect, wall_blocks):
            player_pos[0] = new_pos[0]
            player_pos[1] = new_pos[1]
    if keys[pygame.K_DOWN]:
        movement_vector = pygame.math.Vector2(0, player_speed).rotate(-player_angle)
        new_pos = [player_pos[0] + movement_vector.x, player_pos[1] + movement_vector.y]
        player_rect = pygame.Rect(new_pos[0], new_pos[1], player_tank.get_width(), player_tank.get_height())
        if not check_collision(player_rect, wall_blocks):
            player_pos[0] = new_pos[0]
            player_pos[1] = new_pos[1]

    screen.fill((0, 0, 0))  
    draw_walls()
    draw_rotated_image(player_tank, player_angle, player_pos)
    pygame.display.flip()
    clock.tick(frame_rate)

