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

LEFT = 'LEFT'
RIGHT = 'RIGHT'

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
    def __init__(self):
        pass
    
class Player(object):
    def __init__(self, x_pos, y_pos=None):
        '''
        플레이어의 생성 위치, 기본 스텟, 상태 표시, 스프라이트 생성같은
        기본적인 요소를 생성자 안에다 넣음
        '''
        self.x_pos = x_pos 
        self.y_pos = y_pos
        self.HP = 1000
        self.ATK = 500
        self.DEF = 20
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
        self.hitbox = self.cursprite.get_rect(topleft=(self.x_pos, self.y_pos))

    def InitPos(self):
        '''
        플레이어 생성 좌표를 재조정함
        '''
        self.y_pos = MAP_GROUND - self.hitbox.height
        
    def SetStat(self, HP, ATK, DEF, SPEED):
        '''
        플레이어의 스텟을 설정하는 메서드
        '''
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.SPEED = SPEED
        
    def ChangeStat(self, HP=0, ATK=0, DEF=0, SPEED=0):
        '''
        플레이어의 스텟의 변화를 주는 메서드
        주로 아이템이나 적의 공격을 받을 때 쓰인다
        '''
        self.HP += HP
        self.ATK += ATK
        self.DEF += DEF
        self.SPEED += SPEED
    
    def GetStat(self):
        '''
        플레이어 스텟 반환
        '''
        return [self.HP, self.ATK, self.DEF, self.SPEED]
    
    def GetPos(self):
        '''
        플레이어의 위치 반환
        '''
        return [self.hitbox.x, self.hitbox.y]
    
    def GetProjectiles(self):
        '''
        플레이어의 투사체 리스트 반환
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
        self.isWalk = True
        self.isAttack = False
        self.direction = LEFT
        
    def rightwalk(self):
        '''
        오른쪽으로 걷는 상태를 설정하는 메서드
        '''
        self.isWalk = True
        self.isAttack = False
        self.direction = RIGHT
        
    def jump(self):
        '''
        플레이어의 점프 상태를 설정하는 메서드
        플레이어가 지면으로부터 붕 떠져있는 경우 더 이상 위로 올라가지 않게 수정
        '''
        self.isOnGround = False
        if (self.hitbox.bottom < MAP_GROUND):
            self.y_pos += 0
        else:
            self.y_pos += JUMP_SPEED
                
    def attack(self):
        '''
        플레이어의 공격 상태를 설정하는 메서드
        플레이어는 원거리 공격을 주로 하므로 공격판정마다 projectilelist 내에 방향을 추가
        '''
        self.isWalk = False
        self.isAttack = True
        
        if (self.direction == LEFT):
            self.projectilelist.append(Bubble(self.hitbox.left, self.hitbox.y, self.ATK, LEFT))
        else:
            self.projectilelist.append(Bubble(self.hitbox.right, self.hitbox.y, self.ATK, RIGHT))
            
    def getattack(self, Enemy):
        '''
        플레이어의 피격 상태를 표현해주는 메서드
        적의 위치상태에 따라 방향, 밀려나는 거리를 설정
        '''
        self.isGetattack = True
        self.isWalk = False
        self.isAttack = False
        if (self.x_pos > Enemy.x_pos):
            self.direction = LEFT
            self.x_pos += self.GETATTACK
        else:
            self.direction = RIGHT
            self.x_pos -= self.GETATTACK

    def dead(self):
        '''
        플레이어가 죽었음을 나타내는 메서드
        '''
        self.isDead = True
        self.GETATTACK = 0
        self.isHitbox = False

    def notWalk(self):
        '''
        키보드에서 손뗄 시 걷지 않도록 해주는 메서드
        '''
        self.isWalk = False
        
    def notAttack(self):
        '''
        키보드에서 손뗄 시 공격하지 않도록 해주는 메서드
        '''
        self.isAttack = False
        
    def notGetattack(self):
        '''
        플레이어의 피격 상태가 아님을 나타내는 메서드
        '''
        self.isGetattack = False
        
    def getItem(self, Item):
        '''
        아이템을 얻게 해주는 메서드
        '''
        pass
    
    def drawpos(self):
        '''
        플레이어의 위치에 따라 화면에 그려주는 메서드
        '''
        Screen.blit(self.cursprite, (self.hitbox.x, self.hitbox.y))

    def drawStat(self):
        '''
        플레이어의 스텟을 화면에 그려주는 메서드
        '''
        Length = self.HP / 5
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (10, 10, Length, 30))
        write('ATK: ' + str(self.ATK), BLACK, 70, 60)
        write('DEF: ' + str(self.DEF), BLACK, 70, 100)
        write('SPEED: ' + str(self.SPEED), BLACK, 85, 140)
        
    def draw(self):
        '''
        통합 draw 메서드
        가독성을 위해서
        '''
        self.drawpos()
        self.drawStat()
        
    def updatepos(self):
        '''
        플레이어의 위치를 업데이트 시키는 메서드
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
        
        for Enemy in Enemylist:
            if (self.isHitbox is True):
                if (self.checkcollision(Enemy) is True):
                    self.getattack(Enemy)
                else:
                    self.notGetattack()

    def updatesprite(self):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        '''
        캐릭터의 스프라이트 상태를 업데이트해주는 메서드
        '''
        if (self.direction == LEFT):
            self.curlist = self.leftlist
        elif (self.direction == RIGHT):
            self.curlist = self.rightlist
        
        if (self.isWalk is False or self.isAttack is False or self.isDead is False):
            self.cur = 0
        if (self.isWalk is True):
            self.cur = 1
        if (self.isAttack is True):
            self.cur = 2
        if (self.isGetattack is True):
            self.cur = 3
        if (self.HP <= 0):
            self.cur = 4
            self.dead()

        self.index += 1
        if (self.index >= len(self.curlist[self.cur])):
            self.index = 0
        
        self.cursprite = self.curlist[self.cur][self.index]
        
    def update(self):
        '''
        통합 update 메서드
        가독성을 위해
        '''
        self.updatepos()
        self.updatesprite()

