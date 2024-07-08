import pygame

WHITE = (255, 255, 255)

coinIdSet = {0}
score = 0


def coins(width, height, padding, coinId):
    if coinId in coinIdSet:
        return
    coin_img = pygame.image.load("assets/coin.png")
    coin_rect = coin_img.get_rect()
    coin_rect.topleft = (width, height - padding)
    return coin_img, coin_rect, coinId


def updateScoreCount(coinId: int = 0, resetScore: bool = False):
    if resetScore:
        coinIdSet.clear()
        coinIdSet.add(0)

    global score
    if coinId in coinIdSet:
        score = (len(coinIdSet) - 1) * 100
    else:
        if coinId != 0:
            coinIdSet.add(coinId)

    font = pygame.font.Font(None, 70)
    text = font.render(f"Score: {score}", True, WHITE)
    text_rect = text.get_rect()
    text_rect.topleft = (20, 30)
    return text, text_rect


def bomb(width, height, padding):
    moving_obj_img = pygame.image.load("assets/bomb.png")
    moving_obj_rect = moving_obj_img.get_rect()
    moving_obj_rect.topleft = (width, height - padding)
    return moving_obj_img, moving_obj_rect


def game_over_check(width, height, game_over, window):
    if game_over:
        font = pygame.font.Font(None, 120)
        font1 = pygame.font.Font(None, 50)
        game_over_text = font.render("Game Over", True, (102, 43, 40))
        game_press_enter_to_continue = font1.render(f"Score:{(len(coinIdSet) - 1) * 100}", True, (102, 43, 40))
        window.blit(game_over_text,
                    (width // 2 - game_over_text.get_width() // 2, height // 3 - game_over_text.get_height() // 2))
        window.blit(game_press_enter_to_continue, (width // 2 - game_press_enter_to_continue.get_width() // 2,
                                                   (height // 3) + 50 - game_press_enter_to_continue.get_height() // 2))


class GameComponent:
    pass
