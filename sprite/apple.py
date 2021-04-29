import random
from constant import *


class Apple(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super(Apple, self).__init__()
        self.image = pygame.Surface((BODY_WIDTH - 0.1, BODY_HEIGHT - 0.1))
        self.image.fill((255, 0, 0))
        while True:
            coordinate = self.__randomize_coordinate()
            self.rect = self.image.get_rect(center=coordinate)
            if pygame.sprite.spritecollideany(self, sprites) is None:
                break

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

