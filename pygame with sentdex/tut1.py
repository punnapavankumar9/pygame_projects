import time
import random
import pygame

pygame.init()
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Hello Gamer')
clock = pygame.time.Clock()
font_style = "comicsansms"
pause = False
carImg = pygame.image.load('racecar.png')

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0,255, 0]

thick_green = [0, 200, 0]
thick_red = [200, 0, 0]


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


class TextOnScreen:
    def __init__(self, text, pos=(int(displayWidth/2), int(displayHeight/2)), size=115):
        self.text = text
        self.pos = pos
        self.size = size

    def get_printed(self):
        large_text = pygame.font.SysFont(font_style, self.size)
        text_surface, text_rect = large_text.render(self.text, True, black), large_text.render(self.text, True, black).get_rect()
        text_rect.center = (self.pos[0], self.pos[1])
        gameDisplay.blit(text_surface, text_rect)


def thing(start_x, start_y, thing_width, thing_height, color):
    pygame.draw.rect(gameDisplay, color, [start_x, start_y, thing_width, thing_height])


def things_dodged(count):
    font = pygame.font.SysFont(font_style, 25)
    text = font.render('Dodged: ' + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def display_message(text):

    # large_text = pygame.font.SysFont(font_style, 50)
    # text_surface, text_rect = large_text.render(text, True, black), large_text.render(text, True, black).get_rect()
    # text_rect.center = (int(displayWidth/2), int(displayHeight/2))
    # gameDisplay.blit(text_surface, text_rect)
    TextOnScreen(text).get_printed()

    pygame.display.update()
    time.sleep(2)

    game_loop()


def crash(text):
    display_message(text)


def button(msg, btn_text_size, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
        thing(x, y, w, h, ac)
        if clicked[0] == 1 and action != None:
            action()
    else:
        thing(x, y, w, h, ic)

    TextOnScreen(msg, size=btn_text_size, pos=(x+int(w/2), y+int(h/2))).get_printed()


def quit_func():
    pygame.quit()
    quit()


def un_pause():
    global pause
    pause = False


def game_pause():
    global pause

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause

        # gameDisplay.fill(white)

        TextOnScreen('Paused').get_printed()

        button('Continue', 25, 150, 400, 100, 50, green, thick_green, un_pause)
        button('Exit', 25, 530, 400, 100, 50, red, thick_red, quit_func)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        TextOnScreen('A Bit Racey').get_printed()

        button('Start', 25, 150, 400, 100, 50, green, thick_green, game_loop)
        button('Exit', 25, 530, 400, 100, 50, red, thick_red, quit_func)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    x = int(displayWidth * .45)
    y = int(displayHeight * .8)
    x_change = 0
    car_height = 82
    car_width = 73
    car_speed = 5

    thing_start_x = random.randrange(0, displayWidth)
    thing_start_y = -600
    thing_width = 50
    thing_height = 50
    dodged = 0
    color = red
    thing_speed = 5

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -car_speed

                if event.key == pygame.K_RIGHT:
                    x_change = +car_speed

                if event.key == pygame.K_p:
                    global pause
                    pause = True
                    game_pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        if x <= 0 or x >= displayWidth - car_width:
            crash('You Crashed')

        if thing_start_y > displayHeight:
            thing_start_y = 0 - thing_height
            thing_start_x = random.randrange(0, displayWidth)
            dodged += 1
            thing_speed += 1
            thing_width += int(dodged * 1.2)

        x += x_change
        gameDisplay.fill(white)

        thing(thing_start_x, thing_start_y, thing_width, thing_height, color)
        thing_start_y += thing_speed
        car(x, y)
        things_dodged(dodged)

        if y < thing_start_y + thing_height:
            if thing_start_x < x < thing_start_x + thing_width or thing_start_x < x + car_width < thing_start_x + thing_width or thing_start_x + thing_width / 2 < x + (car_width / 2) < thing_start_x + thing_width / 2:
                crash('You Crashed')

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()

quit()




