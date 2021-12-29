from pygame import *
from pygame.sprite import *
import sys
from tkinter import *
from tkinter import messagebox

sys.path.insert(1, r'C:\Users\User\Desktop\NDU\Python_NDU_course\slimecrusher\slimecrusher.py')

pygame.init()

clock = time.Clock()

WIDTH = 1080
HEIGHT = 720

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Slime Crusher")

mixer.music.load('sound/audio.wav')
mixer.music.play(-1)

#adding a background imagea
bg_im = pygame.image.load("images/menu_bg.jpg")

#Text font
title_font = font.SysFont('Arial', 90)
options_font = font.SysFont('Arial', 50)

title1 = title_font.render("Slime", True, (255, 255, 255))
title2 = title_font.render("Crusher", True, (255, 255, 255))

start_text = options_font.render("START", True, (255, 255, 255))
start_rect = start_text.get_rect()

help_text = options_font.render("HELP", True, (255, 255, 255))
help_rect = help_text.get_rect()

quit_text = options_font.render("QUIT", True, (255, 255, 255))
quit_rect = quit_text.get_rect()

button_color = (50, 50, 50)


while True:
    e = event.wait()
    mousePos = mouse.get_pos()
    
    if e.type == QUIT:
        pygame.quit()
        break

    if e.type == MOUSEBUTTONDOWN and e.button == 1:
        mousePos = mouse.get_pos()
        if 430 < mousePos[0] < 600 and 560 < mousePos[1] < 620:
            Tk().wm_withdraw()
            isYes = messagebox.askyesno("Exit", "Are you sure you want to exit?")
            if isYes:
                pygame.quit()
                break

    if e.type == MOUSEBUTTONDOWN and e.button == 1:
        mousePos = mouse.get_pos()
        if 430 < mousePos[0] < 600 and 400 < mousePos[1] < 460:
            import slimecrusher
            pygame.quit()


    screen.blit(bg_im, (0, 0))

    draw.rect(screen, button_color, [430, 400, 170, 60])
    draw.rect(screen, button_color, [430, 480, 170, 60])
    draw.rect(screen, button_color, [430, 560, 170, 60])

    screen.blit(title1, (440, 150))
    screen.blit(title2, (400, 250))

    screen.blit(start_text, (450, 400))
    screen.blit(help_text, (450, 480))
    screen.blit(quit_text, (450, 560))

    if e.type == MOUSEBUTTONDOWN and e.button == 1:
        mousePos = mouse.get_pos()
        if 430 < mousePos[0] < 600 and 480 < mousePos[1] < 540:
            draw.rect(screen, button_color, [700, 100, 400, 600])
            screen.blit(options_font.render("Move: WASD", True, (255, 255, 255)), (700, 200))
            screen.blit(options_font.render("Mute: M", True, (255, 255, 255)), (700, 280))
            screen.blit(options_font.render("Shoot: Left-Click", True, (255, 255, 255)), (700, 360))
            screen.blit(options_font.render("Exit: ESC", True, (255, 255, 255)), (700, 440))

    display.update()
    clock.tick(60)
