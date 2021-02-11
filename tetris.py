import pygame
import sys
import random

class Board(object):
    def __init__(self):
        self.board = []
        tmpimage = pygame.image.load('C:/Users/jeawo/OneDrive/바탕 화면/sprites/display.png')
        self.image = pygame.transform.scale(tmpimage, (pixel, pixel))
        
        for dx in range(boardx):
            self.board.append([self.image] * boardy) #-> board[boardy][boardx]

    def addmino(self, mino):
        for x in range(Templatex):
            for y in range(Templatey):
                if (Shapedic[mino.shape][mino.rotation][y][x] != BLANK):
                    self.board[x + int(mino.boxx)][y + int(mino.boxy)] = mino.image
                    
    def isOnBoard(self, x, y):
        return x >= 0 and x < boardx and y < boardy
    
    def isValiedPosition(self, mino, adjX=0, adjY=0):
        for x in range(Templatex):
            for y in range(Templatey):
                if (Shapedic[mino.shape][mino.rotation][y][x] == BLANK):
                    continue
                if not (self.isOnBoard(x + int(mino.boxx) + adjX, y + int(mino.boxy) + adjY)):
                    return False
                if (self.board[x + int(mino.boxx) + adjX][y + int(mino.boxy) + adjY] != self.image):
                    return False
        return True
    
    def isCompleteLine(self, y):
        for x in range(boardx):
            if (self.board[x][y] == self.image):
                return False
        return True
                
    def removeCompliteLine(self):
        numLinesRemoved = 0
        y = boardy - 1
        while (y >= 0):
            if (self.isCompleteLine(y)):
                for pullDownY in range(y, 0, -1):
                    for x in range(boardx):
                        self.board[x][pullDownY] = self.board[x][pullDownY - 1]
                for x in range(boardx):
                    self.board[x][0] = self.image
                numLinesRemoved += 1
            else:
                y -= 1
                
        return numLinesRemoved
    
    def drawboard(self):
        for x in range(boardx):
            for y in range(boardy):
                screen.blit(self.board[x][y], (xmargin + x * pixel,
                                               ymargin + y * pixel))

class Mino(object):
    def __init__(self, x_pos=None, y_pos=None):
        shape = random.choice(list(Shapedic.keys()))
        image = random.choice(ColorList)
        self.shape = shape
        self.rotation = random.randint(0, len(Shapedic[self.shape]) - 1)
        tmpimage = pygame.image.load(image)
        self.image = pygame.transform.scale(tmpimage, (pixel, pixel))
        if (x_pos is None):
            self.boxx = int(boardx / 2) - int(Templatex / 2)
        else:
            self.boxx = x_pos
        if (y_pos is None):
            self.boxy = 0
        else:
            self.boxy = y_pos
        self.exist = True

    def initpos(self):
        self.boxx = int(boardx / 2) - int(Templatex / 2)
        self.boxy = 0

    def move(self, x_pos, y_pos=None):
        self.boxx += x_pos
        if (y_pos is None):
            self.boxy += 0.5
        else:
            self.boxy += y_pos

    def spin(self, rotation=None):
        if(rotation is None):
            self.rotation += 1
            if (self.rotation == len(Shapedic[self.shape])):
                self.rotation = 0
        else:
            self.rotation += rotation
            if (self.rotation < 0):
                self.rotation = len(Shapedic[self.shape]) - 1

    def drawmino(self):
        curmino = Shapedic[self.shape][self.rotation]
        pixelx, pixely = convertpixel(self.boxx, self.boxy)
        
        for x in range(Templatex):
            for y in range(Templatey):
                if (curmino[y][x] != BLANK):
                    screen.blit(self.image, (pixelx + (x * pixel),
                                             pixely + (y * pixel)))

pygame.init()

BLACK= ( 0,  0,  0)
WHITE= (255, 255, 255)
BLUE = ( 0,  0,255)
GREEN= ( 0,255,  0)
RED  = (255,  0,  0)
GRAY = (185, 185, 185)

