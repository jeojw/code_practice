import pygame
import sys
import random

class Mino(object):
    def __init__(self, image, x_pos=None, y_pos=None):
        shape = random.choice(list(Shapedic.keys()))
        self.shape = shape
        self.rotation = random.randint(0, len(Shapedic[self.shape]) - 1)
        tmpimage = pygame.image.load(image)
        self.image = pygame.transform.scale(tmpimage, (pixel, pixel))
        if (x_pos is None):
            self.x_pos = int(gameboardx / 2)
        else:
            self.x_pos = x_pos
        if (y_pos is None):
            self.y_pos = -10
        else:
            self.y_pos = y_pos
            
        self.curmino = Shapedic[self.shape][self.rotation]
        self.location = []
        self.hitboxlist = []
        for x in range(Templatex):
            for y in range(Templatey):
                if (self.curmino[y][x] != BLANK):
                    self.location.append([x, y])

        for rects in self.location:
            self.hitboxlist.append(self.image.get_rect(topleft=(self.x_pos + rects[0] * pixel,
                                                                self.y_pos + rects[1] * pixel)))

    def move(self, x_pos, y_pos=None):
        for hitbox in self.hitboxlist:
            hitbox.x += x_pos
            if (y_pos is None):
                hitbox.y += pixel / 10
            else:
                hitbox.y += y_pos

    def spin(self):
        self.rotation += 1
        if (self.rotation == len(Shapedic[self.shape])):
            self.rotation = 0

    def drawmino(self):
        for block in self.hitboxlist:
            screen.blit(self.image, block)

                    
pygame.init()

BLACK= ( 0,  0,  0)
WHITE= (255, 255, 255)
BLUE = ( 0,  0,255)
GREEN= ( 0,255,  0)
RED  = (255,  0,  0)
GRAY = (185, 185, 185)

size = [600, 800]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

roop = True
FPS = 10
clock = pygame.time.Clock()
pixel = 40
gameboardx = 440
gameboardy = 720
xmargin = size[0] - gameboardx
ymargin = size[1] - gameboardy
BLANK = '.'
Templatex = 5
Templatey = 5
font = pygame.font.SysFont('굴림', 70)

displayimage = pygame.image.load('display.png')
scaledisplay = pygame.transform.scale(displayimage, (40, 40))
display = scaledisplay.get_rect()

IminoTemplate = [['..o..',
                  '..o..',
                  '..o..',
                  '..o..',
                  '.....'],
                 ['.....',
                  '.....',
                  'oooo.',
                  '.....',
                  '.....']]

LminoTemplate = [['.....',
                  '..o..',
                  '..o..',
                  '..oo.',
                  '.....'],
                 ['.....',
                  '.....',
                  '.ooo.',
                  '.o...',
                  '.....'],
                 ['.....',
                  '.oo..',
                  '..o..',
                  '..o..',
                  '.....'],
                 ['.....',
                  '...o.',
                  '.ooo.',
                  '.....',
                  '.....']]

JminoTemplate = [['.....',
                  '..o..',
                  '..o..',
                  '.oo..',
                  '.....'],
                 ['.....',
                  '.o...',
                  '.ooo.',
                  '.....',
                  '.....'],
                 ['.....',
                  '..oo.',
                  '..o..',
                  '..o..',
                  '.....'],
                 ['.....',
                  '.....',
                  '.ooo.',
                  '...o.',
                  '.....']]

SminoTemplate = [['.....',
                  '..oo.',
                  '.oo..',
                  '.....',
                  '.....'],
                 ['.....',
                  '.o...',
                  '.oo..',
                  '..o..',
                  '.....']]

ZminoTemplate = [['.....',
                  '.oo..',
                  '..oo.',
                  '.....',
                  '.....'],
                 ['.....',
                  '..o..',
                  '.oo..',
                  '.o...',
                  '.....']]

TminoTemplate = [['.....',
                  '.....',
                  '.ooo.',
                  '..o..',
                  '.....'],
                 ['.....',
                  '..o..',
                  '.oo..',
                  '..o..',
                  '.....'],
                 ['.....',
                  '..o..',
                  '.ooo.',
                  '.....',
                  '.....'],
                 ['.....',
                  '..o..',
                  '..oo.',
                  '..o..',
                  '.....']]

OminoTemplate = [['.....',
                  '..oo.',
                  '..oo.',
                  '.....',
                  '.....']]

Shapedic = {'I': IminoTemplate,
            'L': LminoTemplate,
            'J': JminoTemplate,
            'S': SminoTemplate,
            'Z': ZminoTemplate,
            'T': TminoTemplate,
            'O': OminoTemplate}

def SetGameBoard():
    board = []
    for dy in range(0, int(gameboardy / pixel) + 1):
        board.append([BLANK] * (int(gameboardx / pixel) + 1))

    return board

def convertpixel(boardx, boardy):
    pixelx = xmargin + (boardx * pixel)
    pixely = ymargin + (boardy * pixel)

    return pixelx, pixely
    
def DrawBoard():
    for dy in range(0, int(gameboardy / pixel) + 1):
            for dx in range(0, int(gameboardx / pixel) + 1):
                screen.blit(scaledisplay, (xmargin + dx * pixel,
                                           ymargin + dy * pixel))

def rungame():
    pygame.init()
    
    shape = random.choice(list(Shapedic.keys()))
    FallingMino = Mino('test.png')
    NextMino = Mino('test.png')
    
    while True:
        screen.fill(RED)
        FallingMino.move(0)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    FallingMino.move(-pixel)
                elif (event.key == pygame.K_RIGHT):
                    FallingMino.move(pixel)
                elif (event.key == pygame.K_DOWN):
                    FallingMino.move(0, pixel / 2)
                elif (event.key == pygame.K_g):
                    FallingMino.spin()

        DrawBoard()
        FallingMino.drawmino()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    rungame()
