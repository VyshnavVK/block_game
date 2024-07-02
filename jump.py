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

transparent_surface_start_width = 50
moving_obj_vel = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

background = pygame.image.load("assets/bg.png")

initial_character_position = (0, SCREEN_HEIGHT - 230)
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

coin1 = coins(300, SCREEN_HEIGHT, 175, 1)

coin2 = coins(850, SCREEN_HEIGHT, 265, 2)

coins = [coin1, coin2]

score_limit = 100

updateScoreCount: updateScoreCount


class Directions(Enum):
    LEFT = 1
    RIGHT = 2
    JUMP = 3


def coinCollect(active_coin):
    for _coin in active_coin:
        if character_rect.colliderect(_coin[1]):
            return updateScoreCount(_coin[2])
    return updateScoreCount()


class JumpGame:

    def __init__(self, update_score_count_func):
        self.frame_iteration = 0
        self.updateScore = None
        update_score_count_func(0, True)
        self.move_right = True
        self.game_over = False
        self.run = True
        self.jump = False
        self.jumpCount = 0
        character_rect.topleft = initial_character_position

    def reset_game(self):
        updateScoreCount(0, True)
        self.move_right = True
        self.game_over = False
        self.run = True
        self.jump = False
        self.jumpCount = 0
        character_rect.topleft = initial_character_position
        self.frame_iteration = 0

    def run_game(self):
        self.frame_iteration += 1
        window.blit(background, (0, 0))
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if not self.jump and (event.key == pygame.K_UP or Directions.JUMP == 0):
                    self.jump = True
                    self.jumpCount = jumpMax
                if self.game_over and event.key == pygame.K_RETURN:
                    self.reset_game()

        keys = pygame.key.get_pressed()
        left, right = False, False
        if not self.game_over:
            if keys[pygame.K_LEFT]:
                left = keys[pygame.K_LEFT]
                self.frame_iteration = 0
            if keys[pygame.K_RIGHT]:
                right = keys[pygame.K_RIGHT]
                self.frame_iteration = 0

            move_x = (right - left) * vel
            new_centerx = character_rect.centerx + move_x

            if transparent_surface_start_width < new_centerx < SCREEN_WIDTH:
                character_rect.centerx = new_centerx

            if self.jump:
                character_rect.y -= self.jumpCount
                if self.jumpCount > -jumpMax:
                    self.jumpCount -= 1
                else:
                    self.jump = False

            if character_rect.colliderect(platform_rect):
                if self.jumpCount < 0:
                    character_rect.bottom = platform_rect.top
                    self.jump = False
                    self.jumpCount = 0

            if self.move_right:
                moving_obj_rect.x += moving_obj_vel
                moving_obj_rect1.x += moving_obj_vel
                if moving_obj_rect.x >= 650:
                    self.move_right = False
            else:
                moving_obj_rect.x -= moving_obj_vel
                moving_obj_rect1.x -= moving_obj_vel
                if moving_obj_rect.x <= 600:
                    self.move_right = True

            if (character_rect.colliderect(moving_obj_rect)
                    or character_rect.colliderect(moving_obj_rect1)
                    or self.frame_iteration > (10 * score_limit)):  # game over if you do nothing for an amount of time
                self.game_over = True

        window.blit(background, (0, 0))

        transparent_surface_bottom = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
        transparent_surface_bottom.fill((0, 0, 0, 0))
        window.blit(transparent_surface_bottom, (0, SCREEN_HEIGHT - 100))

        transparent_surface_start = pygame.Surface((transparent_surface_start_width, SCREEN_HEIGHT),
                                                   pygame.SRCALPHA)
        transparent_surface_start.fill((0, 0, 0, 0))
        window.blit(transparent_surface_start, (0, 0))

        window.blit(moving_obj_img, moving_obj_rect.topleft)
        window.blit(moving_obj_img1, moving_obj_rect1.topleft)

        window.blit(character, character_rect.topleft)

        for coin in coins:
            window.blit(coin[0], coin[1])

        self.updateScore = coinCollect(coins)

        window.blit(self.updateScore[0], self.updateScore[1])

        game_over_check(SCREEN_WIDTH, SCREEN_HEIGHT, self.game_over, window)

        pygame.display.flip()


if __name__ == '__main__':
    game = JumpGame(updateScoreCount)

    while game.run:
        game.run_game()

    pygame.quit()
    exit()
