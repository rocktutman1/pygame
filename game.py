import pygame
import sys
import random
def drawing():
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, color_coin, coin)
    pygame.draw.rect(screen, color, player_rect)
    pygame.draw.rect(screen, color_floor, floor_rect)
    pygame.draw.rect(screen, color_floor, wall_left_rect)
    pygame.draw.rect(screen, color_floor, wall_right_rect)
    pygame.draw.rect(screen, color_lava, lava_box_1)
    pygame.draw.rect(screen, color_lava, lava_box_2)
    pygame.draw.rect(screen, color_lava, lava_box_3)
    screen.blit(player_sprite, (player_rect.x-10, player_rect.y-10))  


# 1) Initialize the engine
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
# 2) Setup the "hero" (the math)
player_rect = pygame.Rect(375, 500, 50, 50)
player_speed = 0
y_vel = 15
player_sprite = pygame.image.load("epstein.jpeg").convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (70, 70))
# 2.5) Setup the enviornment
floor_rect = pygame.Rect(0,550,800,50)
wall_left_rect = pygame.Rect(0,0,30,600)
wall_right_rect = pygame.Rect(770,0,30,600)
lava_box_1 = pygame.Rect(random.randint(50,750), random.randint(50,440), 30, 30)
lava_box_2 = pygame.Rect(random.randint(50,750), random.randint(50,440), 30, 30)
lava_box_3 = pygame.Rect(random.randint(50,750), random.randint(50,440), 30, 30)
lava_boxes = [lava_box_1, lava_box_2, lava_box_3]
while True:
    coin = pygame.Rect(random.randint(50, 750), random.randint(50, 450), 30, 30)
    if all(not coin.colliderect(lava.inflate(70, 70)) for lava in lava_boxes):
        break
coins_collected = 0
# 2.75) Setup colors and fonts
font = pygame.font.SysFont('Arial', 20)
font_final = pygame.font.SysFont('Arial', 80)
color = (255, 0, 0)
color_floor = (0,0,75)
color_coin = (227, 223, 4)
color_lava = (181, 24, 56)
# 3) The holy game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    y_vel += 0.5
    keys = pygame.key.get_pressed()
    if True: #Coin stuff     
        text_surface = font.render(f'Collected {coins_collected}/15 Coins', False, (0, 0, 0))
        if player_rect.colliderect(coin):
            while True:
                coin = pygame.Rect(random.randint(50, 750), random.randint(50, 450), 30, 30)
                if all(not coin.colliderect(lava.inflate(70, 70)) for lava in lava_boxes):
                    break
            coins_collected += 1
    if True: #X axis movement and acceleration
        if keys[pygame.K_LEFT]:
            player_speed -= 1
        elif keys[pygame.K_RIGHT]:
            player_speed += 1
        else:
            if player_speed > 0 and not player_rect.colliderect(floor_rect):
                player_speed -= .5
            elif player_speed < 0 and not player_rect.colliderect(floor_rect):
                player_speed += .5
            elif player_speed > 0:
                player_speed -= 1
            elif player_speed < 0:
                player_speed += 1
    if True: #Deceleration
        if player_speed > 7:
            player_speed -= 1
        elif player_speed < -7:
            player_speed += 1
        if player_speed > 40:
            player_speed = 40
        elif player_speed < -40:
            player_speed = -40
    if True: #Movement
        player_rect.x += player_speed
        player_rect.y += y_vel
    if True: #Collision
        if player_rect.colliderect(wall_left_rect):
            player_speed = -2 * player_speed
            player_rect.left = wall_left_rect.right
        if player_rect.colliderect(wall_right_rect):
            player_speed = -2 * player_speed
            player_rect.right = wall_right_rect.left
        if player_rect.colliderect(floor_rect):
            if y_vel > 3:
                y_vel = -1/2 * y_vel
            else:
                y_vel = 0
            player_rect.bottom = floor_rect.top
            if keys[pygame.K_UP]:
                y_vel -= 11
    drawing()
    screen.blit(text_surface, (30,0))
    pygame.display.flip()
    # Cap to 60 FPS
    clock.tick(60)
    if True: #win/loose detection
        if coins_collected >= 15:
            win = True
            break
        if any(player_rect.colliderect(x) for x in lava_boxes):
            win = False
            break
time_to_quit = 0
if win == True:
    text_surface = font_final.render(f'Congradulations!', False, (39, 199, 32))
    text_surface1 = font_final.render(f'You win!', False, (39, 199, 32))
if win == False:
    text_surface = font_final.render(f'Congradulations!', False, color_lava)
    text_surface1 = font_final.render(f'You Died!', False, color_lava)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if any(keys):
        if time_to_quit > 120:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    drawing()
    screen.blit(text_surface, (120,200))
    screen.blit(text_surface1, (240,300))
    pygame.display.flip()
    time_to_quit += 1
