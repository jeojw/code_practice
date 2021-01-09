import pygame
import sys

class Player(object):
    def __init__(self):
        self.color = BLUE
        self.height = 15
        self.width = 60
        self.x_pos = 100
        self.y_pos = 500
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos,
                                              self.width, self.height])

    def move(self, x_pos):
        self.x_pos += x_pos

        if(self.x_pos < 2):
            self.x_pos = 2
        elif(self.x_pos > 420 - self.width):
            self.x_pos = 420 - self.width
            
        self.checkhitbox(x_pos)
            
    def checkhitbox(self, x_pos):
        self.x_pos += x_pos
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)
    
    def checkcollision(self, Ahitbox):
        if(pygame.Rect.colliderect(self.hitbox, Ahitbox)):
            return True
        else:
            return False

class Block(object):
    def __init__(self, x_pos=0, y_pos=0, width=40, height=15):
        self.color = GREEN
        self.height = height
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos,
                                              self.width, self.height])
        
    def checkhitbox(self):
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)
        
    def checkcollision(self, Ahitbox):
        if(pygame.Rect.colliderect(self.hitbox, Ahitbox)):
            return True
        else:
            return False

    def destroy(self):
        pass

class Ball(object):
    def __init__(self, x_pos, y_pos, width, height):
        self.color = RED
        self.height = height
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos,
                                              self.width, self.height])

    def move(self, x_pos, y_pos):
        self.x_pos += x_pos
        self.y_pos += y_pos
        
        self.checkhitbox(x_pos, y_pos)
        
    def checkhitbox(self, x_pos, y_pos):
        self.x_pos += x_pos
        self.y_pos += y_pos
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)
        
    def checkcollision(self, Ahitbox):
        if(pygame.Rect.colliderect(self.hitbox, Ahitbox)):
            return True
        else:
            return False

class Wall(object):
    def __init__(self, x_pos, y_pos, width, height):
        self.color = BLACK
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = height
        self.width = width
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)
        
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos,
                                              self.width, self.height])
    
    def checkhitbox(self):
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)
        
    def checkcollision(self, Ahitbox):
        if(pygame.Rect.colliderect(self.hitbox, Ahitbox)):
            return True
        else:
            return False

#---------------------------------------------------------------------------------------
        
pygame.init() # pygame 초기화

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

x_size = 422
y_size = 600
screen = pygame.display.set_mode((x_size, y_size)) # 창 사이즈  설정

pygame.display.set_caption("Wall Breaking") # 창 이름 설정

roop = True
clock = pygame.time.Clock() # FPS
global x_pos
x_pos = 100
global y_pos
y_pos = 500

screen.fill(WHITE)

block = Block(0, 0, 15, 40)
player = Player()
ball = Ball(150, 150, 15, 15)
wall_1 = Wall(0, 50, 2, y_size)
wall_2 = Wall(0, 50, x_size, 2)
wall_3 = Wall(x_size - 2, 50, 2, y_size)

def start(): # 시작 함수
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            roop = False

    keys = pygame.key.get_pressed()
    if(keys[pygame.K_LEFT]):
        player.move(-15)
    elif(keys[pygame.K_RIGHT]):
        player.move(15)
    
    ballspeed = [2, 2]
    ball.move(ballspeed[0], ballspeed[1])
    ball.checkhitbox(ballspeed[0], ballspeed[1])
    if(ball.checkcollision(wall_1.hitbox) is True):
        ballspeed[0] *= -1
    if(ball.checkcollision(wall_2.hitbox) is True):
        ballspeed[1] *= -1
    if(ball.checkcollision(wall_3.hitbox) is True):
        ballspeed[0] *= -1

    screen.fill(WHITE)
    player.draw()
    ball.draw()
    wall_1.draw()
    wall_2.draw()
    wall_3.draw()
    pygame.display.flip() # 업데이트 함수
    clock.tick(60)

def clear():
    pass

def fail():
    pass

while roop:
    start()

pygame.quit() # 
