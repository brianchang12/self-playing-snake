import pygame
from constant import *


class Title:
    def __init__(self, reset_title):
        reset_font = pygame.font.SysFont('timesnewroman', 30)
        self.image = reset_font.render(reset_title, False, (0, 255, 0))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
