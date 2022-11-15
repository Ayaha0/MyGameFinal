
from func import *
# 初始化面設計


WIDTH = 500
HEIGHT = 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CADMIUM_YELLOW = (253, 218, 13)
RED = (255, 0, 0)

def draw_init(clock, win, background_img):
    
    while True:
        clock.tick(FPS)
        win.fill(BLACK)
        win.blit(background_img, (0, 0))
        draw_text(win, "這啥鬼遊戲?", 50, WIDTH/2, 100, CADMIUM_YELLOW)
        draw_text(win, "按E看玩法", 30, WIDTH/2, 200, WHITE)
        draw_text(win, "按Q看開發人員資訊", 30, WIDTH/2, 300, WHITE)
        draw_text(win, "ENTER鍵開始遊戲", 30, WIDTH/2, 400, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_RETURN]:
                    return True
                if key_pressed[pygame.K_e]:
                    if draw_rule(clock, win, background_img) == False:
                        return False
                if key_pressed[pygame.K_q]:
                    if draw_developer(clock, win, background_img) == False:
                        return False
        pygame.display.update()

# 顯示遊戲規則


def draw_rule(clock, win, background_img):
    while True:
        clock.tick(FPS)
        win.fill(BLACK)
        win.blit(background_img, (0, 0))
        draw_text(win, "規則規則", 30, WIDTH/2, 100, WHITE)
        draw_text(win, "規則規則", 30, WIDTH/2, 200, WHITE)
        draw_text(win, "規則規則", 30, WIDTH/2, 300, WHITE)
        draw_text(win, "規則規則", 30, WIDTH/2, 400, WHITE)
        draw_text(win, "規則規則", 30, WIDTH/2, 500, WHITE)
        draw_text(win, "規則規則", 30, WIDTH/2, 600, WHITE)
        draw_text(win, "按ESC回上一頁", 30, WIDTH/2, 700, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_ESCAPE]:
                    return True

        pygame.display.update()

# 顯示開發人員


def draw_developer(clock, win, background_img):
    while True:
        clock.tick(FPS)
        win.fill(BLACK)
        win.blit(background_img, (0, 0))
        draw_text(win, "開發人員", 30, WIDTH/2, 100, WHITE)
        draw_text(win, "開發人員", 30, WIDTH/2, 200, WHITE)
        draw_text(win, "開發人員", 30, WIDTH/2, 300, WHITE)
        draw_text(win, "開發人員", 30, WIDTH/2, 400, WHITE)
        draw_text(win, "開發人員", 30, WIDTH/2, 500, WHITE)
        draw_text(win, "開發人員", 30, WIDTH/2, 600, WHITE)
        draw_text(win, "按ESC回上一頁", 30, WIDTH/2, 700, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_ESCAPE]:
                    return True

        pygame.display.update()
