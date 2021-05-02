import random
import numpy as np
import pygame.time

from modules.helper import plot
from modules.point import Point
from snake_app import *
import torch
from collections import deque
from model import *
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class SnakeAgent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.head
        coordinates = head.rect.center
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]
        point_l = Point(x_coordinate - BODY_WIDTH, y_coordinate)
        point_r = Point(x_coordinate + BODY_WIDTH, y_coordinate)
        point_u = Point(x_coordinate, y_coordinate - BODY_HEIGHT)
        point_d = Point(x_coordinate, y_coordinate + BODY_HEIGHT)
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.collided(point_r)) or
            (dir_l and game.collided(point_l)) or
            (dir_u and game.collided(point_u)) or
            (dir_d and game.collided(point_d)),

            # Danger right
            (dir_u and game.collided(point_r)) or
            (dir_d and game.collided(point_l)) or
            (dir_l and game.collided(point_u)) or
            (dir_r and game.collided(point_d)),

            # Danger left
            (dir_d and game.collided(point_r)) or
            (dir_u and game.collided(point_l)) or
            (dir_r and game.collided(point_u)) or
            (dir_l and game.collided(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,
            game.apple.rect.center[0] < x_coordinate,
            game.apple.rect.center[0] > x_coordinate,
            game.apple.rect.center[1] < y_coordinate,
            game.apple.rect.center[1] > y_coordinate

        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = SnakeAgent()
    game = SnakeApp()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        pygame.time.wait(80)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)
        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()
            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    pygame.init()
    train()
    pygame.quit()