class Enemy(object):
    def __init__(self, x_pos, y_pos=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.HP = 2500
        self.ATK = 60
        self.DEF = 40
        self.SPEED = 4
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
        self.curlist = self.leftlist
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(topleft=(self.x_pos, self.y_pos))
        
    def SetStat(self, HP, ATK, DEF, SPEED):
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.SPEED = SPEED
        
    def ChangeStat(self, HP=0, ATK=0, DEF=0, SPEED=0):
        self.HP += HP
        self.ATK += ATK
        self.DEF += DEF
        self.SPEED += SPEED
        
    def checkcollision(self, Anathor):
        if (pygame.Rect.colliderect(self.hitbox, Anathor.hitbox)):
            return True
        else:
            return False
        
    def leftwalk(self):
        '''
        왼쪽으로 걷는 상태를 설정하는 메서드
        '''
        self.isWalk = True
        self.isAttack = False
        self.direction = LEFT
        
    def rightwalk(self):
        '''
        오른쪽으로 걷는 상태를 설정하는 메서드
        '''
        self.isWalk = True
        self.isAttack = False
        self.direction = RIGHT
        
    def jump(self):
        '''
        적의 점프 상태를 설정하는 메서드
        적이 지면으로부터 붕 떠져있는 경우 더 이상 위로 올라가지 않게 수정
        '''
        self.isOnGround = False
        if (self.hitbox.bottom < MAP_GROUND):
            self.y_pos += 0
        else:
            self.y_pos += JUMP_SPEED
                
    def attack(self):
        '''
        적의 공격 상태를 설정하는 메서드
        '''
        self.isWalk = False
        self.isAttack = True
            
    def getattack(self, Player):
        '''
        적의 피격 상태를 표현해주는 메서드
        플레이어의 위치상태에 따라 방향, 밀려나는 거리를 설정
        '''
        self.isGetattack = True
        self.isWalk = False
        self.isAttack = False
        self.HP -= (Player.ATK - self.DEF)
        Player.projectilelist.remove(bubble)
        if (self.x_pos > Player.GetPos()[0]):
            self.direction = LEFT
            self.x_pos += self.GETATTACK
        else:
            self.direction = RIGHT
            self.x_pos -= self.GETATTACK
            
    def dead(self):
        '''
        적이 죽었음을 나타내는 메서드
        '''
        self.isDead = True
        self.SPEED = 0
        self.GETATTACK = 0
        self.isHitbox = False

    def notWalk(self):
        '''
        걷지 않도록 해주는 메서드
        '''
        self.isWalk = False
        
    def notAttack(self):
        '''
        \공격하지 않도록 해주는 메서드
        '''
        self.isAttack = False
        
    def notGetattack(self):
        '''
        적의 피격 상태가 아님을 나타내는 메서드
        '''
        self.isGetattack = False
    
    def AI(self, player):
        '''
        기본적의 적의 AI
        플레이어에 상태에 따라서 업데이트가 된다
        '''
        distance = self.hitbox.centerx - player.hitbox.centerx #플레이어와 적과의 거리를 계산함
        dx1 = int(self.hitbox.width / 2) #히트박스의 절반
        dx2 = int(player.hitbox.width / 2) #히트박스의 절반
        if (distance > 0):
            self.leftwalk()
        else:
            self.rightwalk()
        
        if (abs(distance) <= dx1 + dx2):
            self.attack()
        
        for projectile in player.projectilelist: #플레이어 내에 변수에 직접 접근은 최대한 피하고 싶은데.... 방법 x?
            if (len(player.projectilelist) != 0):
                if (self.isHitbox is True):
                    if (self.checkcollision(projectile) is True):
                        self.getattack(player)
                    else:
                        self.notGetattack()
                        
        if (self.isDead is True):
            self.SPEED = 0
            self.GETATTACK = 0
            self.isHitbox = False

    def drawpos(self):
        Screen.blit(self.cursprite, (self.hitbox.x, self.hitbox.y))
        
    def drawStat(self):
        Length = self.HP / 20
        DisplayLength = 2500 / 20
        pygame.draw.rect(Screen, RED, (self.hitbox.centerx - DisplayLength / 2,
                                       self.hitbox.bottom + 18, DisplayLength, 12), 1)
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (self.hitbox.centerx - DisplayLength / 2,
                                           self.hitbox.bottom + 19, Length, 10))
            
    def draw(self):
        self.drawpos()
        self.drawStat()
    
    def updatepos(self):
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
    
    def updatesprite(self):
        if (self.direction == LEFT):
            self.curlist = self.leftlist
        elif (self.direction == RIGHT):
            self.curlist = self.rightlist
        
        if (self.isWalk is False or self.isAttack is False or self.isDead is False):
            self.cur = 0
        if (self.isWalk is True):
            self.cur = 1
        if (self.isAttack is True):
            self.cur = 2
        if (self.isGetattack is True):
            self.cur = 3
        if (self.HP <= 0):
            self.cur = 4
            self.dead()

        self.index += 1
        if (self.index >= len(self.curlist[self.cur])):
            self.index = 0
        
        self.cursprite = self.curlist[self.cur][self.index]
        
    def update(self):
        self.updatepos()
        self.updatesprite()

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

# make enemylist!!!
mapimage = pygame.image.load('display.png')
mapscale = pygame.transform.scale(mapimage, (800, 600))

Itemlist = ['ICE', 'ARMOR', 'HASTE', 'DOUBLE'] #-> 전역변수화
player = Player(300, 300)
player.InitPos()
Enemylist = [Enemy(600, MAP_GROUND)]

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
    if (len(player.projectilelist) != 0):
        for bubble in player.projectilelist:
            bubble.move()
            bubble.draw()
            
    for enemy in Enemylist:
        if (len(Enemylist) != 0):
            enemy.AI(player)
            enemy.draw()
            enemy.update()
    write(str(enemy.isDead), BLACK, 400, 20)
    pygame.display.update()
    Clock.tick(FPS)
