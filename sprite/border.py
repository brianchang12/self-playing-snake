import pygame
from constant import *


class HorizontalBorder(pygame.sprite.Sprite):
    def __init__(self, x_coord, y_coord):
        super(HorizontalBorder, self).__init__()
        self.image = pygame.Surface((PLAYABLE_WIDTH, BODY_HEIGHT))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x_coord, y_coord))


class VerticalBorder(pygame.sprite.Sprite):
    def __init__(self, x_coord, y_coord):
        super(VerticalBorder, self).__init__()
        self.image = pygame.Surface((BODY_WIDTH, PLAYABLE_HEIGHT - (BODY_HEIGHT * 2)))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x_coord, y_coord))