FPS = 10
pixel = 30
boardx = 13
boardy = 24
gameboardx = 390
gameboardy = 720
x_size = 600
y_size = 780
xmargin = x_size - gameboardx
ymargin = y_size - gameboardy
BLANK = '.'
Templatex = 5
Templatey = 5
font = pygame.font.SysFont('굴림', 70)

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

ColorList = ['C:/Users/jeawo/OneDrive/바탕 화면/sprites/block' + str(i) + '.png' for i in range(1, 7)]

def convertpixel(boardx, boardy):
    pixelx = xmargin + (boardx * pixel)
    pixely = ymargin + (boardy * pixel)

    return pixelx, pixely

def write(font, Text, color, x_pos, y_pos):
    surface = font.render(Text, True, color)
    rect = surface.get_rect()
    rect.center = (x_pos, y_pos)
    screen.blit(surface, rect)

def StartScreen():
    while True:
        screen.fill(WHITE)
        write(bigfont, 'Tetris', BLACK, x_size / 2, y_size / 2)
        write(bigfont, 'Press S!', BLACK, x_size / 2, 450)
        pygame.display.update()
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_s):
                    return False
                elif (event.type == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

def GameoverScreen():
    screen.fill(GRAY)
    write(bigfont, 'GameOver!!!', BLUE, x_size / 2, 300)
    write(bigfont, 'Try Again?', BLUE, x_size / 2, 370)
    write(bigfont, 'Y / N', BLUE, x_size / 2, 440)
    pygame.display.update()
    pygame.time.wait(500)
    
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_y):
                return True
            elif (event.key == pygame.K_n):
                pygame.quit()
                sys.exit()     

def rungame():
    pygame.init()
    
    GameBoard = Board()
    FallingMino = Mino()
    NextMino = Mino(-6, 1.5)
    curscore = 0
    
    while True:
        if (FallingMino.exist == False):
            FallingMino = NextMino
            FallingMino.initpos()
            NextMino = Mino(-6, 1.5)

            if (GameBoard.isValiedPosition(FallingMino) is False):
                break

        FallingMino.move(0)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT) and (GameBoard.isValiedPosition(FallingMino, adjX=-1)):
                    FallingMino.move(-1)
                elif (event.key == pygame.K_RIGHT) and (GameBoard.isValiedPosition(FallingMino, adjX=1)):
                    FallingMino.move(1)
                elif (event.key == pygame.K_DOWN):
                    if (GameBoard.isValiedPosition(FallingMino, adjY=1)):
                        FallingMino.move(0, 1)
                elif (event.key == pygame.K_g):
                    FallingMino.spin()
                    if not (GameBoard.isValiedPosition(FallingMino)):
                        FallingMino.spin(-1)
                elif (event.key == pygame.K_SPACE):
                    for i in range(1, boardy):
                        if not (GameBoard.isValiedPosition(FallingMino, adjY=i)):
                            break
                    FallingMino.boxy += i - 1
                elif (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
        
        if not (GameBoard.isValiedPosition(FallingMino, adjY=1)):
            GameBoard.addmino(FallingMino)
            curscore += GameBoard.removeCompliteLine()
            FallingMino.exist = False
            
        screen.fill(GRAY)
        GameBoard.drawboard()
        NextMino.drawmino()
        if (FallingMino.exist != False):
            FallingMino.drawmino()
        write(smallfont, 'next mino:', BLACK, 90, 90)
        write(smallfont, 'score:' + str(curscore), BLACK, 70, 40)

        pygame.display.flip()
        clock.tick(FPS)

def main():
    global clock, screen, bigfont, smallfont
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((x_size, y_size))
    bigfont = pygame.font.SysFont('굴림', 70)
    smallfont = pygame.font.SysFont('굴림', 40)
    
    pygame.display.set_caption("Tetris")
    
    StartScreen()
    while True:
        rungame()
        GameoverScreen()

if (__name__ == '__main__'):
    main()
