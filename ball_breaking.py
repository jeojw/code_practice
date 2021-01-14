import pygame
import sys
import time

class Object(object):
    def __init__(self, color, x_pos, y_pos, width, height):
        self.color = color
        self.height = height
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos,
                                  self.width, self.height)
        self.poslist = [self.hitbox.left, self.hitbox.right,
                        self.hitbox.top, self.hitbox.bottom]
        
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos,
                                              self.width, self.height])
    
    def move(self, x_pos, y_pos):
        self.x_pos += x_pos
        self.y_pos += y_pos

    def updatehitbox(self, x_pos, y_pos):
        self.move(x_pos, y_pos)
        self.hitbox.x = self.x_pos
        self.hitbox.y = self.y_pos

    def checkcollidrect(self, Ahitbox):
        if(pygame.Rect.colliderect(self.hitbox, Ahitbox)):
            return True
        else:
            return False

class Player(Object):
    def __init__(self, color, x_pos, y_pos, width, height):
        super().__init__(color, x_pos, y_pos, width, height)

    def move(self, x_pos, y_pos):
        super().move(x_pos, y_pos)

        if(self.x_pos < 2):
            self.x_pos = 2
        elif(self.x_pos > 420 - self.width):
            self.x_pos = 420 - self.width

class Block(Object):
    def __init__(self, color, x_pos, y_pos, width, height):
        super().__init__(color, x_pos, y_pos, width, height)

class Ball(Object):
    def __init__(self, color, x_pos, y_pos, width, height):
        super().__init__(color, x_pos, y_pos, width, height)

class Wall(Object):
    def __init__(self, color, x_pos, y_pos, width, height):
        super().__init__(color, x_pos, y_pos, width, height)

#---------------------------------------------------------------------------------------

pygame.init() # pygame 초기화

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

x_size = 454
y_size = 600
screen = pygame.display.set_mode((x_size, y_size)) # 창 사이즈  설정

pygame.display.set_caption("Wall Breaking") # 창 이름 설정

clock = pygame.time.Clock() # FPS
global x_pos
x_pos = 100
global y_pos
y_pos = 500

screen.fill(WHITE)

blocklist = []
for i in range(2, 7):
    for j in range(2, 9):
        blocklist.append(Block(GREEN, 2 + 41 * j, 52 + 16 * i, 40, 15))
player = Player(BLUE, 100, 500, 60, 15)
ball = Ball(RED, 200, 200, 15, 15)
ballspeed = [1, 2]
wall_1 = Wall(BLACK, 0, 50, 2, y_size)
wall_2 = Wall(BLACK, 0, 50, x_size, 2)
wall_3 = Wall(BLACK, x_size - 2, 50, 2, y_size)
wall_4 = Wall(BLACK, 0, y_size - 2, x_size, 2)

gulimfont = pygame.font.SysFont('굴림', 70)

def write(Text, color, x_pos, y_pos):
    surface = gulimfont.render(Text, True, color)
    rect = surface.get_rect()
    rect.center = (x_pos, y_pos)
    screen.blit(surface, rect)

def clear(curscore):
    write('Stage Clear!!!', BLACK, x_size / 2, 300)
    write('score : ' + str(curscore), BLACK, x_size / 2, 370)

def fail(curscore):
    write('Stage Fail!!!', BLACK, x_size / 2, 200)
    write('score : ' + str(curscore), BLACK, x_size / 2, 270)
    write('Try Again?', BLACK, x_size / 2, 340)
    write('Y / N', BLACK, x_size / 2, 410)

def rungame(): # 시작 함수
    roop = True
    score = 0
    fps = 60

    while roop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                roop = False

        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT]):
            player.move(-5, 0)
            player.updatehitbox(-5, 0)
        elif(keys[pygame.K_RIGHT]):
            player.move(5, 0)
            player.updatehitbox(5, 0)

        ball.move(ballspeed[0], ballspeed[1])
        ball.updatehitbox(ballspeed[0], ballspeed[1])

        if(ball.checkcollidrect(wall_1.hitbox) or
           ball.checkcollidrect(wall_3.hitbox)):
            ballspeed[0] *= -1
        if(ball.checkcollidrect(wall_2.hitbox) or
           ball.checkcollidrect(player.hitbox)):
            ballspeed[1] *= -1
        for b in blocklist:
            if(ball.checkcollidrect(b.hitbox)):
                ballspeed[1] *= -1
                score += 1
                blocklist.remove(b)
                
        screen.fill(WHITE)
        gulimfont = pygame.font.SysFont('굴림', 70)
        curscore = gulimfont.render('score : ' + str(score), 1, BLACK)
        scorerect = curscore.get_rect()
        scorerect.center = (300, 25)
        screen.blit(curscore, scorerect)
        player.draw()
        ball.draw()
        wall_1.draw()
        wall_2.draw()
        wall_3.draw()
        wall_4.draw()
        for b in blocklist:
            b.draw()
        if(ball.checkcollidrect(wall_4.hitbox)):
            ballspeed[0] = 0
            ballspeed[1] = 0
            fail(score)
            if(keys[pygame.K_y]):
                pygame.init() ##??
            if(keys[pygame.K_n]):
                pygame.quit()
        if(len(blocklist) == 0):
            ballspeed[0] = 0
            ballspeed[1] = 0
            clear(score)
        pygame.display.flip() # 업데이트 함수
        clock.tick(fps)

    pygame.quit()

rungame()
