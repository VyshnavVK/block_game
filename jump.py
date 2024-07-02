from enum import Enum

import pygame
from gameComponent import coins, updateScoreCount, bomb as b, game_over_check

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 725

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

rect = pygame.Rect(135, SCREEN_HEIGHT - 137, 30, 30)
vel = 10
jumpMax = 20

jump = False
jumpCount = 0
transparent_surface_start_width = 50
moving_obj_vel = 1

move_right = True
game_over = False
run = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

background = pygame.image.load("assets/bg.png")

initial_character_position = (135, SCREEN_HEIGHT - 230)
character = pygame.image.load("assets/character/man_standing.png")
character_rect = character.get_rect()
character_rect.topleft = initial_character_position

platform_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)

bomb = b(600, SCREEN_HEIGHT, 165)
moving_obj_img = bomb[0]
moving_obj_rect = bomb[1]

bomb1 = b(300, SCREEN_HEIGHT, 350)
moving_obj_img1 = bomb1[0]
moving_obj_rect1 = bomb1[1]

back_buffer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

coin = coins(850, SCREEN_HEIGHT, 265, 1)

updateScoreCount: updateScoreCount


def reset_game():
    global move_right, game_over, run, jump, jumpCount, character_rect
    updateScoreCount(0, True)
    move_right = True
    game_over = False
    run = True
    jump = False
    jumpCount = 0
    character_rect.topleft = initial_character_position


class Directions(Enum):
    LEFT = 1
    RIGHT = 2
    JUMP = 3


while run:
    window.blit(background, (0, 0))
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not jump and (event.key == pygame.K_UP or Directions.JUMP == 0):
                jump = True
                jumpCount = jumpMax
            if game_over and event.key == pygame.K_RETURN:
                reset_game()

    keys = pygame.key.get_pressed()
    left, right = False, False
    if not game_over:
        if keys == pygame.K_LEFT or Directions.LEFT:
            left = keys[pygame.K_LEFT]
        if keys == pygame.K_RIGHT or Directions.RIGHT:
            right = keys[pygame.K_RIGHT]

        move_x = (right - left) * vel
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
            moving_obj_rect1.x += moving_obj_vel
            if moving_obj_rect.x >= 650:
                move_right = False
        else:
            moving_obj_rect.x -= moving_obj_vel
            moving_obj_rect1.x -= moving_obj_vel
            if moving_obj_rect.x <= 600:
                move_right = True

        if character_rect.colliderect(moving_obj_rect) or character_rect.colliderect(moving_obj_rect1):
            game_over = True

    window.blit(background, (0, 0))

    transparent_surface_bottom = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
    transparent_surface_bottom.fill((0, 0, 0, 0))
    window.blit(transparent_surface_bottom, (0, SCREEN_HEIGHT - 100))

    transparent_surface_start = pygame.Surface((transparent_surface_start_width, SCREEN_HEIGHT), pygame.SRCALPHA)
    transparent_surface_start.fill((0, 0, 0, 0))
    window.blit(transparent_surface_start, (0, 0))

    window.blit(moving_obj_img, moving_obj_rect.topleft)
    window.blit(moving_obj_img1, moving_obj_rect1.topleft)

    window.blit(character, character_rect.topleft)
    window.blit(coin[0], coin[1])

    updateScore = updateScoreCount()
    if character_rect.colliderect(coin[1]):
        updateScore = updateScoreCount(coin[2])

    window.blit(updateScore[0], updateScore[1])

    game_over_check(SCREEN_WIDTH, SCREEN_HEIGHT, game_over, window)

    pygame.display.flip()

pygame.quit()
exit()
