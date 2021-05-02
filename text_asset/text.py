import pygame
from constant import *


class GenerationText:
    def __init__(self, generation):
        font = pygame.font.Font(None, 20)
        self.image = font.render('Generation: ' + str(generation), True, (0, 255, 0))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 5, (SCREEN_HEIGHT - PLAYABLE_HEIGHT) / 3))


class ScoreText:
    def __init__(self, score):
        font = pygame.font.Font(None, 20)
        self.image = font.render('Generation: ' + str(score), True, (0, 255, 0))
        self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH / 5, 2 * ((SCREEN_HEIGHT - PLAYABLE_HEIGHT) / 3)))
