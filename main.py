# made by @kofiol
# for @sv0080

import pygame
import sys
import os

asciiartkofiol = '''
#  --------------  #
#  made by kofiol  #
#  --------------  #
'''
print(asciiartkofiol)

# initialize pygame
pygame.init()

# screen resolution
screen = pygame.display.set_mode((1080, 720))

# window title
pygame.display.set_caption("tanks")

# font
font_path = os.path.join(os.path.dirname(__file__), 'resources/fonts/ps-2p-font.ttf')
font = pygame.font.Font(font_path, 48)

# text color
text_color = (211, 211, 211)

# greeting text
initial_text = ["НАЖМИ ENTER", "ЧТОБЫ ИГРАТЬ", "В ТАНЧИКИ"]
wait_text = ["ИНИЦИАЛИЗАЦИЯ,", "ПОЖАЛУЙСТА ПОДОЖДИТЕ...", "загружаем ресурсы", "осталось 2 сек"]

# greeting tank art path and size parameters
image_path = os.path.join(os.path.dirname(__file__), 'resources/images/tank-art.png')
image = pygame.image.load(image_path)
scale_factor = 0.5
image_size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
image = pygame.transform.scale(image, image_size)

# player tank image path
player_tank_path = os.path.join(os.path.dirname(__file__), 'resources/images/1.png')
player_tank = pygame.image.load(player_tank_path)
player_tank = pygame.transform.scale(player_tank, (50, 50))

# greeting tank padding
image_rect = image.get_rect()
padding = 20
image_rect.bottomleft = (padding, screen.get_height() - padding)

# greeting tank animation
tank_x_pos = screen.get_width()  # start completely off-screen on the right
tank_speed = 5  # speed at which the tank moves

# frame rate control
frame_rate = 17
clock = pygame.time.Clock()

# animation control
animation_timer = 0
animation_interval = 0.3  # time in seconds

# current text to display
current_text = initial_text
tank_visible = True  # tank visibility control
refresh_start_time = None
refresh_duration = 0.5  # time to display "please wait..." in seconds
refresh_effect_duration = 0.66  # duration of the refresh effect in seconds
screen_refreshing = False
refresh_step_time = 0

# player tank control variables
player_pos = [screen.get_width() // 2, screen.get_height() // 2]
player_angle = 0
player_speed = 5

def draw_rotated_image(image, angle, pos):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=pos).center)
    screen.blit(rotated_image, new_rect.topleft)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not screen_refreshing:
                current_text = wait_text
                tank_visible = False
                refresh_start_time = pygame.time.get_ticks() / 1000.0  # start refresh
                screen_refreshing = True
                refresh_step_time = pygame.time.get_ticks() / 1000.0

    if screen_refreshing:
        # handle refresh animation and transition
        current_time = pygame.time.get_ticks() / 1000.0  
        if current_time - refresh_start_time < refresh_duration:
            # display "please wait..." for 2.5 seconds
            screen.fill((0, 0, 0))  # clear screen
            y_offset = 150
            for line in current_text:
                text = font.render(line, True, text_color)
                screen.blit(text, (50, y_offset))
                y_offset += font.get_height()
        elif current_time - refresh_start_time < (refresh_duration + refresh_effect_duration):
            # vertical line refresh effect
            if (current_time - refresh_step_time) >= refresh_effect_duration / (screen.get_width() // 2):
                refresh_step_time = current_time
                screen.fill((0, 0, 0))  # clear screen
        else:
            # start the game level after refresh
            screen_refreshing = False
            current_text = []
            tank_visible = False

    if not screen_refreshing and current_text == []:
        # game level logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_angle += 5
        if keys[pygame.K_RIGHT]:
            player_angle -= 5
        if keys[pygame.K_UP]:
            movement_vector = pygame.math.Vector2(0, -player_speed).rotate(-player_angle)
            player_pos[0] += movement_vector.x
            player_pos[1] += movement_vector.y
        if keys[pygame.K_DOWN]:
            movement_vector = pygame.math.Vector2(0, player_speed).rotate(-player_angle)
            player_pos[0] += movement_vector.x
            player_pos[1] += movement_vector.y

        screen.fill((0, 0, 0))  # clear screen for the level
        draw_rotated_image(player_tank, player_angle, player_pos)

    elif not screen_refreshing:
        screen.fill((0, 0, 0))  # clear screen
        if tank_visible:
            # update tank position
            tank_x_pos -= tank_speed
            if tank_x_pos < -image_rect.width:
                tank_x_pos = screen.get_width()
            # update animation timer
            current_time = pygame.time.get_ticks() / 1000.0 
            if current_time - animation_timer >= animation_interval:
                animation_timer = current_time
                # update tank position
                image_rect.topleft = (tank_x_pos, screen.get_height() - image_rect.height - padding)
            screen.blit(image, image_rect)
        # display initial text
        y_offset = 150
        for line in current_text:
            text = font.render(line, True, text_color)
            screen.blit(text, (50, y_offset))
            y_offset += font.get_height()

    pygame.display.flip()
    clock.tick(frame_rate)
