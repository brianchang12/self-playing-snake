from enum import Enum

import pygame
import numpy as np
from button.button import ResetButton
from constant import *
from pygame.locals import *

from sprite.apple import *
from sprite.border import *
from sprite.snake_component import SnakeComponent
from text_asset.title import Title
from modules.point import *


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class SnakeApp:

    def __init__(self):
        self.direction = Direction.UP
        self.score = 0
        self.snake_length = 3
        self.clock = pygame.time.Clock()
        self.non_head = pygame.sprite.Group()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        top_border = HorizontalBorder(x_coord=SCREEN_WIDTH / 2, y_coord=BODY_HEIGHT / 2)
        bottom_border = HorizontalBorder(x_coord=SCREEN_WIDTH / 2, y_coord=SCREEN_HEIGHT - (BODY_HEIGHT / 2))
        left_border = VerticalBorder(x_coord=BODY_WIDTH / 2, y_coord=SCREEN_HEIGHT / 2)
        right_border = VerticalBorder(x_coord=SCREEN_WIDTH - (BODY_WIDTH / 2), y_coord=SCREEN_HEIGHT / 2)
        self.borders = pygame.sprite.Group()
        self.borders.add(top_border, left_border, bottom_border, right_border)
        self.borders.draw(self.screen)
        head_tail = self._build_initial_snake()
        self.head = head_tail[0]
        self.tail = head_tail[1]
        self.non_head.add(top_border, left_border, right_border, bottom_border)
        self.snake_components = pygame.sprite.Group()
        traverse = self.head
        while traverse is not None:
            if traverse.head is False:
                self.non_head.add(traverse)
            self.snake_components.add(traverse)
            traverse = traverse.next
        self.snake_components.draw(self.screen)
        self.apple = Apple(self.snake_components)
        self.screen.blit(self.apple.image, self.apple.rect)
        pygame.display.update(self.screen.get_rect())
        self.frame_rate = 30
        self.game_iteration = 0

    @staticmethod
    def _build_initial_snake() -> tuple:
        head = SnakeComponent(head=True, speed=[0, -BODY_HEIGHT])
        head.next = SnakeComponent(speed=[0, -BODY_HEIGHT], x_coord=head.rect.center[0],
                                   y_coord=head.rect.center[1] + BODY_HEIGHT)
        head.next.next = SnakeComponent(speed=[0, -BODY_HEIGHT], x_coord=head.next.rect.center[0],
                                        y_coord=head.next.rect.center[1] + BODY_HEIGHT)
        tail = head.next.next
        return head, tail

    def execute(self):
        running = True
        while running:
            self.play_step()
            self.update_ui()
            if self.snake_length == MAX_SNAKE:
                pygame.time.delay(1000)
            self.clock.tick(self.frame_rate)

    def update_ui(self):
        self.screen.fill((0, 0, 0))
        self.borders.draw(self.screen)
        self.screen.blit(self.apple.image, self.apple.rect)
        self.snake_components.draw(self.screen)
        pygame.display.update(self.screen.get_rect())

    def reset(self):
        self.direction = Direction.UP
        self.screen.fill((0, 0, 0))
        self.game_iteration = 0
        self.score = 0
        self.snake_length = 3
        self.game_iteration = 0
        for component in self.snake_components:
            component.kill()
        head_tail = self._build_initial_snake()
        self.head = head_tail[0]
        self.tail = head_tail[1]
        traverse = self.head
        while traverse is not None:
            if traverse.head is False:
                self.non_head.add(traverse)
            self.snake_components.add(traverse)
            traverse = traverse.next
        coordinate = self.apple.randomize(self.snake_components)
        self.apple.rect = self.apple.image.get_rect(center=coordinate)
        self.borders.draw(self.screen)
        self.snake_components.draw(self.screen)
        self.screen.blit(self.apple.image, self.apple.rect)
        pygame.display.update(self.screen.get_rect())

    def play_step(self, action):
        self.game_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == APPLE_EVENT:
                self.screen.blit(self.apple.image, self.apple.rect)
                pygame.event.post(pygame.event.Event(GROW_EVENT))
                if self.frame_rate <= 3:
                    self.frame_rate += 0.2
        self.move_snake(action)
        self.update_ui()
        reward = 0
        game_over = False
        if self.collided() or self.game_iteration > 100 * self.snake_length:
            reward = -10
            game_over = True
            pygame.time.delay(300)
            return reward, game_over, self.score
        if self.head.rect.colliderect(self.apple.rect):
            coordinate = self.apple.randomize(self.snake_components)
            self.apple.rect = self.apple.image.get_rect(center=coordinate)
            pygame.event.post(pygame.event.Event(APPLE_EVENT))
            reward = 10
            self.score += 1
        return reward, game_over, self.score

    def collided(self, point=None) -> bool:
        compare_rect = self.head.rect
        if point is not None:
            compare_rect = pygame.Surface((BODY_WIDTH - 0.1, BODY_HEIGHT - 0.1)).get_rect(center=(point.x, point.y))
        for non_head_sprite in self.non_head:
            if compare_rect.colliderect(non_head_sprite.rect):
                return True
        return False

    def move_snake(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]
        self.direction = new_dir
        tail_speed = [self.tail.speed[0], self.tail.speed[1]]
        tail_x = self.tail.rect.center[0]
        tail_y = self.tail.rect.center[1]
        if self.direction == Direction.UP:
            self.head.speed[0] = 0
            self.head.speed[1] = -BODY_HEIGHT
            self.head.rect.move_ip(self.head.speed[0], self.head.speed[1])
            prev_speed = self.head.speed
            self._move_snake_helper(self.head.next, prev_speed)
        elif self.direction == Direction.LEFT:
            self.head.speed[0] = -BODY_WIDTH
            self.head.speed[1] = 0
            self.head.rect.move_ip(self.head.speed[0], self.head.speed[1])
            prev_speed = self.head.speed
            self._move_snake_helper(self.head.next, prev_speed)
        elif self.direction == Direction.RIGHT:
            self.head.speed[0] = BODY_WIDTH
            self.head.speed[1] = 0
            self.head.rect.move_ip(self.head.speed[0], self.head.speed[1])
            prev_speed = self.head.speed
            self._move_snake_helper(self.head.next, prev_speed)
        elif self.direction == Direction.DOWN:
            self.head.speed[0] = 0
            self.head.speed[1] = BODY_HEIGHT
            self.head.rect.move_ip(self.head.speed[0], self.head.speed[1])
            prev_speed = self.head.speed
            self._move_snake_helper(self.head.next, prev_speed)
        if pygame.event.peek(GROW_EVENT):
            tail_node = SnakeComponent(speed=tail_speed,
                                       x_coord=tail_x, y_coord=tail_y)
            self.tail.next = tail_node
            self.tail = tail_node
            self.snake_components.add(tail_node)
            self.non_head.add(tail_node)
            self.snake_length += 1

    def _move_snake_helper(self, node, prev_speed):
        if node is None:
            return
        else:
            speed = [node.speed[0], node.speed[1]]
            node.rect.move_ip(node.speed[0], node.speed[1])
            if prev_speed[0] != node.speed[0] and prev_speed[1] != node.speed[1]:
                node.speed[0] = prev_speed[0]
                node.speed[1] = prev_speed[1]
            self._move_snake_helper(node.next, speed)
