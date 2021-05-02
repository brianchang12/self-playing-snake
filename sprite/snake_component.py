import pygame

from constant import *


class SnakeComponent(pygame.sprite.Sprite):

    def __init__(self, speed, x_coord=SCREEN_WIDTH / 2, y_coord=SCREEN_HEIGHT / 2
                 , head=False):
        super(SnakeComponent, self).__init__()
        self.head = head
        self.image = pygame.Surface((BODY_WIDTH - 0.1, BODY_HEIGHT - 0.1))
        if head is True:
            self.image.fill((255, 255, 0))
        else:
            self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x_coord, y_coord))
        self.speed = speed
        self.next = None

