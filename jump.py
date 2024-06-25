import pygame

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

rect = pygame.Rect(135, 220, 30, 30) 
vel = 5
jump = False
jumpCount = 0
jumpMax = 15

run = True
while run:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: 
            if not jump and event.key == pygame.K_UP:
                jump = True
                jumpCount = jumpMax

    keys = pygame.key.get_pressed()    
    rect.centerx = (rect.centerx + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel) % 300
    
    if jump:
        rect.y -= jumpCount
        if jumpCount > -jumpMax:
            jumpCount -= 1
        else:
            jump = False 

    window.fill((255, 255, 255))
    pygame.draw.rect(window, (64, 64, 64), (0, 250, 300, 100))
    pygame.draw.circle(window, (255, 0, 0), rect.center, 15)
    pygame.display.flip()

pygame.quit()
exit() 
