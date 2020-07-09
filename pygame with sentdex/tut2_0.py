import pygame
import random

pygame.init()

# default parameter
display_width = 800
display_height = 600
carImg = pygame.image.load('racecar.png')
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Hello Gamer')
clock = pygame.time.Clock()
font_style = 'comicsansms'
game_pause_value = False
game_crash_value = False

# colors
white = (255, 255, 255)
black = (0, 0, 0)
light_red = (255, 0, 0)
red = (200, 0, 0)
light_green = (0, 255, 0)
green = (0, 200, 0)
blue = (0, 0, 255)


def thing(x, y, w, h, color):
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])


class Thing:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.w, self.h])


def display_text(text, color, size=115, pos=(display_width // 2, display_height // 2)):
    sample_text = pygame.font.SysFont(font_style, size)
    text_surface = sample_text.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    gameDisplay.blit(text_surface, text_rect)


def button(msg, x, y, w, h, ac, ic, action=None):
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if x <= mouse[0] <= x+w and y <= mouse[1] <= y+h:
        Thing(x, y, w, h, ac).draw()
        if clicked[0] == 1 and action is not None:
            action()
    else:
        Thing(x, y, w, h, ic).draw()

    display_text(msg, black, size=30, pos=(x + w//2, y + h//2))


def game_crash():
    global game_crash_value
    game_crash_value = True
    while game_crash_value:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
        display_text('You Crashed', black)
        button('Restart', 150, 450, 150, 50, green, light_green, game_loop)
        button('Exit', 550, 450, 100, 50, red, light_red, quit_game)
        pygame.display.update()
        clock.tick(30)


def quit_game():
    pygame.quit()
    quit()


def game_un_pause():
    global game_pause_value
    game_pause_value = False


def game_pause():
    global game_pause_value
    game_pause_value = True
    while game_pause_value:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_pause_value = not game_pause_value
                if event.key == pygame.K_RETURN:
                    game_pause_value = not game_pause_value

        display_text('Paused', black, size=150)
        button('Continue', 150, 450, 150, 50, green, light_green, game_un_pause)
        button('Exit', 550, 450, 100, 50, red, light_red, quit_game)
        pygame.display.update()
        clock.tick(30)
        # pygame.time.delay(2000)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

        gameDisplay.fill(white)
        display_text('A bIt rAceY', black)
        button('Start', 150, 450, 100, 50, green, light_green, game_loop)
        button('Exit', 550, 450, 100, 50, red, light_red, quit_game)
        pygame.display.update()
        clock.tick(30)
        # pygame.time.delay(2000)


def game_loop():
    score = 0
    x = int(display_width * 0.45)
    y = int(display_height * 0.8)
    x_change = 0
    thing_width = 50
    thing_height = 50
    thing_start_x = random.randrange(0, (display_width - thing_width) // 50) * 50
    thing_start_y = -300
    car_width = 73
    car_height = 82
    thing_speed = 5
    things_list = [Thing(thing_start_x, thing_start_y, thing_width, thing_height, red)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 5
                if event.key == pygame.K_RIGHT:
                    x_change += 5
                if event.key == pygame.K_p:
                    game_pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        x += x_change

        if x <= 0 or x >= display_width - car_width:
            game_crash()
        for thing_in_list in things_list:
            if thing_in_list.y + thing_height >= y and thing_in_list.y <= y + car_height:
                if thing_in_list.x <= x <= thing_in_list.x + thing_in_list.w or thing_in_list.x <= x + car_width <= thing_in_list.x + thing_in_list.w or thing_in_list.x <= x + car_width//2 <= thing_in_list.x + thing_in_list.w:
                    game_crash()

            # if score % 3 == 0:
                # things_list.append(Thing(thing_start_x, thing_start_y, thing_width, thing_height, red))

        gameDisplay.fill(white)

        for thing_in_list in things_list:
            thing_in_list.y += thing_speed
            if thing_in_list.y > display_height:
                thing_in_list.y = -random.randrange(thing_height , 300)
                thing_in_list.x = random.randrange(0, (display_width - thing_width) // 50) * 50
                score += 1
                if score % 4 == 0:

                    things_list.append(Thing(thing_start_x, thing_start_y, thing_width, thing_height, red))
            # print(thing_in_list)
            thing_in_list.draw()

        gameDisplay.blit(carImg, (x, y))
        display_text(f"Score: {score}", blue, 25, (70, 30))
        pygame.display.update()
        clock.tick(60)


game_intro()
