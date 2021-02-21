import pygame
import sys

temp_h = -150
temp_t = 60
JUMP_SPEED = 60 * temp_h / temp_t
GRAVITY = -80 * temp_h / (temp_t ** 2)
MAP_GROUND = 465
MAP_HEIGHT = 0
MAP_LIMIT_LEFT = 0
MAP_LIMIT_RIGHT = 800

class Player(object):
    def __init__(self, x_pos, y_pos=None):
        self.HP = 1000
        self.ATK = 30
        self.DEF = 20
        self.SPEED = 10
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.direction = 'RIGHT'
        self.dead = False
        self.attack = False
        self.walk = False
        self.isOnGround = True
        self.index = 0
        self.cur = 0
        
        rightstatic = [pygame.image.load('char_static.png')]
        rightdead = [pygame.image.load('char_dead.png')]
        rightwalk = [pygame.image.load('char_walk_' + str(i) + '.png') for i in range(1, 4)]
        rightattack = [pygame.image.load('char_attack.png')]
        leftwalk = [pygame.transform.flip(rightwalks, True, 0) for rightwalks in rightwalk]
        leftstatic = [pygame.transform.flip(rightstatic[0], True, 0)]
        leftdead = [pygame.transform.flip(rightdead[0], True, 0)]
        leftattack = [pygame.transform.flip(rightattack[0], True, 0)]

        self.rightlist = [rightstatic, rightwalk, rightattack, rightdead]
        self.leftlist = [leftstatic, leftwalk, leftattack, leftdead]
        self.curlist = self.rightlist
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(topleft=(self.x_pos, self.y_pos))
        
    def SetStat(self, HP, ATK, DEF, SPEED):
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.SPEED = SPEED
    
    def move(self, x_pos, y_pos):
        self.x_pos += x_pos
        self.y_pos += y_pos

    def checkcollision(self, Enemy):
        pass

    def draw(self):
        Screen.blit(self.cursprite, (self.hitbox.x, self.hitbox.y))

    def drawStat(self):
        Length = self.HP / 5
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (10, 10, Length, 30))

    def update(self):
        self.hitbox.x = self.x_pos
        self.hitbox.y = self.y_pos
        
        if (self.isOnGround is False):
            self.y_pos += GRAVITY
        if (self.hitbox.bottom >= MAP_GROUND):
            self.hitbox.bottom = MAP_GROUND
            self.isOnGround = True
        if (self.hitbox.left <= MAP_LIMIT_LEFT):
            self.hitbox.left = MAP_LIMIT_LEFT
        if (self.hitbox.right >= MAP_LIMIT_RIGHT):
            self.hitbox.right = MAP_LIMIT_RIGHT

        if (self.direction == 'LEFT'):
            self.curlist = self.leftlist

        elif (self.direction == 'RIGHT'):
            self.curlist = self.rightlist
        if (self.walk is True):
            self.cur = 1
        else:
            self.cur = 0
        if (self.attack is True):
            self.cur = 2
        else:
            self.cur = 0
        if (self.HP <= 0):
            self.cur = 3
            self.dead = True

        self.index += 1
        if (self.index >= len(self.curlist[self.cur])):
            self.index = 0
            
        self.cursprite = self.curlist[self.cur][self.index]

class Enemy(object):
    def __init__(self):
        pass

class Boss(object):
    def __init__(self):
        pass

class Bubble(object):
    def __init__(self, x_pos, y_pos, ATK):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.ATK = ATK
        self.SPEED = (3, 4)
        image = pygame.image.load('bubble.png')
        self.image = pygame.transform.scale(image, (30, 30))
        self.hitbox = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        
    def draw(self):
        Screen.blit(self.image, (self.hitbox.x, self.hitbox.y))
        
    def move(self):
        self.hitbox.x += self.SPEED[0]
        
        
    def checkcollision(self, Enemy):
        if (self.hitbox.colliderect(Enemy)):
            return True
        else:
            return False
    
pygame.init() # pygame 초기화

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

x_size = 800
y_size = 600
Screen = pygame.display.set_mode((x_size, y_size))
FPS = 60
Clock = pygame.time.Clock()

# make enemylist!!!
mapimage = pygame.image.load('display.png')
mapscale = pygame.transform.scale(mapimage, (800, 600))

player = Player(300, MAP_GROUND - 64)
Bubblelist = []

while True:
    Screen.blit(mapscale, (0, 0))
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
            
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                player.attack = False
                player.walk = True
                player.direction = 'LEFT'
            elif (event.key == pygame.K_RIGHT):
                player.attack = False
                player.walk = True
                player.direction = 'RIGHT'
            elif (event.key == pygame.K_UP):
                player.walk = True
                player.isOnGround = False
                player.move(0, JUMP_SPEED)
            elif (event.key == pygame.K_x):
                player.walk = False
                player.attack = True
            elif (event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
                
        elif (event.type == pygame.KEYUP):
            if (event.key == pygame.K_LEFT or
                event.key == pygame.K_RIGHT or
                event.key == pygame.K_UP):
                player.walk = False
            
            elif (event.key == pygame.K_x):
                player.attack = False
                
    if (player.walk is True and player.attack is False):
        if (player.direction == 'LEFT'):
            player.move(-player.SPEED, 0)
        elif (player.direction == 'RIGHT'):
            player.move(player.SPEED, 0)
            
    if (player.attack is True):
        Bubblelist.append(Bubble(player.hitbox.right, player.hitbox.y , player.ATK))

    player.draw()
    player.drawStat()
    player.update()
    if (len(Bubblelist) != 0):
        for bubble in Bubblelist:
            bubble.move()
            bubble.draw()
    pygame.display.update()
    Clock.tick(FPS)
