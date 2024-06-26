import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 725

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

rect = pygame.Rect(135, SCREEN_HEIGHT - 137, 30, 30)
vel = 10
jump = False
jumpCount = 0
jumpMax = 20
transparent_surface_start_width = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

background = pygame.image.load("assets/bg.png")

character = pygame.image.load("assets/character/man_standing.png")
character_rect = character.get_rect()
character_rect.topleft = (135, SCREEN_HEIGHT - 230)

platform_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)

moving_obj_img = pygame.image.load("assets/bomb.png")
moving_obj_rect = moving_obj_img.get_rect()
moving_obj_rect.topleft = (600, SCREEN_HEIGHT - 165)
moving_obj_vel = 1
move_right = True
game_over = False
run = True
back_buffer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


def game_over_check():
    if game_over:
        font = pygame.font.Font(None, 120)
        game_over_text = font.render("Game Over", True, (102, 43, 40))
        window.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3*1000)


while run:
    window.blit(background, (0, 0))
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not jump and event.key == pygame.K_UP:
                jump = True
                jumpCount = jumpMax

    keys = pygame.key.get_pressed()

    if not game_over:
        move_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
        new_centerx = character_rect.centerx + move_x

        if transparent_surface_start_width < new_centerx < SCREEN_WIDTH:
            character_rect.centerx = new_centerx

        if jump:
            character_rect.y -= jumpCount
            if jumpCount > -jumpMax:
                jumpCount -= 1
            else:
                jump = False

        if character_rect.colliderect(platform_rect):
            if jumpCount < 0:
                character_rect.bottom = platform_rect.top
                jump = False
                jumpCount = 0

        if move_right:
            moving_obj_rect.x += moving_obj_vel
            if moving_obj_rect.x >= 650:
                move_right = False
        else:
            moving_obj_rect.x -= moving_obj_vel
            if moving_obj_rect.x <= 600:
                move_right = True

        if character_rect.colliderect(moving_obj_rect):
            game_over = True

    window.blit(background, (0, 0))

    transparent_surface_bottom = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
    transparent_surface_bottom.fill((64, 64, 64, 0))
    window.blit(transparent_surface_bottom, (0, SCREEN_HEIGHT - 100))

    transparent_surface_start = pygame.Surface((transparent_surface_start_width, SCREEN_HEIGHT), pygame.SRCALPHA)
    transparent_surface_start.fill((64, 64, 64, 0))
    window.blit(transparent_surface_start, (0, 0))
    window.blit(moving_obj_img, moving_obj_rect.topleft)
    window.blit(character, character_rect.topleft)
    pygame.display.flip()

    game_over_check()

pygame.quit()
exit()
