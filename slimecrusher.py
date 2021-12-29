from pygame import *
import pygame
from pygame.sprite import *
import random
import math

#Initialize the pygame display module
pygame.init()
#key.set_repeat(10)

#defining variables for width and height for later use
WIDTH = 1080
HEIGHT = 720
FPS = 60


#Setting the display window with clock
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Slime Crusher")
clock = pygame.time.Clock()

#Loading sound
mixer.music.load('sound/audio.wav')
mixer.music.play(-1)
muted = False

#adding a background image
bg_im = pygame.image.load("images/bg_5.jpg").convert()

#adding score and health point text
my_font = font.SysFont(None, 36)
score_text = my_font.render("Score:", True, (153, 0, 0))
score = 0
my_score = my_font.render(str(score), True, (153, 0, 0))

hp_text = my_font.render("HP:", True, (0, 204, 0))
hp = 200
my_hp = my_font.render(str(hp), True, (0, 255, 0))

gameover_font = font.SysFont('Arial', 90)
game_text = gameover_font.render("Game", True, (255, 255, 255))
over_text = gameover_font.render("Over", True, (255, 255, 255))

#Creating game classes
class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.load("images/shooter_top.gif").convert()
        self.image = transform.scale(self.image, (50, 50))
        self.Xposition = 450
        self.Yposition = 360
        self.rect = self.image.get_rect().move(self.Xposition, self.Yposition)

    def updateLeft(self):
        self.rect = self.rect.move(-2, 0)

    def updateRight(self):
        self.rect = self.rect.move(2, 0)

    def updateUp(self):
        self.rect = self.rect.move(0, -2)

    def updateDown(self):
        self.rect = self.rect.move(0, 2)

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.load("images/tower.gif").convert()
        self.image = transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect().move(x, y)
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        edi = [pygame.image.load("images/s1_1.png"), pygame.image.load("images/s2_1.png"), pygame.image.load("images/s3_1.png"), pygame.image.load("images/s4_1.png"), pygame.image.load("images/s5.png")]
        rc = random.choice(edi)
        self.image = rc.convert_alpha()
        self.image = transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.spawn()
             
    def spawn(self):
        self.direction = random.randrange(4)
        if self.direction == 0:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.Xspeed = 0
            self.Yspeed = random.randrange(1, 4)
        elif self.direction == 1:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(HEIGHT, HEIGHT + 6)
            self.Xspeed = 0 
            self.Yspeed = -random.randrange(1, 4)
        elif self.direction == 2:
            self.rect.x = random.randrange(-100, -40)
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.Xspeed = random.randrange(1, 4)
            self.Yspeed = 0
        elif self.direction == 3:
            self.rect.x = random.randrange(WIDTH, WIDTH +60)
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.Xspeed = -random.randrange(1, 4)
            self.Yspeed = 0

    def update(self):
        self.rect.x += self.Xspeed
        self.rect.y += self.Yspeed

        if self.direction == 0:
            if self.rect.top > HEIGHT + 10:
                self.spawn()
        elif self.direction == 1:
            if self.rect.bottom < -10:
                self.spawn()
        elif self.direction == 2:
            if self.rect.left > WIDTH + 10:
                self.spawn()
        elif self.direction == 3:
            if self.rect.right < -10:
                self.spawn()

class Ammo(pygame.sprite.Sprite):
    def __init__(self, sx, sy, dx, dy, Vel):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((8, 6))
        #pygame.draw.ellipse(self.image, (218, 165, 32), self.image.get_rect())
        self.image = image.load("images/cb.png").convert_alpha()
        self.image = transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()

        #starting location for the bullet
        self.rect.x = sx
        self.rect.y = sy
        #float points coordinates for the bullet better for aiming
        self.flt_x = sx
        self.flt_y = sy
        #We need the difference for the angle that the bullet will travel
        x_diff = dx - sx
        y_diff = dy - sy
        angle = math.atan2(y_diff, x_diff)
        #Calculating the change in positions factoring velocity
        #Vel = 20
        self.change_x = math.cos(angle) * Vel
        self.change_y = math.sin(angle) * Vel

    def update(self):
        
        #Use float coords
        self.flt_y += self.change_y
        self.flt_x += self.change_x

        self.rect.y = int(self.flt_y)
        self.rect.x = int(self.flt_x)

        #we need to get rid of stray bullets
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()
        

all_sprites = pygame.sprite.Group()
enm = pygame.sprite.Group()
ammunition = pygame.sprite.Group()
my_character = Character()
all_towers = pygame.sprite.Group()
tower = Tower(380, 170)
tower2 = Tower(640, 170)
tower3 = Tower(380, 420)
tower4 = Tower(640, 420)
all_sprites.add(my_character)
all_sprites.add(tower)
all_sprites.add(tower2)
all_sprites.add(tower3)
all_sprites.add(tower4)
all_towers.add(tower)
all_towers.add(tower2)
all_towers.add(tower3)
all_towers.add(tower4)

for i in range(6):
    enemy = Enemy()
    all_sprites.add(enemy)
    enm.add(enemy)

