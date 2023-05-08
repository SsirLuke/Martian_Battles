import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Martian Battles")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2 - 10, WIDTH, 10)

BULLET_HIT_SOUND = pygame.mixer.Sound('Pygame_games\Assets\Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Pygame_games\Assets\Gun+Silencer.mp3')
IM_BOUTA_BLOW = pygame.mixer.Sound('Pygame_games\Assets\im-bouta-blow.mp3')

HEALTH_FONT = pygame.font.SysFont('timesnewroman', 40)
WINNER_FONT = pygame.font.SysFont('timesnewroman', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40



YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#spaceship and martian images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Pygame_games\Assets\spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Pygame_games\Assets\Martian.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

GALAXY = pygame.transform.scale(pygame.image.load(
    os.path.join('Pygame_games\Assets\Galaxy.png')), (WIDTH, HEIGHT))




def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(GALAXY, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_a] and yellow.x - VEL > -2: #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.width < 496:  # down
        yellow.y += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.height < WIDTH:  # right
        yellow.x += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y - VEL - 8 > 495:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > -2: #left
        red.x -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.width < HEIGHT:  # down
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.height < WIDTH:  # right
        red.x += VEL



def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:

        bullet.y += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.y > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.y < 0:
            red_bullets.remove(bullet)



def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(WIDTH//2 - 5, 750, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(WIDTH//2 - 5, 350, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if yellow_health == 2:
                IM_BOUTA_BLOW.play()

            if red_health == 2:
                IM_BOUTA_BLOW.play()

        winner_text = ""

        if red_health == 2:
            event.type 
        if red_health <= 0:
            winner_text = "Humans Wins!"

        if yellow_health <= 0:
            winner_text = "Martians win!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()