import pygame
import sys

class Player:
    def __init__(self):
        self.color = BLUE
        self.height = 15
        self.width = 60
        self.x_pos = 100
        self.y_pos = 500
        self.Rect = pygame.Rect(self.x_pos, self.y_pos,
                                self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos,
                                              self.width, self.height])

    def move(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT]):
            self.x_pos -= 15
        elif(keys[pygame.K_RIGHT]):
            self.x_pos += 15

        if(self.x_pos < 0):
            self.x_pos = 0
        elif(self.x_pos > 422 - self.width):
            self.x_pos = 422 - self.width
        
class Block:
    def __init__(self, x_pos=0, y_pos=0, height=15, width=40):
        self.color = GREEN
        self.height = height
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.Rect = pygame.Rect(self.x_pos, self.y_pos,
                                self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos,
                                              self.width, self.height])

    def destroy(self):
        pass
    

class Ball:
    def __init__(self, x_pos, y_pos, height, width):
        self.speed = [5, 5]
        self.color = RED
        self.height = height
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.Rect = pygame.Rect(self.x_pos, self.y_pos,
                                self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.Rect.x, self.Rect.y,
                                              self.Rect.width, self.Rect.height])

    def move(self):
        self.Rect.x += self.speed[0]
        self.Rect.y += self.speed[1]
        
        if (self.Rect.right > x_size):
            self.speed[0] *= -1
        
        if (self.Rect.left < 0):
            self.speed[0] *= -1
        
        if (self.Rect.top < 0):
            self.speed[1] *= -1
            
        if ()

class Wall:
    def __init__(self, x_start, y_start, x_finish, y_finish, thick):
        self.color = BLACK
        self.x_start = x_start
        self.y_start = y_start
        self.x_finish = x_finish
        self.y_finish = y_finish
        self.thick = thick

    def draw(self):
        pygame.draw.line(screen, self.color, [self.x_start, self.y_start],
                         [self.x_finish, self.y_finish], self.thick)

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
ball = Ball(300, 300, 15, 15)
wall_1 = Wall(0, 0, 0, 600, 2)
wall_2 = Wall(420, 0, 420, 600, 2)
wall_3 = Wall(0, 0, 422, 0, 2)

def start(): # 시작 함수
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            roop = False

    player.move()
    ball.move()
    
    screen.fill(WHITE)
    player.draw()
    ball.draw()
    pygame.display.flip() # 업데이트 함수
    clock.tick(60)

def clear():
    pass

def fail():
    pass

while roop:
    start()

pygame.quit() # 
