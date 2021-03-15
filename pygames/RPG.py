import pygame
import sys
import random
import queue

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

'''
아이템 이미지, 이펙트 관련 변수
'''
ICE = 'char_sprite/ice.png'
ARMOR = 'items/shield.png'
HASTE = 'items/haste.png'

BASIC = 'char_sprite/bubble.png'
REINFORCE = 'char_sprite/ice.png'

'''
오브젝트 관련 리스트 및 변수
'''
Enemylist = [] # 화면에 그릴 적 리스트
Deadboollist = [] # 적들이 생존해있는지 아닌지 체크해주는 리스트. 만일 모든 리스트 요소가 참일 경우 스테이지 종료되도록 설정

Enemydic = {'Near': list(),
            'Distance': list(),
            'Boss': list()} #추후 쓰일 적 딕셔너리 타입. 딕셔너리 타입에 따라 스텟을 조정할 예정
ItemTypes = [ICE, ARMOR, HASTE] # 아이템 타입, 주로 스프라이트 파일로 통해 아이템 획득을 구분할 예정
Itemlist = [] # 아이템을 담는 리스트

'''
텍스트 작성 함수
'''
Font = pygame.font.SysFont('굴림', 40)

def write(Font, Text, color, x_pos, y_pos):
    surface = Font.render(Text, True, color)
    rect = surface.get_rect()
    rect.center = (x_pos, y_pos)
    Screen.blit(surface, rect)

