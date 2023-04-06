#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
from time import sleep

import pygame
import sys
import random


class SnakeGame:
    def __init__(self):
        pygame.init()
        
        self.WIDTH = 640*2
        self.HEIGHT = 480*2
        self.CELL_SIZE = 20
        self.COLUMNS = self.WIDTH // self.CELL_SIZE
        self.ROWS = self.HEIGHT // self.CELL_SIZE
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        self.SNAKE_1_COLOR = (193, 205, 193)
        self.SNAKE_2_COLOR = (255, 193, 193)
        self.FOOD_COLOR = (152, 251, 152)

        self.FPS = 10

        self.score = 0
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()

        self.INITIAL_SNAKE_LENGTH = 3  # 蛇的初始长度
        self.controls = [
            (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
            (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        ]
        self.INITIAL_SNAKE_COUNT = 2  # 蛇的数量
        self.snakes = self.create_snakes()

        self.FOOD_TIMER_DURATION = 10000  # 设置食物定时器的持续时间，单位为毫秒
        self.FOOD_FLASH_DURATION = 2000  # 设置食物闪烁时间，单位为毫秒
        self.FOOD_FLASH_FREQUENCY = 300  # 设置食物闪烁频率，单位为毫秒
        self.FOOD_COUNT = 3  # 设置同时存在的食物数量

        self.food_timers = []  # 使用列表跟踪食物及其定时器
        for _ in range(self.FOOD_COUNT):
            self.create_food()
        
    def get_random_position(self, existing_snakes, min_distance=10):
        while True:
            x = random.randrange(1, self.WIDTH // self.CELL_SIZE - 1) * self.CELL_SIZE
            y = random.randrange(1, self.HEIGHT // self.CELL_SIZE - 1) * self.CELL_SIZE
            position = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)

            if not existing_snakes:  # 如果蛇列表为空，直接返回位置
                return position
            
            if all(self.distance_between(position, snake.body[0]) >= min_distance for snake in existing_snakes):
                return position
            
    @staticmethod
    def distance_between(rect1, rect2):
        return math.sqrt((rect1.x - rect2.x) ** 2 + (rect1.y - rect2.y) ** 2)

    def create_snakes(self):
        existing_snakes = []
        colors = [self.SNAKE_1_COLOR, self.SNAKE_2_COLOR]  # Snake colors
        for i in range(self.INITIAL_SNAKE_COUNT):
            new_snake = Snake(self, self.get_random_position(existing_snakes), colors[i % len(colors)],
                              self.controls[i])
            existing_snakes.append(new_snake)
        return existing_snakes
    
    def create_food(self):
        while True:
            food = pygame.Rect(
                random.randint(1, self.COLUMNS - 2) * self.CELL_SIZE,
                random.randint(1, self.ROWS - 2) * self.CELL_SIZE,
                self.CELL_SIZE,
                self.CELL_SIZE,
            )

            if not any(snake.collides_with(food) for snake in self.snakes):
                break
                    
        self.food_timers.append((food, pygame.time.get_ticks() + self.FOOD_TIMER_DURATION))
    
    def start_screen(self):
        self.screen.fill(self.BLACK)
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Snake Game", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
        
        instructions_font = pygame.font.Font(None, 36)
        instructions_text = instructions_font.render("Press any key to start", True, self.WHITE)
        instructions_rect = instructions_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT * 2 // 3))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(instructions_text, instructions_rect)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    waiting = False
    
    def end_screen(self):
        self.screen.fill(self.BLACK)
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Game Over", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f" Your score: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4 + 50))
        
        instructions_font = pygame.font.Font(None, 36)
        instructions_text = instructions_font.render("Press any key to play again", True, self.WHITE)
        instructions_rect = instructions_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT * 3 // 4))
        
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render("Quit", True, self.BLACK)
        button_rect = pygame.Rect(self.WIDTH // 2 - 50, self.HEIGHT // 2 - 25, 100, 50)
        pygame.draw.rect(self.screen, self.RED, button_rect)
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(instructions_text, instructions_rect)
        self.screen.blit(button_text, (button_rect.x + 25, button_rect.y + 10))
        pygame.display.flip()
        
        sleep(1)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit()
                
                if event.type == pygame.KEYUP:
                    self.__init__()
                    self.restart()
                    running = False

    def run(self, show_start=True):
        if show_start:
            self.start_screen()
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                for snake in self.snakes:
                    snake.control_direction(event)

            for snake in self.snakes:
                snake.move()
            
            if any(snake.check_collision() for snake in self.snakes):
                self.end_screen()
                break

            current_time = pygame.time.get_ticks()
            for food, timer in self.food_timers:
                if current_time >= timer:
                    self.food_timers.remove((food, timer))
                    self.create_food()

            self.screen.fill(self.BLACK)
            for snake in self.snakes:
                snake.draw(self.screen)
            
            for food, timer in self.food_timers:
                remaining_time = timer - current_time
                if remaining_time > self.FOOD_FLASH_DURATION or (remaining_time // self.FOOD_FLASH_FREQUENCY) % 2 == 0:
                    pygame.draw.rect(self.screen, self.FOOD_COLOR, food)
        
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def restart(self):
        self.__init__()
        self.run(False)
    
    
class Snake:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    def __init__(self, snake_game, initial_position, color, control_keys):
        self.game = snake_game
        self.body = [pygame.Rect(initial_position.x - i * self.game.CELL_SIZE,
                                 initial_position.y,
                                 self.game.CELL_SIZE,
                                 self.game.CELL_SIZE)
                     for i in range(self.game.INITIAL_SNAKE_LENGTH)]
        self.color = color
        self.control_keys = control_keys
        self.direction = self.RIGHT
    
    def move(self):
        """
        move()方法首先计算蛇头的新位置，然后检查是否碰到食物。如果碰到食物，就移除食物，增加分数，并创建新的食物。否则，移除蛇的尾部。最后，将新的头部添加到蛇身体的前端。
        :return:
        """
        # 计算新的头部位置
        new_head_x = self.body[0].x + self.direction[0] * self.game.CELL_SIZE
        new_head_y = self.body[0].y + self.direction[1] * self.game.CELL_SIZE
        new_head = pygame.Rect(new_head_x, new_head_y, self.game.CELL_SIZE, self.game.CELL_SIZE)

        # 检查是否吃到食物
        eaten_food_index = None
        for index, (food, timer) in enumerate(self.game.food_timers):
            if new_head.colliderect(food):
                eaten_food_index = index
                break

        if eaten_food_index is not None:
            self.game.food_timers.pop(eaten_food_index)
            self.game.create_food()
            self.game.score += 1
        else:
            self.body.pop()

        self.body.insert(0, new_head)

    def check_collision(self):
        print(self.body[0])
        return (
            self.body[0].x < 0
            or self.body[0].x >= self.game.WIDTH
            or self.body[0].y < 0
            or self.body[0].y >= self.game.HEIGHT
            or any(self.body[0].colliderect(part) for part in self.body[1:])
        )

    def collides_with(self, rect):
        for segment in self.body:
            if segment.colliderect(rect):
                return True
        return False

    def draw(self, screen):
        for part in self.body:
            pygame.draw.rect(screen, self.color, part)

    def control_direction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.control_keys[0] and self.direction != self.DOWN:
                self.direction = self.UP
            elif event.key == self.control_keys[1] and self.direction != self.UP:
                self.direction = self.DOWN
            elif event.key == self.control_keys[2] and self.direction != self.RIGHT:
                self.direction = self.LEFT
            elif event.key == self.control_keys[3] and self.direction != self.LEFT:
                self.direction = self.RIGHT
    

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
