import pygame
import os

WIDTH = 500
# 繪畫文字方塊函式


def draw_text(win, text, size, x, y, color):
    font = pygame.font.Font(os.path.join("fonts", "msjhbd.ttc"), size)
    text = font.render(text, 1, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    win.blit(text, text_rect)


