import pygame
from constant import *


class ResetButton:
    def __init__(self):
        font = pygame.font.SysFont('timesnewroman', 20)
        self.image = font.render('RESET', True, (0, 255, 0), (0, 0, 255))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75))