#Main loop
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == KEYUP and event.key == K_ESCAPE):
            running = False

        if (event.type == MOUSEBUTTONDOWN and score <= 100):
            pos = pygame.mouse.get_pos()
            mx = pos[0]
            my = pos[1]
            bullet = Ammo(my_character.rect.centerx, my_character.rect.centery, mx, my, 25)
            all_sprites.add(bullet)
            ammunition.add(bullet)

        elif (event.type == MOUSEBUTTONDOWN and score > 100 and score <= 200):
            pos = pygame.mouse.get_pos()
            mx = pos[0]
            my = pos[1]
            bullet = Ammo(my_character.rect.centerx, my_character.rect.centery, mx, my, 20)
            all_sprites.add(bullet)
            ammunition.add(bullet)

        elif (event.type == MOUSEBUTTONDOWN and score > 200 and score <= 300):
            pos = pygame.mouse.get_pos()
            mx = pos[0]
            my = pos[1]
            bullet = Ammo(my_character.rect.centerx, my_character.rect.centery, mx, my, 15)
            all_sprites.add(bullet)
            ammunition.add(bullet)

        elif (event.type == MOUSEBUTTONDOWN and score > 300 and score <= 400):
            pos = pygame.mouse.get_pos()
            mx = pos[0]
            my = pos[1]
            bullet = Ammo(my_character.rect.centerx, my_character.rect.centery, mx, my, 10)
            all_sprites.add(bullet)
            ammunition.add(bullet)

        elif event.type == MOUSEBUTTONDOWN and score > 400:
            pos = pygame.mouse.get_pos()
            mx = pos[0]
            my = pos[1]
            bullet = Ammo(my_character.rect.centerx, my_character.rect.centery, mx, my, 5)
            all_sprites.add(bullet)
            ammunition.add(bullet)

        else:
           if event.type == pygame.QUIT:
            running = False
        
        if (event.type == KEYUP and event.key == K_m):
            if not muted:
                mixer.music.stop()
                muted = True
            else:
                mixer.music.load('sound/audio.wav')
                mixer.music.play(-1)
                muted = False

    keys_down = key.get_pressed()

    if keys_down[K_a]:
         if my_character.rect.left > 420:
             my_character.image = image.load("images/shooter_left.gif").convert()
             my_character.image = transform.scale(my_character.image, (50, 50))
             my_character.updateLeft()
            
    if keys_down[K_d]:
        if my_character.rect.right < 660:
            my_character.image = image.load("images/shooter_right.gif").convert()
            my_character.image = transform.scale(my_character.image, (50, 50))
            my_character.updateRight()

    if keys_down[K_w]:
        if my_character.rect.top > 240:
            my_character.image = image.load("images/shooter_top.gif").convert()
            my_character.image = transform.scale(my_character.image, (50, 50))
            my_character.updateUp()

    if keys_down[K_s]:
        if my_character.rect.bottom < 480:
            my_character.image = image.load("images/shooter_bottom.gif").convert()
            my_character.image = transform.scale(my_character.image, (50, 50))
            my_character.updateDown()

    if keys_down[K_a] and keys_down[K_w]:
        my_character.image = image.load("images/shooter_tl.gif").convert()
        my_character.image = transform.scale(my_character.image, (70, 70))

    if keys_down[K_d] and keys_down[K_w]:
        my_character.image = image.load("images/shooter_tr.gif").convert()
        my_character.image = transform.scale(my_character.image, (70, 70))

    if keys_down[K_a] and keys_down[K_s]:
        my_character.image = image.load("images/shooter_bl.gif").convert()
        my_character.image = transform.scale(my_character.image, (70, 70))

    if keys_down[K_d] and keys_down[K_s]:
        my_character.image = image.load("images/shooter_br.gif").convert()
        my_character.image = transform.scale(my_character.image, (70, 70))

    #adding the blit for image persistance in event loop
    screen.blit(bg_im, (0, 0))
    #blitting the text score
    screen.blit(score_text, (940, 20))
    screen.blit(my_score, (1020, 20))
    #Updating all sprite in the event main loop
    all_sprites.update()

    #Check if there is a collision between character and enemy and implement decrease in HP upon collision
    incr = 10
    coli = pygame.sprite.spritecollide(my_character, enm, True)

    for col in coli:
        m = Enemy()
        all_sprites.add(m)
        enm.add(m)
        
    if coli:
        hp = hp - incr
        my_hp = my_font.render(str(hp), True, (0, 255, 0))
        if hp > 0:
            running = True
        else:
            for sprite in all_sprites:
                sprite.kill()
        
    #Check if there is a collision between towers and enemy and implement decrease in HP
    col_to = pygame.sprite.groupcollide(all_towers, enm, False, True)
        
    for col in col_to:
        m = Enemy()
        all_sprites.add(m)
        enm.add(m)

    if col_to:
        hp = hp - incr
        my_hp = my_font.render(str(hp), True, (0, 255, 0))
        if hp > 0:
            running = True
        else:
            for sprite in all_sprites:
                sprite.kill()
        
    #Collision between bullet and enemy and implement increase in score
    col_be = pygame.sprite.groupcollide(ammunition, enm, True, True)
    for col in col_be:
        m = Enemy()
        all_sprites.add(m)
        enm.add(m)
        score = score + incr
        my_score = my_font.render(str(score), True, (153, 0, 0))
        running = True

        
    #Blitting HP text
    screen.blit(hp_text, (800, 20))
    screen.blit(my_hp, (850, 20))

    if hp <= 0:
        screen.blit(game_text, (450, 200))
        screen.blit(over_text, (470, 300))
        
    #Update all sprite draw in the main event loop
    all_sprites.draw(screen)
    #Final update command
    pygame.display.update()

pygame.quit()
