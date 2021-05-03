from enum import Enum

import numpy as np
import pygame

from sprite.apple import *
from sprite.border import *
from sprite.snake_component import SnakeComponent
from text_asset.text import GenerationText, ScoreText, TextFactory


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
        self.playable_space = pygame.Surface((PLAYABLE_WIDTH, PLAYABLE_HEIGHT))
        self.playable_space.fill((0, 0, 0))
        top_border = HorizontalBorder(x_coord=PLAYABLE_WIDTH / 2, y_coord=BODY_HEIGHT / 2)
        bottom_border = HorizontalBorder(x_coord=PLAYABLE_WIDTH / 2, y_coord=PLAYABLE_HEIGHT - (BODY_HEIGHT / 2))
        left_border = VerticalBorder(x_coord=BODY_WIDTH / 2, y_coord=PLAYABLE_HEIGHT / 2)
        right_border = VerticalBorder(x_coord=PLAYABLE_WIDTH - (BODY_WIDTH / 2), y_coord=PLAYABLE_HEIGHT / 2)
        self.borders = pygame.sprite.Group()
        self.borders.add(top_border, left_border, bottom_border, right_border)
        self.borders.draw(self.playable_space)
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
        self.snake_components.draw(self.playable_space)
        self.apple = Apple(self.snake_components)
        self.playable_space.blit(self.apple.image, self.apple.rect)
        self.text_space = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - PLAYABLE_HEIGHT))
        self.text_space_rect = self.text_space.get_rect(topleft=(0, PLAYABLE_HEIGHT))
        self.gen = 1
        self.high_score = 0
        self.text_space.fill((0, 0, 0))
        self.factory = TextFactory()
        self.gen_text = self.factory.factory("GenerationText", self.gen)
        self.score_text = self.factory.factory("ScoreText", self.score)
        self.high_score_text = self.factory.factory("HighScoreText", self.high_score)
        self.text_space.blit(self.gen_text.image, self.gen_text.rect)
        self.text_space.blit(self.score_text.image, self.score_text.rect)
        self.text_space.blit(self.high_score_text.image, self.high_score_text.rect)
        self.screen.blit(self.playable_space, self.playable_space.get_rect(topleft=(0, 0)))
        self.screen.blit(self.text_space, self.text_space_rect)
        pygame.display.update()
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
        self.playable_space.fill((0, 0, 0))
        self.borders.draw(self.playable_space)
        self.playable_space.blit(self.apple.image, self.apple.rect)
        self.snake_components.draw(self.playable_space)
        self.screen.blit(self.playable_space, self.playable_space.get_rect(topleft=(0, 0)))
        pygame.display.update(self.playable_space.get_rect())

    def reset(self):
        self.direction = Direction.UP
        self.playable_space.fill((0, 0, 0))
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
        self.screen.blit(self.text_space, self.text_space.get_rect(topleft=(0, PLAYABLE_HEIGHT)))
        self.apple.rect = self.apple.image.get_rect(center=coordinate)
        self.borders.draw(self.playable_space)
        self.snake_components.draw(self.playable_space)
        self.playable_space.blit(self.apple.image, self.apple.rect)
        self.screen.blit(self.playable_space, self.playable_space.get_rect(topleft=(0, 0)))

        self.text_space.fill((0, 0, 0))
        self.gen_text.image = self.gen_text.update_text(self.gen)
        self.score_text.image = self.score_text.update_text(self.score)
        self.text_space.blit(self.score_text.image, self.score_text.rect)
        self.text_space.blit(self.gen_text.image, self.gen_text.rect)
        self.text_space.blit(self.high_score_text.image, self.high_score_text.rect)
        self.screen.blit(self.text_space, self.text_space.get_rect(topleft=(0, PLAYABLE_HEIGHT)))
        pygame.display.update()

    def play_step(self, action):
        self.game_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == APPLE_EVENT:
                self.playable_space.blit(self.apple.image, self.apple.rect)
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
            pygame.time.delay(100)
            self.gen += 1
            return reward, game_over, self.score
        elif self.head.rect.colliderect(self.apple.rect):
            coordinate = self.apple.randomize(self.snake_components)
            self.apple.rect = self.apple.image.get_rect(center=coordinate)
            pygame.event.post(pygame.event.Event(APPLE_EVENT))
            reward = 10
            self.score += 1
            self.text_space.fill((0, 0, 0))
            self.score_text.image = self.score_text.update_text(self.score)
            self.text_space.blit(self.gen_text.image, self.gen_text.rect)
            self.text_space.blit(self.score_text.image, self.score_text.rect)
            if self.score > self.high_score:
                self.high_score = self.score
                self.high_score_text.image = self.high_score_text.update_text(self.high_score)
            self.text_space.blit(self.high_score_text.image, self.high_score_text.rect)
            self.screen.blit(self.text_space, self.text_space.get_rect(topleft=(0, PLAYABLE_HEIGHT)))
            pygame.display.update(pygame.display.update(self.text_space_rect))
        if self.score == MAX_SNAKE - 3:
            game_over = True
        return reward, game_over, self.score

    def collided(self, point=None) -> bool:
        compare_rect = self.head.rect
        if point is not None:
            compare_rect = pygame.Surface((BODY_WIDTH - 0.1, BODY_HEIGHT - 0.1)).get_rect(center=(point[0], point[1]))
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
