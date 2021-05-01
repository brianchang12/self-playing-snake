import pygame

from modules.snake_app import SnakeApp

if __name__ == '__main__':
    pygame.init()
    snake_game = SnakeApp()
    running = True
    while running:
        running = snake_game.execute()
        snake_game.reset()
    pygame.quit()




