import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Snake settings
snake_size = 20
snake_speed = 15
snake_pos = [[100, 50], [90, 50], [80, 50]]

# Food settings
food_size = 20
food_pos = [random.randrange(1, (screen_width // 20)) * 20, random.randrange(1, (screen_height // 20)) * 20]
food_spawn = True

# Clock settings
clock = pygame.time.Clock()


def game_over():
    pygame.quit()
    sys.exit()


direction = 'RIGHT'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    if direction == 'UP':
        snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - 20])
    if direction == 'DOWN':
        snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + 20])
    if direction == 'LEFT':
        snake_pos.insert(0, [snake_pos[0][0] - 20, snake_pos[0][1]])
    if direction == 'RIGHT':
        snake_pos.insert(0, [snake_pos[0][0] + 20, snake_pos[0][1]])

    # Snake collisions
    if snake_pos[0][0] >= screen_width or snake_pos[0][0] < 0 or snake_pos[0][1] >= screen_height or snake_pos[0][
        1] < 0:
        game_over()
    for block in snake_pos[1:]:
        if snake_pos[0] == block:
            game_over()

    # Food collision
    if snake_pos[0] == food_pos:
        food_spawn = False
    else:
        snake_pos.pop()

    # Spawn food
    if not food_spawn:
        food_pos = [random.randrange(1, (screen_width // 20)) * 20, random.randrange(1, (screen_height // 20)) * 20]
        food_spawn = True

    # Draw snake and food
    screen.fill(white)
    for pos in snake_pos:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], snake_size, snake_size))
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], food_size, food_size))

    pygame.display.flip()
    clock.tick(snake_speed)
