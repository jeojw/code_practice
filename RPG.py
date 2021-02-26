import pygame
import sys

pygame.init() # pygame 초기화

temp_h = -150
temp_t = 60
JUMP_SPEED = 60 * temp_h / temp_t
GRAVITY = -80 * temp_h / (temp_t ** 2)
MAP_GROUND = 465
MAP_HEIGHT = 0
MAP_LIMIT_LEFT = 0
MAP_LIMIT_RIGHT = 800

'''
오브젝트의 스텟 관련 변수
'''
HP = 'hp'
ATK = 'atk'
DEF = 'def'
SPEED = 'speed'

'''
오브젝트의 컨디션 관련 전역변수
'''
LEFT = 'LEFT'
RIGHT = 'RIGHT'
DIRECTION = 'direction'
WALK = 'walk'
ATTACK = 'attack'
GETATTACK = 'getattack'
DEAD = 'dead'
HITBOX = 'hitbox'
ONGROUND = 'onground'

'''
히트박스 사이즈 및 위치 전역변수
'''
X = 'x'
Y = 'y'
WIDTH = 'width'
HEIGHT = 'height'

class Bubble(object):
    def __init__(self, x_pos, y_pos, ATK, direction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.ATK = ATK
        self.SPEED = 3
        self.direction = direction
        image = pygame.image.load('char_sprite/bubble.png')
        self.image = pygame.transform.scale(image, (30, 30))
        self.hitbox = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        
    def draw(self):
        Screen.blit(self.image, (self.hitbox.x, self.hitbox.y))
        
    def move(self):
        if (self.direction == LEFT):
            self.hitbox.x += -self.SPEED
        else:
            self.hitbox.x += self.SPEED

    def checkcollision(self, Enemy):
        if (pygame.Rect.colliderect(self.hitbox, Enemy.hitbox)):
            return True
        else:
            return False

class Item(object):
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = None
    
class Life(object):
    '''
    해당 클래스는 가독성을 위해 enemy class, player class의 부모 클래스로, 이 클래스 기반으로 상속 및 오버라이딩을 함
    '''
    def __init__(self, x_pos, y_pos=None):
        '''
        해당 생성자는 부모 생성자로, 자식 클래스들이 이를 오버라이딩을 함!
        '''
        
        '''
        오브젝트의 스텟 및 위치
        '''
        self.x_pos = x_pos
        if (y_pos is None):
            self.y_pos = MAP_GROUND
        else:
            self.y_pos = y_pos
        self.HP = 0
        self.ATK = 0
        self.DEF = 0
        self.SPEED = 0
        self.GETATTACK = 80 #피격당할 시 넉백되는 거리를 설정
        
        '''
        오브젝트의 전체적인 상태를 나타내는 변수들
        '''
        self.direction = RIGHT
        self.isDead = False
        self.isAttack = False
        self.isWalk = False
        self.isOnGround = True
        self.isGetattack = False
        self.isHitbox = True #사망 시에 히트박스 없는 것으로 처리
        self.index = 0 #각 스프라이트 리스트의 인덱스
        self.cur = 0 #각 스프라이트 덩어리의 인덱스
        self.projectilelist = [] #플레이어가 공격판정이 정해질 때 리스트로 따로 관리함
        self.items = 0 #플레이어가 공격성 아이템을 획득 시 공격 한번 할때마다 차감되도록 설정
        
        '''
        여기에서 이미지파일을 기반으로 스프라이트 및 히트박스들을 관리함
        '''
        rightstatic = []
        rightdead = []
        rightwalk = []
        rightattack = []
        rightgetattack = []
        leftwalk = []
        leftstatic = []
        leftdead = []
        leftattack = []
        leftgetattack = []

        self.rightlist = [rightstatic, rightwalk, rightattack, rightgetattack ,rightdead]
        self.leftlist = [leftstatic, leftwalk, leftattack, leftgetattack ,leftdead]
        self.curlist = self.rightlist
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
    def SetStat(self, HP, ATK, DEF, SPEED):
        '''
        오브젝트의 스텟을 설정하는 메서드
        '''
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.SPEED = SPEED
        
    def ChangeStat(self, HP=0, ATK=0, DEF=0, SPEED=0):
        '''
        오브젝트의 스텟의 변화를 주는 메서드
        주로 아이템이나 적의 공격을 받을 때 쓰인다
        '''
        self.HP += HP
        self.ATK += ATK
        self.DEF += DEF
        self.SPEED += SPEED
    
    def GetStat(self, stat):
        '''
        오브젝트의 스텟 반환
        '''
        try:
            if (stat == 'hp'):
                return self.HP
            elif (stat == 'atk'):
                return self.ATK
            elif (stat == 'def'):
                return self.DEF
            elif (stat == 'speed'):
                return self.SPEED
            else:
                raise ValueError
        except ValueError:
            print('Not Stat!!')
    
    def GetCondition(self, condition):
        '''
        오브젝트의 상태 불값에 대해 반환함
        '''
        try:
            if (condition == 'direction'):
                return self.direction
            elif (condition == 'onground'):
                return self.isOnGround
            elif (condition == 'walk'):
                return self.isWalk
            elif (condition == 'attack'):
                return self.isAttack
            elif (condition == 'getattack'):
                return self.isGetattack
            elif (condition == 'dead'):
                return self.isDead
            elif (condition == 'hitbox'):
                return self.isHitbox
            else:
                raise ValueError
        except ValueError:
            print('Not Condition!!')
    
    def GetPos(self, pos):
        '''
        오브젝트의 위치 반환
        '''
        try:
            if (pos == 'x'):
                return self.hitbox.x
            elif (pos == 'y'):
                return self.hitbox.y
            else:
                raise ValueError
        except ValueError:
            print('Not Pos!!!!')
    
    def GetSize(self, length):
        '''
        오브젝트의 크기 반환
        '''
        try:
            if (length == 'width'):
                return self.hitbox.width
            elif (length == 'height'):
                return self.hitbox.height
            else:
                raise ValueError
        except ValueError:
            print('Not Lenght!!!')
    
    def GetProjectiles(self):
        '''
        오브젝트의 투사체 리스트 반환
        '''
        return self.projectilelist
        
    def checkcollision(self, Anathor):
        '''
        히트박스간에 충돌을 검사하는 함수
        주로 클래스 내에서만 쓰이는 함수이다
        '''
        if (pygame.Rect.colliderect(self.hitbox, Anathor.hitbox)):
            return True
        else:
            return False
        
    def leftwalk(self):
        '''
        왼쪽으로 걷는 상태를 설정하는 메서드
        '''
        if (self.isDead is False): # 만일 이 조건문이 없을 시 죽은 후에도 방향전환이 됨. 아래도 동일
            self.isWalk = True
            self.isAttack = False
            self.direction = LEFT
        
    def rightwalk(self):
        '''
        오른쪽으로 걷는 상태를 설정하는 메서드
        '''
        if (self.isDead is False):
            self.isWalk = True
            self.isAttack = False
            self.direction = RIGHT
        
    def jump(self):
        '''
        오브젝트의 점프 상태를 설정하는 메서드
        오브젝트가 지면으로부터 붕 떠져있는 경우 더 이상 위로 올라가지 않게 수정
        '''
        if (self.isDead is False):
            self.isOnGround = False
            if (self.hitbox.bottom < MAP_GROUND):
                self.y_pos += 0
            else:
                self.y_pos += JUMP_SPEED
                
    def attack(self):
        '''
        오브젝트의 공격 상태를 설정하는 메서드
        '''
        self.isWalk = False
        self.isAttack = True
            
    def getattack(self, Another):
        '''
        플레이어의 피격 상태를 표현해주는 메서드
        적의 위치상태에 따라 방향, 밀려나는 거리를 설정
        '''
        self.isGetattack = True
        self.isWalk = False
        self.isAttack = False
        self.HP -= (Another.GetStat(ATK) - self.DEF)
        if (self.x_pos > Another.GetPos(X)):
            self.direction = LEFT
            self.x_pos += self.GETATTACK
        else:
            self.direction = RIGHT
            self.x_pos -= self.GETATTACK

    def dead(self):
        '''
        오브젝트가 죽었음을 나타내는 메서드
        '''
        self.isDead = True
        self.GETATTACK = 0
        self.isHitbox = False
        self.isWalk = False
        self.isAttack = False
        self.isGetattack = False
        
    def notWalk(self):
        '''
        걷지 않도록 해주는 메서드
        '''
        self.isWalk = False
        
    def notAttack(self):
        '''
        공격하지 않도록 해주는 메서드
        '''
        self.isAttack = False
        
    def notGetattack(self):
        '''
        오브젝트가 피격 상태가 아님을 나타내는 메서드
        '''
        self.isGetattack = False
        
    def notDead(self):
        '''
        오브젝트가 죽은 상태가 아님을 나타내는 메서드
        '''
        self.isDead = False
    
    def drawpos(self):
        '''
        오브젝트의 위치에 따라 화면에 그려주는 메서드
        '''
        Screen.blit(self.cursprite, (self.hitbox.x, self.hitbox.y))

    def drawStat(self):
        '''
        오브젝트의 스텟을 화면에 그려주는 메서드
        이 메서드는 자식 클래스에서 오버라이딩하게끔 수정
        '''
        pass
        
    def draw(self):
        '''
        통합 draw 메서드
        가독성을 위해서
        '''
        self.drawpos()
        self.drawStat()
        
    def updatepos(self):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        '''
        self.hitbox.x = self.x_pos
        self.hitbox.y = self.y_pos

        if (self.isOnGround is False):
            self.y_pos += GRAVITY
        if (self.hitbox.bottom >= MAP_GROUND):
            self.y_pos = MAP_GROUND - self.hitbox.height
            self.isOnGround = True
        if (self.hitbox.left <= MAP_LIMIT_LEFT):
            self.x_pos = MAP_LIMIT_LEFT
        if (self.hitbox.right >= MAP_LIMIT_RIGHT):
            self.x_pos = MAP_LIMIT_RIGHT - self.hitbox.width
            
        if (self.isWalk is True and self.isAttack is False):
            if (self.direction == LEFT):
                self.x_pos += -self.SPEED
            elif (self.direction == RIGHT):
                self.x_pos += self.SPEED

    def updatesprite(self):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        '''
        오브젝트의 스프라이트 및 히트박스를 업데이트해주는 메서드
        '''
        if (self.direction == LEFT):
            self.curlist = self.leftlist
        elif (self.direction == RIGHT):
            self.curlist = self.rightlist
        
        if (self.isWalk is False or self.isAttack is False or
            self.isDead is False or self.isGetattack is False):
            self.cur = 0
        if (self.isWalk is True):
            self.cur = 1
        if (self.isAttack is True):
            self.cur = 2
        if (self.isGetattack is True):
            self.cur = 3
            self.notGetattack()
        if (self.HP <= 0):
            self.cur = 4
            self.dead()

        self.index += 1
        if (self.index >= len(self.curlist[self.cur])):
            self.index = 0
        
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(topleft=(self.x_pos, self.y_pos))
        
    def update(self):
        '''
        통합 update 메서드
        가독성을 위해
        '''
        self.updatepos()
        self.updatesprite()
        
class Player(Life):
    def __init__(self, x_pos, y_pos=None):
        self.x_pos = x_pos 
        if (y_pos is None):
            self.y_pos = MAP_GROUND
        else:
            self.y_pos = y_pos
        self.HP = 1000
        self.ATK = 100
        self.DEF = 0
        self.SPEED = 10
        self.GETATTACK = 80 #피격당할 시 넉백되는 거리를 설정

        self.direction = RIGHT
        self.isDead = False
        self.isAttack = False
        self.isWalk = False
        self.isOnGround = True
        self.isGetattack = False
        self.isHitbox = True #사망 시에 히트박스 없는 것으로 처리
        self.index = 0 #각 스프라이트 리스트의 인덱스
        self.cur = 0 #각 스프라이트 덩어리의 인덱스
        self.projectilelist = [] #플레이어가 공격판정이 정해질 때 리스트로 따로 관리함
        self.items = 0 #플레이어가 공격성 아이템을 획득 시 공격 한번 할때마다 차감되도록 설정
        
        self.atkcool = 5
        
        rightstatic = [pygame.image.load('char_sprite/char_static.png')]
        rightdead = [pygame.image.load('char_sprite/char_dead.png')]
        rightwalk = [pygame.image.load('char_sprite/char_walk_' + str(i) + '.png') for i in range(1, 4)]
        rightattack = [pygame.image.load('char_sprite/char_attack.png')]
        rightgetattack = [pygame.image.load('char_sprite/char_get_attack.png')]
        leftwalk = [pygame.transform.flip(rightwalks, True, 0) for rightwalks in rightwalk]
        leftstatic = [pygame.transform.flip(rightstatic[0], True, 0)]
        leftdead = [pygame.transform.flip(rightdead[0], True, 0)]
        leftattack = [pygame.transform.flip(rightattack[0], True, 0)]
        leftgetattack = [pygame.transform.flip(rightgetattack[0], True, 0)]

        self.rightlist = [rightstatic, rightwalk, rightattack, rightgetattack ,rightdead]
        self.leftlist = [leftstatic, leftwalk, leftattack, leftgetattack ,leftdead]
        self.curlist = self.rightlist
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
                
    def attack(self):
        '''
        플레이어의 공격 상태를 설정하는 메서드
        플레이어는 원거리 공격을 주로 하므로 공격판정마다 projectilelist 내에 방향을 추가
        (overriding)
        '''
        self.isWalk = False
        self.isAttack = True
        
        if (self.isDead is False):   #? 왜 isAttack is True가 조건문일때는 버그가? -> 키입력은 내가 설정한 bool 변수와는 하등 관계가 없나?
            if (self.direction == LEFT):
                self.projectilelist.append(Bubble(self.hitbox.left, self.hitbox.y, self.ATK, LEFT))
            else:
                self.projectilelist.append(Bubble(self.hitbox.right, self.hitbox.y, self.ATK, RIGHT))
        
    def getItem(self, Item):
        '''
        아이템을 얻게 해주는 메서드
        '''
        for Item in Itemlist:
            pass

    def drawStat(self):
        Length = self.HP / 5
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (10, 10, Length, 30))
        write('ATK: ' + str(self.ATK), BLACK, 70, 60)
        write('DEF: ' + str(self.DEF), BLACK, 70, 100)
        write('SPEED: ' + str(self.SPEED), BLACK, 85, 140)
        
    def updatepos(self):
        super().updatepos()
        for Enemy in Enemylist:
            if (self.isHitbox is True):
                if (self.checkcollision(Enemy) is True and Enemy.GetCondition(HITBOX) is True):
                    self.getattack(Enemy)

class Enemy(Life):
    def __init__(self, x_pos, y_pos=None):
        self.x_pos = x_pos
        if (y_pos is None):
            self.y_pos = MAP_GROUND
        else:
            self.y_pos = y_pos
        self.HP = 2500
        self.ATK = 70
        self.DEF = 40
        self.SPEED = 7
        self.GETATTACK = 80 #피격당할 시 넉백되는 거리를 설정

        self.direction = LEFT
        self.isDead = False
        self.isAttack = False
        self.isWalk = False
        self.isOnGround = True
        self.isGetattack = False
        self.isHitbox = True
        self.index = 0
        self.cur = 0
        
        rightstatic = [pygame.image.load('enemy_sprite/enemy_static.png')]
        rightdead = [pygame.image.load('char_sprite/char_dead.png')]
        rightwalk = [pygame.image.load('enemy_sprite/enemy_walk_' + str(i) + '.png') for i in range(1, 3)]
        rightattack = [pygame.image.load('char_sprite/char_attack.png')]
        rightgetattack = [pygame.image.load('char_sprite/char_get_attack.png')]
        leftwalk = [pygame.transform.flip(rightwalks, True, 0) for rightwalks in rightwalk]
        leftstatic = [pygame.transform.flip(rightstatic[0], True, 0)]
        leftdead = [pygame.transform.flip(rightdead[0], True, 0)]
        leftattack = [pygame.transform.flip(rightattack[0], True, 0)]
        leftgetattack = [pygame.transform.flip(rightgetattack[0], True, 0)]

        self.rightlist = [rightstatic, rightwalk, rightattack, rightgetattack ,rightdead]
        self.leftlist = [leftstatic, leftwalk, leftattack, leftgetattack ,leftdead]
        self.curlist = self.leftlist
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
    
    def AI(self, player):
        '''
        기본적의 적의 AI
        플레이어에 상태에 따라서 업데이트가 된다
        '''
        distance = self.hitbox.centerx - (player.GetPos(X) + player.GetSize(WIDTH)) #플레이어와 적과의 거리를 계산함
        dx1 = int(self.hitbox.width / 2) #히트박스의 절반
        dx2 = int(player.GetSize(WIDTH) / 2) #히트박스의 절반
        if (distance > 0):
            self.leftwalk()
        else:
            self.rightwalk()
        
        if (abs(distance) < dx1 + dx2):
            if (player.GetCondition(HITBOX) is True):
                self.attack()
        
        for projectile in player.GetProjectiles(): 
            if (len(player.GetProjectiles()) != 0):
                if (self.isHitbox is True):
                    if (self.checkcollision(projectile) is True):
                        self.getattack(player)
                        player.GetProjectiles().remove(bubble)
        
    def drawStat(self):
        Length = self.HP / 20
        DisplayLength = 2500 / 20
        pygame.draw.rect(Screen, RED, (self.hitbox.centerx - DisplayLength / 2,
                                       self.hitbox.bottom + 18, DisplayLength, 12), 1)
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (self.hitbox.centerx - DisplayLength / 2,
                                           self.hitbox.bottom + 19, Length, 10))

class Boss(object):
    def __init__(self):
        pass

font = pygame.font.SysFont('굴림', 40)
def write(Text, color, x_pos, y_pos):
    surface = font.render(Text, True, color)
    rect = surface.get_rect()
    rect.center = (x_pos, y_pos)
    Screen.blit(surface, rect)

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
Time = pygame.time.get_ticks()

# make enemylist!!!
mapimage = pygame.image.load('display.png')
mapscale = pygame.transform.scale(mapimage, (800, 600))

Itemlist = [] #-> 전역변수화 atk, def, speed, hp
player = Player(300)
Enemylist = [Enemy(600)]

while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                player.leftwalk()
            elif (event.key == pygame.K_RIGHT):
                player.rightwalk()
            elif (event.key == pygame.K_UP):
                player.jump()
            elif (event.key == pygame.K_x):
                player.attack()
            elif (event.key == pygame.K_z): #아이템 획득 키
                pass
            elif (event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        elif (event.type == pygame.KEYUP):
            if (event.key == pygame.K_LEFT or
                event.key == pygame.K_RIGHT):
                player.notWalk()

            elif (event.key == pygame.K_x):
                player.notAttack()
                
    Screen.blit(mapscale, (0, 0))
    player.draw()
    player.update()
    if (len(player.GetProjectiles()) != 0):
        for bubble in player.GetProjectiles():
            bubble.move()
            bubble.draw()
            
    for enemy in Enemylist:
        if (len(Enemylist) != 0):
            enemy.AI(player)
            enemy.draw()
            enemy.update()
    write('FPS: ' + str(int(Clock.get_fps())) + '   ' + str(pygame.time.get_ticks()), BLACK, 400, 20)
    pygame.display.update()
    Clock.tick(FPS)