'''
기본적인 색상
'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
VIRGINRED = (204, 0, 0)

'''
기본적인 시스템 변수 설정
'''
x_size = 800
y_size = 600
startTime = pygame.time.get_ticks()
FPS = 60

# make enemylist!!!
mapimage = pygame.image.load('display.png')
mapscale = pygame.transform.scale(mapimage, (800, 600))

class Projectile(object):
    '''
    해당 클래스는 투사체의 기본적인 틀을 정해놓았다. 기본적으로는 버블임
    '''
    def __init__(self, image, x_pos, y_pos, ATK, direction):
        '''
        생성자에서 위치, 스텟, 방향, 이미지, 히트박스 설정을 관리함
        '''
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.ATK = ATK
        self.SPEED = 7
        self.direction = direction
        tmpimage = pygame.image.load(image)
        self.image = pygame.transform.scale(tmpimage, (30, 30))
        self.hitbox = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        
    def SetStat(self, ATK, SPEED):
        '''
        투사체의 스텟 설정
        '''
        self.ATK = ATK
        self.SPEED = SPEED
        
    def GetPos(self, pos):
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
        
    def draw(self):
        '''
        스크린에다가 투사체를 그려넣음
        '''
        Screen.blit(self.image, (self.hitbox.x, self.hitbox.y))
        
    def move(self):
        '''
        투사체가 자동으로 움직이도록 하는 메서드
        업데이트까지 겸함
        '''
        if (self.direction == LEFT):
            self.hitbox.x += -self.SPEED
        else:
            self.hitbox.x += self.SPEED
            
        if (self.hitbox.left <= MAP_LIMIT_LEFT or self.hitbox.right >= MAP_LIMIT_RIGHT):
            return 'delete'

    def checkcollision(self, enemy):
        '''
        충돌 판정
        '''
        if (pygame.Rect.colliderect(self.hitbox, enemy.hitbox)):
            return True
        else:
            return False

class Item(object):
    def __init__(self, x_pos, y_pos, image):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = image # 이미지 파일 정보...(일단 임시임)
        self.sprite = pygame.image.load(image)
        self.hitbox = self.sprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
    def GetImage(self):
        return self.image
    
    def draw(self):
        Screen.blit(self.sprite, (self.hitbox.x, self.hitbox.y))

    def checkcollision(self, Player):
        if (pygame.Rect.colliderect(self.hitbox, Player.hitbox)):
            return True
        else:
            return False
    
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
        self.KNOCKBACK = 80 #피격당할 시 넉백되는 거리를 설정
        
        '''
        오브젝트의 전체적인 상태를 나타내는 변수들
        '''
        self.direction = RIGHT
        self.isDead = False
        self.isAttack = False
        self.isWalk = False
        self.isOnGround = True
        self.isGetattack = False
        self.isHitbox = True # 사망 시에 히트박스 없는 것으로 처리
        self.isChangeStat = False # 스텟 변경이 되는지에 대한 불값
        self.index = 0 # 각 스프라이트 리스트의 인덱스
        self.cur = 0 #각 스프라이트 덩어리의 인덱스
        self.curtime = 0
        
    def InitStat(self):
        '''
        초기 스텟
        '''
        pass
    
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
        pass
    
    def GetSize(self, length):
        '''
        오브젝트의 크기 반환
        '''
        pass
        
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
        if (self.x_pos + self.hitbox.width / 2 > Another.GetPos(X) + Another.GetSize(WIDTH) / 2):
            self.direction = LEFT
            self.x_pos += self.KNOCKBACK
        else:
            self.direction = RIGHT
            self.x_pos -= self.KNOCKBACK

    def dead(self):
        '''
        오브젝트가 죽었음을 나타내는 메서드
        '''
        self.isDead = True
        self.KNOCKBACK = 0
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
        self.hitbox.bottom = self.y_pos

        if (self.isOnGround is False):
            self.y_pos += GRAVITY
        if (self.y_pos >= MAP_GROUND):
            self.y_pos = MAP_GROUND
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
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
    def update(self):
        '''
        통합 update 메서드
        가독성을 위해
        '''
        self.updatepos()
        self.updatesprite()
        
class Player(Life):
    def __init__(self, x_pos, y_pos=None):
        super().__init__(x_pos, y_pos)
        
        self.direction = RIGHT
        self.getitem = False
        self.itemType = None
        self.projectileimage = 'char_sprite/bubble.png'
        self.projectilelist = []
        self.itemQueue = queue.Queue(1)
        self.ammunition = 30 # 강화 공격 제한 개수
        self.startTime = 0
        self.elapsedTime = 0
        
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
        
    def InitStat(self):
        self.HP = 500
        self.ATK = 50
        self.DEF = 0
        self.SPEED = 10
        
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
        return self.projectilelist
                
    def attack(self):
        '''
        플레이어의 공격 상태를 설정하는 메서드
        플레이어는 원거리 공격을 주로 하므로 공격판정마다 projectilelist 내에 방향을 추가
        (overriding)
        '''
        super().attack()
        if (self.itemType == ICE):
            self.ammunition -= 1
        if (self.isDead is False):   #? 왜 isAttack is True가 조건문일때는 버그가? -> 키입력은 내가 설정한 bool 변수와는 하등 관계가 없나?
            if (self.direction == LEFT):
                self.projectilelist.append(Projectile(self.projectileimage, self.hitbox.left, self.hitbox.y, self.ATK, LEFT))
            else:
                self.projectilelist.append(Projectile(self.projectileimage, self.hitbox.right, self.hitbox.y, self.ATK, RIGHT))
            
        for projectile in self.projectilelist:
            if (projectile.move() == 'delete'):
                self.projectilelist.remove(projectile)
        
    def getItem(self):
        '''
        아이템을 얻게 해주는 메서드 아이템 종류에 따라 효과가 다르게 발동되도록 변경
        '''
        self.getitem = True
        
        for item in Itemlist:
            if (self.checkcollision(item) is True):
                Itemlist.remove(item)
                self.isChangeStat = True
                self.itemQueue.push(item.GetImage())
                if (item.GetImage() == ICE):
                    self.itemType = ICE
                    self.ChangeStat(0, 10, 0, 0)
                    self.projectileimage = REINFORCE
                elif (item.GetImage() == ARMOR):
                    self.itemType = ARMOR
                    self.ChangeStat(0, 0, 20, 0)
                    self.startTime = pygame.time.get_ticks()
                elif (item.GetImage() == HASTE):
                    self.itemType = HASTE
                    self.ChangeStat(0, 0, 0, 5)
                    self.startTime = pygame.time.get_ticks()

    def drawStat(self):
        Length = self.HP / 5
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (10, 10, Length, 30))
            
        if (self.itemType == ICE):
            pass
        elif (self.itemType == ARMOR):
            pass
        elif (self.itemType == HASTE):
            pass
            
    def updateCondition(self):
        '''
        플레이어의 아이템 획득마다 상태를 업데이트시켜주는 함수
        '''
        itemQueue = queue.Queue(1)
        itemQueue.put('None')
        for enemy in Enemylist:
            if (self.isHitbox is True):
                if (self.checkcollision(enemy) is True and enemy.GetCondition(HITBOX) is True): #??? 충돌 판정일 경우에는 왜 피격 판정이 참값이 아닐까???
                    self.getattack(enemy)
                    
        if (self.getitem is True and self.isChangeStat is True):
            if (self.itemType == ICE):
                if (self.ammunition == 0):
                    itemQueue.pop()
                    self.itemType = None
                    self.ChangeStat(0, -10, 0, 0)
                    self.projectileimage = BASIC
                    self.isChangeStat = False
                    self.ammunition = 30
            elif (self.itemType == ARMOR):
                self.elapsedTime = (pygame.time.get_ticks() - self.startTime) / 1000
                if (self.elapsedTime > 20):
                    self.itemType = None
                    self.ChangeStat(0, 0, -20, 0)
                    self.isChangeStat = False
                    self.elapsedTime = 0
                    self.startTime = 0
            elif (self.itemType == HASTE):
                self.elapsedTime = (pygame.time.get_ticks() - self.startTime) / 1000
                if (self.elapsedTime > 20):
                    self.itemType = None
                    self.ChangeStat(0, 0, 0, -5)
                    self.isChangeStat = False
                    self.elapsedTime = 0
                    self.startTime = 0

        
    def update(self):
        self.updateCondition()
        super().update()

class Enemy(Life):
    def __init__(self, x_pos, y_pos=None):
        super().__init__(x_pos, y_pos)
        
        self.direction = LEFT
        self.isDrop = False # 아이템 드랍 관련 불값
        self.curtime = 0
        self.attackRange = 70 # 공격 범위
        
        rightstatic = [pygame.image.load('enemy_sprite/enemy_static.png')]
        rightdead = [pygame.image.load('enemy_sprite/enemy_dead.png')]
        rightwalk = [pygame.image.load('enemy_sprite/enemy_walk_' + str(i) + '.png') for i in range(1, 3)]
        rightattack = [pygame.image.load('enemy_sprite/enemy_attack_' + str(i) + '.png') for i in range(1, 3)]
        rightgetattack = [pygame.image.load('enemy_sprite/enemy_get_attack.png')]
        leftwalk = [pygame.transform.flip(rightwalks, True, 0) for rightwalks in rightwalk]
        leftstatic = [pygame.transform.flip(rightstatic[0], True, 0)]
        leftdead = [pygame.transform.flip(rightdead[0], True, 0)]
        leftattack = [pygame.transform.flip(rightattacks, True, 0) for rightattacks in rightattack]
        leftgetattack = [pygame.transform.flip(rightgetattack[0], True, 0)]

        self.rightlist = [rightstatic, rightwalk, rightattack, rightgetattack ,rightdead]
        self.leftlist = [leftstatic, leftwalk, leftattack, leftgetattack ,leftdead]
        self.curlist = self.leftlist
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
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

    def dropItem(self):
        '''
        아이템을 드롭시키는 함수, 나중에 확률에 따라 드랍시킬 생각
        '''
        image = random.choice(ItemTypes)
        Itemlist.append(Item(self.x_pos, self.y_pos, image))
    
    def AI(self, player):
        '''
        기본적의 적의 AI
        플레이어에 상태에 따라서 업데이트가 된다
        '''
        distance = self.hitbox.centerx - (player.GetPos(X) + player.GetSize(WIDTH) / 2) #플레이어와 적과의 거리를 계산함
        if (distance > 0):
            self.leftwalk()
        else:
            self.rightwalk()

        if (abs(distance) <= self.attackRange):
            if (player.GetCondition(HITBOX) is True):
                self.notWalk()
                self.attack()

        for projectile in player.GetProjectiles():
            if (len(player.GetProjectiles()) != 0):
                if (self.isHitbox is True):
                    if (self.checkcollision(projectile) is True):
                        self.getattack(player)
                        player.GetProjectiles().remove(projectile)

        if (self.isDead is True and self.isDrop is False):
            self.dropItem()
            self.isDrop = True

    def drawStat(self):
        Length = self.HP / 20
        DisplayLength = 2500 / 20
        pygame.draw.rect(Screen, VIRGINRED, (self.hitbox.centerx - DisplayLength / 2,
                                             self.hitbox.bottom + 18, DisplayLength, 12), 3)
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (self.hitbox.centerx - DisplayLength / 2,
                                           self.hitbox.bottom + 19, Length, 9))
            
    def updatesprite(self):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        super().updatesprite()
        if (self.direction == LEFT):
            self.hitbox = self.cursprite.get_rect(bottomright=(self.x_pos + self.attackRange, self.y_pos)) #방향전환시 좌표오류를 잡아줌
        else:
            self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))

class Boss(Enemy):
    def __init__(self, x_pos, y_pos=None):
        super().__init__(x_pos, y_pos)
        
        self.curtime = 0
        self.attackRange = 70
        
        rightstatic = [pygame.image.load('enemy_sprite/enemy_static.png')]
        rightdead = [pygame.image.load('enemy_sprite/enemy_dead.png')]
        rightwalk = [pygame.image.load('enemy_sprite/enemy_walk_' + str(i) + '.png') for i in range(1, 3)]
        rightattack = [pygame.image.load('enemy_sprite/enemy_attack_' + str(i) + '.png') for i in range(1, 3)]
        rightgetattack = [pygame.image.load('enemy_sprite/enemy_get_attack.png')]
        leftwalk = [pygame.transform.flip(rightwalks, True, 0) for rightwalks in rightwalk]
        leftstatic = [pygame.transform.flip(rightstatic[0], True, 0)]
        leftdead = [pygame.transform.flip(rightdead[0], True, 0)]
        leftattack = [pygame.transform.flip(rightattacks, True, 0) for rightattacks in rightattack]
        leftgetattack = [pygame.transform.flip(rightgetattack[0], True, 0)]

        self.rightlist = [rightstatic, rightwalk, rightattack, rightgetattack ,rightdead]
        self.leftlist = [leftstatic, leftwalk, leftattack, leftgetattack ,leftdead]
        self.curlist = self.leftlist
        self.cursprite = self.curlist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
            
    def dropItem(self):
        '''
        아이템을 드롭시키는 함수, 나중에 확률에 따라 드랍시킬 생각
        '''
        pass
    
    def AI(self, player):
        '''
        기본적의 적의 AI
        플레이어에 상태에 따라서 업데이트가 된다
        '''
        pass
        
    def drawStat(self):
        pass

def StartScreen():
    while True:
        Screen.fill(WHITE)
        write(BigFont, 'Tetris', BLACK, x_size / 2, y_size / 2)
        write(BigFont, 'Press S!', BLACK, x_size / 2, 450)
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
    write(BigFont, 'GameOver!!!', BLUE, x_size / 2, 300)
    write(BigFont, 'Try Again?', BLUE, x_size / 2, 370)
    write(BigFont, 'Y / N', BLUE, x_size / 2, 440)
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
    
    global Enemy, Item
    player = Player(300)
    enemy = Enemy(600)
    player.InitStat()
    Enemylist.append(enemy)
    Itemlist.append(Item(100, MAP_GROUND, ARMOR))
    Itemlist.append(Item(150, MAP_GROUND, ARMOR))
    for Enemy in Enemylist:
        Deadboollist.append(Enemy.GetCondition(DEAD))
    for Enemy in Enemylist:
        Enemy.SetStat(2500, 40, 10, 2)

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
                    player.getItem()
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
            for projectile in player.GetProjectiles():
                projectile.move()
                projectile.draw()
                
            for projectile in player.GetProjectiles():
                if (projectile.GetPos(X) <= MAP_LIMIT_LEFT or
                    projectile.GetPos(X) + projectile.GetSize(WIDTH) >= MAP_LIMIT_RIGHT):
                    player.GetProjectiles().remove(projectile)
            
        for enemy in Enemylist:
            if (len(Enemylist) != 0):
                enemy.AI(player)
                enemy.draw()
                enemy.update()
                
        for item in Itemlist:
            if (len(Itemlist) != 0):
                item.draw()
            
        write(SmallFont, str(player.DEF) + '   ' + str(player.elapsedTime), BLACK, 400, 20)
        pygame.display.update()
        Clock.tick(FPS)
    
def main():
    global Clock, Screen, BigFont, SmallFont
    pygame.init()
    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((x_size, y_size))
    BigFont = pygame.font.SysFont('굴림', 70)
    SmallFont = pygame.font.SysFont('굴림', 40)
    
    pygame.display.set_caption("RPG")
    
    rungame()
    
if (__name__ == '__main__'):
    main()