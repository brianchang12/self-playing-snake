import pygame

from button.button import ResetButton
from constant import *
from pygame.locals import *

from sprite.apple import *
from sprite.border import *
from sprite.snake_component import SnakeComponent
from text_asset.title import Title


class SnakeApp:
    pass

    def execute(self) -> bool:
        snake_length = 3
        clock = pygame.time.Clock()
        non_head = pygame.sprite.Group()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        top_border = HorizontalBorder(x_coord=SCREEN_WIDTH / 2, y_coord=BODY_HEIGHT / 2)
        bottom_border = HorizontalBorder(x_coord=SCREEN_WIDTH / 2, y_coord=SCREEN_HEIGHT - (BODY_HEIGHT / 2))
        left_border = VerticalBorder(x_coord=BODY_WIDTH / 2, y_coord=SCREEN_HEIGHT / 2)
        right_border = VerticalBorder(x_coord=SCREEN_WIDTH - (BODY_WIDTH / 2), y_coord=SCREEN_HEIGHT / 2)
        borders = pygame.sprite.Group()
        borders.add(top_border, bottom_border, left_border, right_border)
        borders.draw(screen)
        apple_group = pygame.sprite.Group()
        head = SnakeComponent(head=True, speed=[0, -BODY_HEIGHT])
        head.next = SnakeComponent(speed=[0, -BODY_HEIGHT], x_coord=head.rect.center[0],
                                   y_coord=head.rect.center[1] + BODY_HEIGHT)
        head.next.next = SnakeComponent(speed=[0, -BODY_HEIGHT], x_coord=head.next.rect.center[0],
                                        y_coord=head.next.rect.center[1] + BODY_HEIGHT)
        tail = head.next.next
        for border in borders:
            non_head.add(border)
        traverse = head
        snake_components = pygame.sprite.Group()
        while traverse is not None:
            if traverse.head is False:
                non_head.add(traverse)
            snake_components.add(traverse)
            traverse = traverse.next
        snake_components.draw(screen)
        apple = Apple(snake_components)
        apple_group.add(apple)
        apple_group.draw(screen)
        pygame.display.update(screen.get_rect())
        frame_rate = 10
        reset_screen = True
        running = True
        reset_title = ''
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    reset_screen = False
                if event.type == APPLE_EVENT:
                    apple = Apple(snake_components)
                    apple_group.add(apple)
                    pygame.event.post(pygame.event.Event(GROW_EVENT))
                    if frame_rate <= 17:
                        frame_rate += 0.2
            keys_pressed = pygame.key.get_pressed()
            tail_speed = [tail.speed[0], tail.speed[1]]
            tail_x = tail.rect.center[0]
            tail_y = tail.rect.center[1]
            if keys_pressed[K_UP] and head.speed[0] != 0:
                head.speed[0] = 0
                head.speed[1] = -BODY_HEIGHT
                head.rect.move_ip(head.speed[0], head.speed[1])
                prev_speed = head.speed
                self.updater(head.next, prev_speed)
            elif keys_pressed[K_LEFT] and head.speed[1] != 0:
                head.speed[0] = -BODY_WIDTH
                head.speed[1] = 0
                head.rect.move_ip(head.speed[0], head.speed[1])
                prev_speed = head.speed
                self.updater(head.next, prev_speed)
            elif keys_pressed[K_RIGHT] and head.speed[1] != 0:
                head.speed[0] = BODY_WIDTH
                head.speed[1] = 0
                head.rect.move_ip(head.speed[0], head.speed[1])
                prev_speed = head.speed
                self.updater(head.next, prev_speed)
            elif keys_pressed[K_DOWN] and head.speed[0] != 0:
                head.speed[0] = 0
                head.speed[1] = BODY_HEIGHT
                head.rect.move_ip(head.speed[0], head.speed[1])
                prev_speed = head.speed
                self.updater(head.next, prev_speed)
            else:
                head.rect.move_ip(head.speed[0], head.speed[1])
                prev_speed = head.speed
                self.updater(head.next, prev_speed)
            if pygame.event.peek(GROW_EVENT):
                tail_node = SnakeComponent(speed=tail_speed,
                                           x_coord=tail_x, y_coord=tail_y)
                tail.next = tail_node
                tail = tail_node
                snake_components.add(tail_node)
                non_head.add(tail_node)
                snake_length += 1
            screen.fill((0, 0, 0))
            borders.draw(screen)
            apple_group.draw(screen)
            snake_components.draw(screen)
            pygame.display.update(screen.get_rect())
            if pygame.sprite.spritecollideany(head, non_head) is not None:
                pygame.time.delay(300)
                running = False
                reset_title = "GAME OVER"
            if pygame.sprite.spritecollideany(head, apple_group) is not None:
                pygame.sprite.spritecollideany(head, apple_group).kill()
                pygame.event.post(pygame.event.Event(APPLE_EVENT))
            if snake_length == MAX_SNAKE:
                pygame.time.delay(300)
                running = False
                reset_title = "CONGRATULATIONS, YOU WON"
            clock.tick(frame_rate)
        snake_components.empty()
        non_head.empty()
        borders.empty()
        apple_group.empty()
        screen.fill((0, 0, 0))
        title = Title(reset_title)
        screen.blit(title.image, title.rect)
        button = ResetButton()
        screen.blit(button.image, button.rect)
        pygame.display.update(screen.get_rect())
        ret = False
        while reset_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    reset_screen = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    mouse_x = mouse[0]
                    mouse_y = mouse[1]
                    if mouse_x >= button.rect.topleft[0] and mouse_x <= button.rect.topright[0] and mouse_y >= button.rect.topleft[1] and mouse_y <= button.rect.bottomleft[1]:
                        reset_screen = False
                        ret = True
        return ret

    def updater(self, node, prev_speed):
        if node is None:
            return
        else:
            speed = [node.speed[0], node.speed[1]]
            node.rect.move_ip(node.speed[0], node.speed[1])
            if prev_speed[0] != node.speed[0] and prev_speed[1] != node.speed[1]:
                node.speed[0] = prev_speed[0]
                node.speed[1] = prev_speed[1]
            self.updater(node.next, speed)
