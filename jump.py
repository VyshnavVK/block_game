import pygame
import numpy as np
from gameComponent import coins, updateScoreCount, bomb as b, game_over_check, coinIdSet


class GameEnvironment:
    def __init__(self, screen_width=1000, screen_height=725):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.character = pygame.image.load("assets/character/man_standing.png")
        self.background = pygame.image.load("assets/bg.png")
        self.character = pygame.transform.scale(self.character, (70, 70))
        self.character_rect = self.character.get_rect()
        self.character_rect.topleft = (0, self.screen_height - 230)
        self.character_rect.bottomleft = (0, self.screen_height - 180)
        self.platform_rect = pygame.Rect(0, self.screen_height - 100, self.screen_width, 100)
        self.wall_rect = pygame.Rect(screen_width - 30, 0, 100, screen_height)
        self.bombs = [b(700, self.screen_height, 165), b(340, self.screen_height, 165)]
        self.coins = [coins(450, self.screen_height, 265, 1), coins(850, self.screen_height, 265, 2)]
        self.vel = 10
        self.jump_max = 20
        self.jump = False
        self.jump_count = 0
        self.move_right = True
        self.frame_iteration = 0
        self.score = 0
        self.game_over = False
        self.reset()

    def reset(self):
        self.character_rect.topleft = (0, self.screen_height - 130)
        self.jump = False
        self.jump_count = 0
        self.move_right = True
        self.frame_iteration = 0
        self.score = 0
        self.game_over = False
        updateScoreCount(0, True)
        return self.get_state()

    def step(self, action):
        self.frame_iteration += 1
        self.window.blit(self.background, (0, 0))
        self.clock.tick(50)

        reward = 0

        #       if action == 0:  # Left
        #           self.character_rect.x -= self.vel
        if action == 0:  # Right
            self.character_rect.x += self.vel
        elif action == 1 and not self.jump:  # Jump
            self.jump = True
            self.jump_count = self.jump_max

        if self.jump:
            self.character_rect.y -= self.jump_count
            if self.jump_count > -self.jump_max:
                self.jump_count -= 1
            else:
                self.jump = False

        if self.character_rect.colliderect(self.platform_rect):
            if self.jump_count < 0:
                self.character_rect.bottom = self.platform_rect.top
                self.jump = False
                self.jump_count = 0

        if self.character_rect.colliderect(self.wall_rect):
            reward += 100
            self.game_over = True
            self.reset()

        #        if self.move_right:
        #            for bomb in self.bombs:
        #                bomb[1].x += 1
        #            if self.bombs[0][1].x >= 650:
        #                self.move_right = False
        #        else:
        #            for bomb in self.bombs:
        #                bomb[1].x -= 1
        #            if self.bombs[0][1].x <= 600:
        #                self.move_right = True

        for bomb in self.bombs:
            if self.character_rect.colliderect(bomb[1]):
                self.game_over = True
                reward = 0

        if self.frame_iteration > 5000:  # game over if you do nothing for an amount of time
            self.game_over = True

        reward += self.collect_coins()
        state = self.get_state()
        return state, reward, self.game_over

    def collect_coins(self):
        reward = 0
        for coin in self.coins:
            if coin[2] not in coinIdSet and self.character_rect.colliderect(coin[1]):
                reward += 100  # Reward for collecting a coin
                updateScoreCount(coin[2])
        return reward

    def get_state(self):
        state = [
            self.character_rect.x,
            self.character_rect.y,
            self.jump,
            self.jump_count,
            self.bombs[0][1].x,
            self.bombs[1][1].x
        ]
        return np.array(state, dtype=np.float32)

    def render(self, is_playing=False):
        self.window.blit(self.background, (0, 0))
        for bomb in self.bombs:
            self.window.blit(bomb[0], bomb[1].topleft)
        for coin in self.coins:
            if coin[2] not in coinIdSet:
                self.window.blit(coin[0], coin[1].topleft)
        self.window.blit(self.character, self.character_rect.topleft)
        scoreItem = updateScoreCount()
        self.window.blit(scoreItem[0], scoreItem[1])
        if is_playing and len(coinIdSet) >= 3:
            game_over_check(self.screen_width, self.screen_height, self.game_over, self.window)
            self.game_over = True
        for bomb in self.bombs:
            if is_playing and self.character_rect.colliderect(bomb[1]):
                self.game_over = True
                self.reset()

        pygame.display.flip()

    def close(self):
        pygame.quit()
