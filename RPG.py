iimport pygame
import sys

temp_h = -150
temp_t = 60
JUMP_SPEED = 4 * temp_h / temp_t
GRAVITY = -80 * temp_h / (temp_t ** 2)
MAP_GROUND = 465
MAP_HEIGHT = 0
MAP_LIMIT_LEFT = 0
MAP_LIMIT_RIGHT = 800

class Player(object):
    def __init__(self, x_pos, y_pos):
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
        rightdead = [pygame.image.load('get_attack_3.png')]
        rightwalk = [pygame.image.load('char_walk_' + str(i) + '.png') for i in range(1, 4)]
        leftwalk = [pygame.transform.flip(rightwalks, True, 0) for rightwalks in rightwalk]
        leftstatic = [pygame.transform.flip(rightstatic[0], True, 0)]
        leftdead = [pygame.transform.flip(rightdead[0], True, 0)]

        self.rightlist = [rightstatic, rightwalk, rightdead]
        self.leftlist = [leftstatic, leftwalk, leftdead]
        self.curlist = self.rightlist
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(topleft=(self.x_pos, self.y_pos))
    
    def move(self, x_pos, y_pos):
        self.x_pos += x_pos
        self.y_pos += y_pos

    def checkcollision(self, Enemy):
        pass

    def draw(self):
        Screen.blit(self.cursprite, (self.x_pos, self.y_pos))

    def drawStat(self):
        Length = self.HP / 5
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (10, 10, Length, 30))

    def update(self):
        hitbox = self.cursprite.get_rect(topleft=(self.x_pos, self.y_pos))
        
        if (self.isOnGround is False):
            self.y_pos += GRAVITY
        if (self.hitbox.bottom >= MAP_GROUND):
            hitbox.bottom = MAP_GROUND
            self.isOnGround = True
        if (hitbox.left <= MAP_LIMIT_LEFT):
            hitbox.left = MAP_LIMIT_LEFT
        if (hitbox.right >= MAP_LIMIT_RIGHT):
            hitbox.right = MAP_LIMIT_RIGHT

        if (self.direction == 'LEFT'):
            self.curlist = self.leftlist

        elif (self.direction == 'RIGHT'):
            self.curlist = self.rightlist
            
        if (self.walk is True):
            self.cur = 1
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

class projectile(object):
    def __init__(self):
        pass

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

player = Player(300, 300)

while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
            
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_x):
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
                player.walk = True
                
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT]):
        player.attack = False
        player.walk = True
        player.direction = 'LEFT'
        player.move(-player.SPEED, 0)
        
    elif (keys[pygame.K_RIGHT]):
        player.attack = False
        player.walk = True
        player.direction = 'RIGHT'
        player.move(player.SPEED, 0)
    
    elif (keys[pygame.K_UP]):
        player.walk = True
        player.isOnGround = False
        player.move(0, JUMP_SPEED)

    Screen.blit(mapscale, (0, 0))
    player.draw()
    player.drawStat()
    player.update()
    pygame.display.update()
    Clock.tick(FPS)
