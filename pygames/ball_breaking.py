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

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.hitbox.x, self.hitbox.y,
                                              self.width, self.height])

    def move(self, x_pos, y_pos):
        self.hitbox.x += x_pos
        self.hitbox.y += y_pos

    def checkcollision(self, Ahitbox):
        if(pygame.Rect.colliderect(self.hitbox, Ahitbox)):
            return True
        else:
            return False

class Player(Object):
    def __init__(self, color, x_pos, y_pos, width, height):
        super().__init__(color, x_pos, y_pos, width, height)

    def move(self, x_pos, y_pos):
        super().move(x_pos, y_pos)

        if(self.hitbox.x < 2):
            self.hitbox.x = 2
        elif(self.hitbox.x > 452 - self.width):
            self.hitbox.x = 452 - self.width

class Block(Object):
    def __init__(self, color, x_pos, y_pos, width, height):
        super().__init__(color, x_pos, y_pos, width, height)

class Ball(Object):
    def __init__(self, color, x_pos, y_pos, width, height):
        super().__init__(color, x_pos, y_pos, width, height)
        self.speed = [1, 2]
        
    def reflect(self, Ahitbox):
        dx1 = abs(self.hitbox.right - Ahitbox.hitbox.left)
        dx2 = abs(self.hitbox.left - Ahitbox.hitbox.right)
        dy1 = abs(self.hitbox.top - Ahitbox.hitbox.bottom)
        dy2 = abs(self.hitbox.bottom - Ahitbox.hitbox.top)
        
        selfpos = [self.hitbox.centerx, self.hitbox.centery]
        Apos = [Ahitbox.hitbox.centerx, Ahitbox.hitbox.centery]
        vector = ["X", "Y", "S"]
        
        if(self.checkcollision(Ahitbox.hitbox)):
            if(selfpos[0] > Apos[0] and selfpos[1] > Apos[1]):
                if(dy1 > dx2):
                    return vector[0]
                elif(dy1 < dx2):
                    return vector[1]
                else:
                    return vector[2]
            elif(selfpos[0] > Apos[0] and selfpos[1] < Apos[1]):
                if(dy2 > dx2):
                    return vector[0]
                elif(dy2 < dx2):
                    return vector[1]
                else:
                    return vector[2]
            elif(selfpos[0] < Apos[0] and selfpos[1] > Apos[1]):
                if(dy1 > dx1):
                    return vector[0]
                elif(dy1 < dx1):
                    return vector[1]
                else:
                    return vector[2]
            elif(selfpos[0] < Apos[0] and selfpos[1] < Apos[1]):
                if(dy2 > dx1):
                    return vector[0]
                elif(dy2 < dx1):
                    return vector[1]
                else:
                    return vector[2]

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
fps = 60

def write(Text, color, x_pos, y_pos):
    surface = font.render(Text, True, color)
    rect = surface.get_rect()
    rect.center = (x_pos, y_pos)
    screen.blit(surface, rect)
    
def StartScreen():
    while True:
        screen.fill(WHITE)
        write('Ball Breaking', BLACK, x_size / 2, y_size / 2)
        write('Press S!', BLACK, x_size / 2, y_size * (2 / 3))
        pygame.display.update()
        
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_s):
                    return False
            
def GameoverScreen():
    write('Stage Fail!!!', BLACK, x_size / 2, 200)
    write('Try Again?', BLACK, x_size / 2, 270)
    write('Y / N', BLACK, x_size / 2, 340)
    pygame.display.update()
    pygame.time.wait(500)
    
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_y):
                return True
            elif (event.key == pygame.K_n):
                pygame.quit()
                sys.exit()     
    
def clear(curscore):
    write('Stage Clear!!!', BLACK, x_size / 2, 300)
    write('score : ' + str(curscore), BLACK, x_size / 2, 370)

def rungame(): # 시작 함수
    screen.fill(WHITE)

    blocklist = []
    for i in range(2, 7):
        for j in range(1, 10):
            blocklist.append(Block(GREEN, 2 + 41 * j, 52 + 16 * i, 40, 15))
    player = Player(BLUE, 100, 500, 60, 15)
    ball = Ball(RED, 200, 200, 15, 15)
    ballspeed = [2, 4]
    wall_1 = Wall(BLACK, 0, 50, 2, y_size)
    wall_2 = Wall(BLACK, 0, 50, x_size, 2)
    wall_3 = Wall(BLACK, x_size - 2, 50, 2, y_size)
    wall_4 = Wall(BLACK, 0, y_size - 2, x_size, 2)
    walllist = [wall_1, wall_2, wall_3, wall_4]
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT]):
            player.move(-5, 0)
        elif(keys[pygame.K_RIGHT]):
            player.move(5, 0)

        ball.move(ballspeed[0], ballspeed[1])

        if(ball.checkcollision(wall_1.hitbox) or
           ball.checkcollision(wall_3.hitbox)):
            ballspeed[0] *= -1
        if(ball.checkcollision(wall_2.hitbox)):
            ballspeed[1] *= -1
        for b in blocklist:
            if(ball.reflect(b) == "X"):
                ballspeed[0] *= -1
                score += 1
                blocklist.remove(b)
            if(ball.reflect(b) == "Y"):
                ballspeed[1] *= -1
                score += 1
                blocklist.remove(b)
            if(ball.reflect(b) == "S"):
                ballspeed[0] *= -1
                ballspeed[1] *= -1
                score += 1
                blocklist.remove(b)
        if(ball.reflect(player) == "X"):
            ballspeed[0] *= -1
        if(ball.reflect(player) == "Y"):
            ballspeed[1] *= -1
        if(ball.reflect(player) == "S"):
            ballspeed[0] *= -1
            ballspeed[1] *= -1

        screen.fill(WHITE)
        curscore = font.render('score : ' + str(score), 1, BLACK)
        scorerect = curscore.get_rect()
        scorerect.center = (300, 25)
        screen.blit(curscore, scorerect)
        player.draw()
        ball.draw()
        for wall in walllist:
            wall.draw()
        for b in blocklist:
            b.draw()
        if(ball.checkcollision(wall_4.hitbox)):
            ballspeed[0] = 0
            ballspeed[1] = 0
            break
        if(len(blocklist) == 0):
            ballspeed[0] = 0
            ballspeed[1] = 0
            clear(score)
        pygame.display.flip() # 업데이트 함수
        clock.tick(fps)

def main():
    global clock, screen, font
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((x_size, y_size))
    font = pygame.font.SysFont('굴림', 70)
    
    
    pygame.display.set_caption("Wall Breaking")
    
    StartScreen()
    while True:
        rungame()
        GameoverScreen()

if (__name__ == '__main__'):
    main()
