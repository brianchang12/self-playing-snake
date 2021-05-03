import pygame
from constant import *


class TextFactory:
    @staticmethod
    def factory(input_param, val):
        localized = {
            "GenerationText": "Generation: ",
            "ScoreText": "Score: ",
            "HighScoreText": 'HighScore: '
        }
        header_str = localized[input_param]
        if input_param == "GenerationText":
            return GenerationText(header_str, val)
        elif input_param == "ScoreText":
            return ScoreText(header_str, val)
        elif input_param == "HighScoreText":
            return HighScoreText(header_str, val)


class Text:
    def __init__(self, text, val):
        self.text = text + str(val)

    def update_text(self, val):
        str_list = self.text.split()
        self.text = str_list[0] + " " + str(val)
        font = pygame.font.Font(None, 20)
        return font.render(self.text, True, (0, 255, 0))


class GenerationText(Text):
    def __init__(self, generation, val):
        super().__init__(generation, val)
        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, (0, 255, 0))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 5, (SCREEN_HEIGHT - PLAYABLE_HEIGHT) / 4))


class ScoreText(Text):
    def __init__(self, score, val):
        super().__init__(score, val)
        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, (0, 255, 0))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 5, (SCREEN_HEIGHT - PLAYABLE_HEIGHT) / 2))


class HighScoreText(Text):
    def __init__(self, high_score, val):
        super().__init__(high_score, val)
        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, (0, 255, 0))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 5, (SCREEN_HEIGHT - PLAYABLE_HEIGHT) * 0.75))
