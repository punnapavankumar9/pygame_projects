import pygame
import random
import time

# default parameters
pygame.init()
display_size = 500
gameDisplay = pygame.display.set_mode((display_size, display_size))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font_style = 'comicsansms'
rows = 25
cell_size = display_size // rows
pause = False
crash = False

# colors
white = (255, 255, 255)
light_white = (175, 175, 175)
black = (0, 0, 0)
red = (255, 0, 0)
thick_red = (200, 0, 0)
green = (0, 255, 0)
thick_green = (0, 200, 0)
blue = (0, 0, 255)


def game_quit():
    pygame.quit()
    quit()


def un_pause():
    global pause
    pause = False


def display_text(text, color, size=115, pos=(display_size // 2, display_size // 2)):
    sample_text = pygame.font.SysFont(font_style, size)
    text_surface = sample_text.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    gameDisplay.blit(text_surface, text_rect)


def cube(x, y, color):
    pygame.draw.rect(gameDisplay, color, [x + 2, y + 2, cell_size - 3, cell_size - 3])
    # pygame.draw.rect(gameDisplay, color, [x + 2, y + 2, cell_size-3, cell_size-3])


def button(text, text_color, x, y, w, h, ac, ic, action=None):
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
        color = ac
        if clicked[0] == 1 and action is not None:
            action()
    else:
        color = ic
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])
    display_text(text, text_color, size=25, pos=(x + w // 2, y + h // 2))


def game_crashed():
    global crash
    crash = True
    while crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        display_text('Game Over', red, size=90)
        button('Restart', black, 50, 350, 100, 50, green, thick_green, game_loop)
        button('Exit', black, 350, 350, 100, 50, green, thick_green, game_quit)
        pygame.display.update()
        clock.tick(30)


def game_paused():
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause

        display_text('Paused', red, size=90)
        button('Continue', black, 50, 350, 100, 50, green, thick_green, un_pause)
        button('Exit', black, 350, 350, 100, 50, green, thick_green, game_quit)
        pygame.display.update()
        clock.tick(30)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

        display_text('Snake Game', blue, size=90)
        button('Start', black, 50, 350, 100, 50, green, thick_green, game_loop)
        button('Exit', black, 350, 350, 100, 50, green, thick_green, game_quit)
        pygame.display.update()
        clock.tick(30)


def food(x, y):
    cube(x, y, red)


def draw_snake(snake_x, snake_y):
    cube(snake_x, snake_y, green)


def draw_grid():
    global cell_size, display_size
    x = 0
    y = 0
    for i in range(rows):
        x += cell_size
        y += cell_size

        pygame.draw.line(gameDisplay, light_white, (x, 0), (x, display_size))
        pygame.draw.line(gameDisplay, light_white, (0, y), (display_size, y))


def game_loop():
    global cell_size, crash
    snake_cells = []
    snake_x = random.randrange(0, rows) * cell_size
    snake_y = random.randrange(0, rows) * cell_size
    score = 0

    # x_change = 0
    # y_change = 0
    food_x = random.randrange(0, rows) * cell_size
    food_y = random.randrange(0, rows) * cell_size
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dir_x, dir_y = random.choice(directions)
    while True:
        pop_value = True
        pygame.time.delay(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused()
                if event.key == pygame.K_LEFT and (dir_x != 1 and dir_y != 0):
                    dir_x += -1
                    dir_y = 0
                elif event.key == pygame.K_RIGHT and (dir_x != -1 and dir_y != 0):
                    dir_x += 1
                    dir_y = 0
                elif event.key == pygame.K_UP and (dir_x != 0 and dir_y != 1):
                    dir_x = 0
                    dir_y += -1
                elif event.key == pygame.K_DOWN and (dir_x != 0 and dir_y != -1):
                    dir_x = 0
                    dir_y += 1

        x_change = dir_x * cell_size
        y_change = dir_y * cell_size
        snake_x += x_change
        snake_y += y_change

        if snake_x > display_size - cell_size:
            snake_x = 0
        if snake_x < 0:
            snake_x = display_size - cell_size
        if snake_y > display_size - cell_size:
            snake_y = 0
        if snake_y < 0:
            snake_y = display_size - cell_size

        if food_x == snake_x and food_y == snake_y:
            food_x = random.randrange(0, rows) * cell_size
            food_y = random.randrange(0, rows) * cell_size
            score += 1
            pop_value = False

        snake_cells.append([snake_x, snake_y])
        gameDisplay.fill(black)
        draw_grid()
        food(food_x, food_y)
        for i, cell in enumerate(snake_cells):
            draw_snake(cell[0], cell[1])
            if snake_cells[0] == snake_cells[i] and i != 0:
                game_crashed()
        if pop_value:
            snake_cells.pop(0)
        else:
            pass
        pygame.display.update()
        clock.tick(15)


game_intro()
