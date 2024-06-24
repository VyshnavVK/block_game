import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 50
PLAYER_SIZE = 30
DEAD_AREA_SIZE = 10
DIAMOND_SIZE = 20
NUM_BLOCKS = 20
NUM_DEAD_AREAS = 6
POINT_DEDUCTION = 10
POINT_GAIN = 100
LIFE = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

block_image = pygame.image.load("assets/bomb.png")
block_image = pygame.transform.scale(block_image, (BLOCK_SIZE, BLOCK_SIZE))

diamond_image = pygame.image.load("assets/diamond.png")
diamond_image = pygame.transform.scale(diamond_image, (DIAMOND_SIZE, DIAMOND_SIZE))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Game")

isGameOver = False


class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.color = BLUE
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.image = block_image
        self.dead_areas = [pygame.Rect(x + random.randint(0, BLOCK_SIZE - DEAD_AREA_SIZE),
                                       y + random.randint(0, BLOCK_SIZE - DEAD_AREA_SIZE),
                                       DEAD_AREA_SIZE, DEAD_AREA_SIZE) for _ in range(NUM_DEAD_AREAS)]
        self.has_diamond = False

    def draw(self):
        screen.blit(self.image, self.rect)
        for da in self.dead_areas:
            if not self.has_diamond:
                pygame.draw.rect(screen, RED, da)
        if self.has_diamond:
            diamond_pos = self.rect.x + (BLOCK_SIZE - DIAMOND_SIZE) // 2, self.rect.y + (BLOCK_SIZE - DIAMOND_SIZE) // 2
            screen.blit(diamond_image, diamond_pos)


player = Player()

blocks = [Block(random.randint(0, SCREEN_WIDTH - BLOCK_SIZE), random.randint(0, SCREEN_HEIGHT - BLOCK_SIZE)) for _ in
          range(NUM_BLOCKS)]

diamond_block = random.choice(blocks)
diamond_block.has_diamond = True

score = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1

    player.move(dx, dy)

    for block in blocks:
        for da in block.dead_areas:
            if player.rect.colliderect(da):
                score -= POINT_DEDUCTION
                LIFE = LIFE - 1
                if LIFE == 0:
                    isGameOver = True
        if block.has_diamond and player.rect.colliderect(block.rect):
            score = POINT_GAIN
            isGameOver = True
            #running = False

    screen.fill(WHITE)

    player.draw()
    for block in blocks:
        block.draw()
    if not isGameOver:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(text, (10, 10))

    if isGameOver:
        font1 = pygame.font.Font(None, 136)
        text1 = font1.render("Game Over", True, BLUE)
        text_rect = text1.get_rect()
        text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        screen.blit(text1, text_rect)

        font2 = pygame.font.Font(None, 70)
        text2 = font2.render(f"Score: {score}", True, BLACK)
        text_rect = text1.get_rect()
        text_rect.center = ((screen.get_width() // 2) + 150, (screen.get_height() // 2) + 100)
        screen.blit(text2, text_rect)
        running = False

    pygame.display.flip()

    pygame.time.Clock().tick(30)

pygame.quit()
