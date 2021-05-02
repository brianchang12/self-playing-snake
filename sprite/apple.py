import random
import copy
from constant import *


class Apple(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super(Apple, self).__init__()
        self.image = pygame.Surface((BODY_WIDTH - 0.1, BODY_HEIGHT - 0.1))
        self.image.fill((255, 0, 0))
        self.coordinates = list()
        width_start = 10
        height_start = 10
        while width_start < 190:
            width_start += 20
            while height_start < 190:
                height_start += 20
                coord = (width_start, height_start)
                self.coordinates.append(coord)
            height_start = 10
        coordinate = self.randomize(sprites)
        self.rect = self.image.get_rect(center=coordinate)

    def randomize(self, sprites) -> tuple:
        copied_coordinates = copy.deepcopy(self.coordinates)
        for sprite in sprites.sprites():
            var = sprite.rect.center
            copied_coordinates.remove(var)
        max_val = len(copied_coordinates) - 1
        if max_val < 0:
            max_val = 0
        ind = random.randint(0, max_val)
        return copied_coordinates[ind]

    @staticmethod
    def __randomize_coordinate() -> tuple:
        width = random.randint(0, 800)
        while width % 20 != 0:
            width = random.randint(0, 800)
        width += 30
        height = random.randint(0, 600)
        while height % 20 != 0:
            height = random.randint(0, 600)
        height += 30
        return width, height
