import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 725

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

rect = pygame.Rect(135, SCREEN_HEIGHT - 137, 30, 30)
vel = 5
jump = False
jumpCount = 0
jumpMax = 15


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
run = True

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
    character_rect.centerx = (character_rect.centerx + (
                keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel) % SCREEN_WIDTH

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

    window.blit(background, (0, 0))
    transparent_surface = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
    transparent_surface.fill((64, 64, 64, 128))

    window.blit(transparent_surface, (0, SCREEN_HEIGHT - 100))

    window.blit(character, character_rect.topleft)
    pygame.display.flip()

pygame.quit()
exit()
