import pygame
import sys
import random

pygame.init() # pygame 초기화

MAP_GROUND = 465
MAP_HEIGHT = 0
MAP_LIMIT_LEFT = 0
MAP_LIMIT_RIGHT = 800
XMARGIN = 200

'''
오브젝트의 스텟 관련 변수
'''
MAXHP = 'maxhp'
HP = 'hp'
ATK = 'atk'
DEF = 'def'
SPEED = 'speed'

'''
오브젝트의 컨디션 관련 전역변수
'''
LEFT = 'left'
RIGHT = 'right'
DIRECTION = 'direction'
STATIC = 'static'
WALK = 'walk'
ATTACK = 'attack'
GETATTACK = 'getattack'
DEAD = 'dead'
HITBOX = 'hitbox'
ATKHITBOX = 'atkhitbox'
ONGROUND = 'onground'

'''
히트박스 사이즈 및 위치 전역변수
'''
X = 'x'
Y = 'y'
WIDTH = 'width'
HEIGHT = 'height'

'''
아이템 아이콘, 이펙트 관련 변수
'''
ICE = 'char_sprite/ice.png'
ARMOR = 'items/shield.png'
HASTE = 'items/haste.png'
ATTACKSPEED = 'items/attackspeed.png'

BASIC = 'char_sprite/bubble.png'
REINFORCE = 'char_sprite/ice.png'

ICEICON = pygame.image.load('char_sprite/ice.png')
ARMORICON = pygame.image.load('items/shield.png')
HASTEICON = pygame.image.load('items/haste.png')
ATTACKSPEEDICON = pygame.image.load('items/attackspeed.png')

DETECTICON = pygame.image.load('effect_icon/detectIcon.png')

'''
오브젝트 관련 리스트 및 변수 -> 이 리스트들을 GameStage 클래스 내부에 조만간 편입시켜야 할듯.
'''
Enemylist = [] # 화면에 그릴 적 리스트
Deadboollist = [] # 적들이 생존해있는지 아닌지 체크해주는 리스트. 만일 모든 리스트 요소가 참일 경우 스테이지 종료되도록 설정

Enemydic = {'Near': list(),
            'Distance': list(),
            'Boss': list()} #추후 쓰일 적 딕셔너리 타입. 딕셔너리 타입에 따라 스텟을 조정할 예정
ItemTypes = [ICE, ARMOR, HASTE, ATTACKSPEED] # 아이템 타입, 주로 스프라이트 파일로 통해 아이템 획득을 구분할 예정
Itemlist = [] # 아이템을 담는 리스트
Stagelist = [1, 2, 3, 4] # 스테이지 리스트 -> 반복문을 통하여 스테이지를 넘어가도록 설계함

'''
텍스트 작성 함수
'''
Font = pygame.font.SysFont('굴림', 40)

def write(Font, Text, color, x_pos, y_pos):
    surface = Font.render(Text, True, color)
    rect = surface.get_rect()
    Screen.blit(surface, (x_pos, y_pos))

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
FPS = 60

# make enemylist!!!
mapimage = pygame.image.load('display.png')
mapscale = pygame.transform.scale(mapimage, (800, 600))

class GameStage(object):
    '''
    해당 클래스는 게임 스테이지를 구현시켜주는 클래스로, 여기에서 스테이지 진행, 게임오버 화면, 클리어 화면, 오프닝, 카메라 뷰 등을 모두 다룸
    차후 나중에 구현할 예정
    '''
    def __init__(self, stage):
        self.stage = stage
        self.mapImages = [mapscale]
        
        self.player = None
        self.Enemylist = []
        self.Itemlist = []
        self.Deadboollist = []
        self.DeadCounts = 0
        
        self.score = 0
        
    def GetScore(self, Type):
        if (Type == 'item'):
            self.score += 10
    
    def OpeningScreen(self):
        while True:
            Screen.fill(WHITE)
            write(BigFont, 'Adventure', BLACK, XMARGIN, 200)
            write(BigFont, 'Press S!', BLACK, XMARGIN, 350)
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
    
    def GameGuide(self):
        while True:
            Screen.fill(WHITE)
            write(SmallFont, 'MANUAL', BLACK, XMARGIN, 30)
            write(SmallFont, '<-, -> : LEFT, RIGHT MOVE', BLACK, XMARGIN, 80)
            write(SmallFont, '^ : JUMP', BLACK, XMARGIN, 110)
            write(SmallFont, 'x : ATTACK', BLACK, XMARGIN, 140)
            write(SmallFont, 'z : GETITEM', BLACK, XMARGIN, 170)
            write(SmallFont, 'ESC : GAME TERMINATE', BLACK, XMARGIN, 200)
        
            Screen.blit(ICEICON, (XMARGIN, 240))
            write(SmallFont, ': REINFORCE ATK', BLACK, XMARGIN + 35, 240)
            Screen.blit(ARMORICON, (XMARGIN, 270))
            write(SmallFont, ': REINFORCE DEF', BLACK, XMARGIN + 35, 270)
            Screen.blit(HASTEICON, (XMARGIN, 300))
            write(SmallFont, ': REINFORCE SPEED', BLACK, XMARGIN + 35, 300)
            Screen.blit(ATTACKSPEEDICON, (XMARGIN, 330))
            write(SmallFont, ': REINFORCE ATTACKSPEED', BLACK, XMARGIN + 35, 330)
        
            write(SmallFont, 'PRESS S!', BLACK, XMARGIN, 500)
            pygame.draw.rect(Screen, BLACK, (0, 0, x_size, y_size), 5)
            pygame.display.update()
        
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_s):
                        return False
    
    def ClearScreen(self):
        for bools in Deadboollist:
            if (bools is True):
                self.DeadCounts += 1
        
        if (self.DeadCounts == len(Deadboollist)):
            
            
    
    def GameoverScreen(self):
        write(BigFont, 'GameOver!!!', BLUE, XMARGIN, 200)
        write(BigFont, 'Try Again?', BLUE, XMARGIN, 280)
        write(BigFont, 'Y / N', BLUE, XMARGIN, 360)
        pygame.display.update()
        pygame.time.wait(2000)
    
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_y):
                    self.ResetStage()
                elif (event.key == pygame.K_n):
                    pygame.quit()
                    sys.exit()
                    
    def SetStage(self):
        if (self.stage == 1):
            self.player = PlayerObject(150)
            enemy = EnemyObject(600)
            self.player.SetStat(MAXHP=500, HP=500, ATK=200, DEF=0, SPEED=5)
            Enemylist.append(enemy)
            for Enemy in Enemylist:
                Deadboollist.append(Enemy.GetCondition(DEAD))
            for Enemy in Enemylist:
                Enemy.SetStat(MAXHP=2500, HP=2500, ATK=80, DEF=10, SPEED=2)
    
    def DrawStage(self):
        Screen.blit(self.mapImages[self.stage - 1], (0, 0))
        
    def ResetStage(self):
        Enemylist.clear()
        Deadboollist.clear()
        Itemlist.clear()
        self.DeadCounts = 0
    
    def UpdateStage(self):
        pass

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
        '''
        아이템의 전체적인 정보를 저장하는 생성자
        '''
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = image # 이미지 파일 정보...(일단 임시임)
        self.icon = pygame.image.load(image)
        self.hitbox = self.icon.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
    def GetImage(self):
        '''
        아이템 아이콘 이미지를 반환하는 함수. 캐릭터의 아이템 획득 함수에 쓰임
        '''
        return self.image
    
    def draw(self):
        '''
        아이템을 그리는 함수
        '''
        Screen.blit(self.icon, (self.hitbox.x, self.hitbox.y))

    def checkcollision(self, Player):
        '''
        충돌판정 함수
        '''
        if (pygame.Rect.colliderect(self.hitbox, Player.hitbox)):
            return True
        else:
            return False
    
class LifeObject(object):
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
        self.MAXHP = 0
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
        self.attackHitbox = False # 공격 시의 히트박스(근접 타입의 적 및 캐릭터만 쓰이는 변수)
        self.isChangeStat = False # 스텟 변경이 되는지에 대한 불값
        self.isChangeCondition = False # 컨디션이 뒤바뀌었는지 검사하는 불값->이 값이 참이 될시에 current_time과 index가 0으로 초기화가 됨(기존에는 전환시에도 index와 current_time이 그대로라 스프라이트 업데이트가 잘 안됨)
        self.Condition = STATIC # 오브젝트의 컨디션
        
        self.gravity = 0 # 중력 계수
        self.airSpace = -12 # 점프 계수
        
        self.ChangeDelay = 0.1 # 컨디션 전환 딜레이
        self.delayStart = 0 # 딜레이 시작 시간
        self.delayElapsed = 0 # 딜레이 경과 시간
        
        self.effectTime = 1.5 # 이펙트 표기 시간
        self.effectStart = 0 # 이펙트 표기 시작 시간
        self.effectElapsed = 0 # 이펙트 표기 경과 시간
        
        self.atkcool = 0 # 공격 쿨타임
        self.coolStart = 0 # 쿨타임 시작 시간
        self.coolElapsed = 0 # 쿨타임 경과 시간
        
        self.index = 0 # 각 스프라이트 리스트의 인덱스
        self.cur = 0 #각 스프라이트 덩어리의 인덱스
                
        self.animation_time = 0 # 스프라이트 업데이트 총 주기
        self.current_time = 0 # 경과 시간
        
    def InitStat(self):
        '''
        초기 스텟
        '''
        pass
    
    def SetStat(self, MAXHP, HP, ATK, DEF, SPEED):
        '''
        오브젝트의 스텟을 설정하는 메서드
        '''
        self.MAXHP = MAXHP
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.SPEED = SPEED
        
    def ChangeStat(self, MAXHP=0, HP=0 ,ATK=0, DEF=0, SPEED=0, ATTACKSPEED=1):
        '''
        오브젝트의 스텟의 변화를 주는 메서드
        주로 아이템이나 적의 공격을 받을 때 쓰인다
        '''
        self.MAXHP += MAXHP
        self.HP += HP
        self.ATK += ATK
        self.DEF += DEF
        self.SPEED += SPEED
        self.atkcool /= ATTACKSPEED
    
    def GetStat(self, stat):
        '''
        오브젝트의 스텟 반환
        '''
        try:
            if (stat == 'maxhp'):
                return self.MAXHP
            elif (stat == 'hp'):
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
            elif (condition == 'atkhitbox'):
                return self.attackHitbox
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
        
    def static(self):
        '''
        오브젝트의 모든 상태 불값이 False인 경우 static으로 반환함
        '''
        if (self.Condition != STATIC):
            self.isChangeCondition = True
            self.delayStart = pygame.time.get_ticks()
        else:
            self.isChangeCondition = False
            
        self.isWalk = False
        self.isAttack = False
        self.isGetattack = False
        self.isDead = False
        
    def left(self):
        '''
        왼쪽 방향
        '''
        self.direction = LEFT
    
    def right(self):
        '''
        오른쪽 방향
        '''
        self.direction = RIGHT
        
    def walk(self):
        '''
        걷는 상태를 설정하는 메서드
        '''
        if (self.Condition != WALK):
            self.isChangeCondition = True
            self.delayStart = pygame.time.get_ticks()
        else:
            self.isChangeCondition = False
        
        if (self.isGetattack is False): # 만일 이 조건문이 없을 시 죽은 후에도 방향전환이 됨. 아래도 동일
            self.isWalk = True
            self.isAttack = False
            self.isGetattack = False
        else:
            self.isWalk = False
            
    def leftwalk(self):
        '''
        왼쪽방향으로 걷게 해주는 메서드
        사망시 방향전환 및 걷기가 안되도록 설정
        '''
        if (self.isDead is False):
            self.left()
            self.walk()
            
    def rightwalk(self):
        '''
        오른쪽방향으로 걷게 해주는 메서드
        사망시 방향전환 및 걷기가 안되도록 설정
        '''
        if (self.isDead is False):
            self.right()
            self.walk()
        
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
                self.y_pos -= 0.1
                
    def attack(self):
        '''
        오브젝트의 공격 상태를 설정하는 메서드
        공격 함수 호출 시 쿨타임이 돌아가도록 설정함
        '''
        if (self.Condition != ATTACK):
            self.isChangeCondition = True
            self.delayStart = pygame.time.get_ticks()
        else:
            self.isChangeCondition = False
        
        if (self.isGetattack is False and self.isDead is False and self.coolElapsed == 0):
            self.isWalk = False
            self.isAttack = True
            self.attackHitbox = True
            self.coolStart = pygame.time.get_ticks()
        else:
            self.isAttack = False
            
    def getattack(self, Another):
        '''
        플레이어의 피격 상태를 표현해주는 메서드
        적의 위치상태에 따라 방향, 밀려나는 거리를 설정
        '''
        if (self.Condition != GETATTACK):
            self.isChangeCondition = True
            self.delayStart = pygame.time.get_ticks()
        else:
            self.isChangeCondition = False
            
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
        if (self.isDead is False):
            self.isChangeCondition = True
        else:
            self.isChangeCondition = False
            
        self.isDead = True
        self.KNOCKBACK = 0
        self.isHitbox = False
        self.isWalk = False
        self.isAttack = False
        self.isGetattack = False
        self.flipPosible = False
    
    def drawPos(self):
        '''
        오브젝트의 위치에 따라 화면에 그려주는 메서드
        flipPosible 이 거짓일 경우 방향전환이 안되도록 함
        '''
        if (self.direction == LEFT):
            Screen.blit(pygame.transform.flip(self.cursprite, True, False), (self.hitbox.x, self.hitbox.y))
        else:
            Screen.blit(self.cursprite, (self.hitbox.x, self.hitbox.y))

    def drawStat(self):
        '''
        오브젝트의 스텟을 화면에 그려주는 메서드
        이 메서드는 자식 클래스에서 오버라이딩하게끔 수정
        '''
        pass
    
    def drawEffect(self):
        '''
        각종 이펙트를 그려주는 함수
        '''
        pass
        
    def draw(self):
        '''
        통합 draw 메서드
        가독성을 위해서
        '''
        self.drawEffect()
        self.drawPos()
        self.drawStat()

    def updateCooldown(self):
        '''
        공격 쿨타임을 업데이트 시켜주는 함수
        updateCondition내부에서만 쓰이는 함수임
        '''
        self.attackHitbox = False
        self.coolElapsed = (pygame.time.get_ticks() - self.coolStart) / 1000
        if (self.coolElapsed >= self.atkcool):
            self.coolElapsed = 0
            self.coolStart = 0
        
    def updateCycle(self):
        '''
        컨디션 전환시 스프라이트 업데이트 주기를 계산시켜주는 메서드
        클래스 내부에서만 쓰이는 메서드
        '''
        self.delayElapsed = (pygame.time.get_ticks() - self.delayStart) / 1000
        if (self.delayElapsed >= self.ChangeDelay):
            self.isChangeCondition = False
            self.delayElapsed = 0
            if (self.Condition == GETATTACK):
                self.isGetattack = False
        
    def updateCondition(self):
        '''
        오브젝트의 컨디션을 업데이트 시켜주는 함수
        불값을 기반으로 업데이트 시켜줌
        '''
        if (self.isWalk is True):
            self.Condition = WALK
        elif (self.isAttack is True):
            self.Condition = ATTACK
        elif (self.isGetattack is True):
            self.Condition = GETATTACK
        elif (self.isDead is True):
            self.Condition = DEAD
        elif (self.isWalk is False and self.isAttack is False and
              self.isGetattack is False and self.isDead is False):
            self.Condition = STATIC
            
        if (self.Condition != ATTACK):
            self.updateCooldown()
        
    def updatePos(self):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        '''
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos

        if (self.isOnGround is False):
            self.y_pos += self.airSpace
            if (self.y_pos <= MAP_GROUND - 80):
                self.airspace = 0
                self.gravity += 1
            self.y_pos += self.gravity
        if (self.y_pos >= MAP_GROUND):
            self.y_pos = MAP_GROUND
            self.isOnGround = True
            self.gravity = 0
        if (self.hitbox.left <= MAP_LIMIT_LEFT):
            self.x_pos = MAP_LIMIT_LEFT
        if (self.hitbox.right >= MAP_LIMIT_RIGHT):
            self.x_pos = MAP_LIMIT_RIGHT - self.hitbox.width
            
        if (self.isWalk is True and self.isAttack is False):
            if (self.direction == LEFT):
                self.x_pos += -self.SPEED
            elif (self.direction == RIGHT):
                self.x_pos += self.SPEED

    def updateSprite(self, dt):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        '''
        적의 스프라이트를 업데이트 시켜주는 함수
        스프라이트 업데이트 지연까지 추가함
        '''  
        self.current_time += dt
        
        if (self.Condition == STATIC):
            self.cur = 0
            self.updateCycle()
        if (self.Condition == WALK):
            self.cur = 1
            self.updateCycle()
        if (self.Condition == ATTACK):
            self.cur = 2
            self.updateCycle()
        if (self.Condition == GETATTACK):
            self.cur = 3
            self.updateCycle()
            self.isGetattack = False
        if (self.HP <= 0):
            self.cur = 4
            self.dead()
            self.isChangeCondition = False
        
        if (self.current_time >= self.animation_time or self.isChangeCondition is True):
            self.current_time = 0
            
            self.index += 1
            if (self.index >= len(self.spritelist[self.cur]) or self.isChangeCondition is True):
                self.index = 0
        
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
    def update(self, dt):
        '''
        통합 update 메서드
        가독성을 위해
        '''
        self.updateCondition()
        self.updatePos()
        self.updateSprite(dt)
        
class PlayerObject(LifeObject):
    def __init__(self, x_pos, y_pos=None):
        '''
        플레이어의 기본적인 정보를 설정하는 생성자
        여기에서 스프라이트 및 쿨타임 등을 관리함
        '''
        super().__init__(x_pos, y_pos)
        
        self.direction = RIGHT
        self.getitem = False
        self.itemType = None
        self.projectileimage = BASIC
        self.projectilelist = []
        self.ammunition = 30 # 강화 공격 제한 개수
        self.duration = 20 # 아이템 지속 시간
        self.itemStart = 0 # 아이템 시작 시간
        self.itemElapsed = 0 # 아이템 획득 후 경과시간
        self.atkcool = 0.75
        
        static = [pygame.image.load('char_sprite/char_static.png')]
        dead = [pygame.image.load('char_sprite/char_dead.png')]
        walk = [pygame.image.load('char_sprite/char_walk_' + str(i) + '.png') for i in range(1, 4)]
        attack = [pygame.image.load('char_sprite/char_attack.png')]
        getattack = [pygame.image.load('char_sprite/char_get_attack.png')]

        self.spritelist = [static, walk, attack, getattack ,dead]
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
        self.animation_time = round(100 / len(self.spritelist[self.cur] * 100), 2)
        
    def ResetCondition(self):
        '''
        플레이어의 체력을 제외한 모든 스텟 및 시간을 초기화시키는 메서드
        주로 아이템을 중복으로 먹었을 시에 활성화 됨
        '''
        self.MAXHP = 500
        self.ATK = 50
        self.DEF = 0
        self.SPEED = 10
        self.projectileimage = BASIC
        
        self.duration = 20
        self.itemStart = 0
        self.itemElapsed = 0
        self.atkcool = 0.75
        
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
        if (self.isDead is False and self.isGetattack is False and self.coolElapsed == 0):
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
                if (item.GetImage() == ICE):
                    self.itemType = ICE
                    self.ResetCondition()
                    self.ChangeStat(MAXHP=0, HP=0, ATK=100, DEF=0, SPEED=0, ATTACKSPEED=1)
                    self.projectileimage = REINFORCE
                elif (item.GetImage() == ARMOR):
                    self.itemType = ARMOR
                    self.ResetCondition()
                    self.ChangeStat(MAXHP=0, HP=0, ATK=0, DEF=20, SPEED=0, ATTACKSPEED=1)
                    self.itemStart = pygame.time.get_ticks()
                elif (item.GetImage() == HASTE):
                    self.itemType = HASTE
                    self.ResetCondition()
                    self.ChangeStat(MAXHP=0, HP=0, ATK=0, DEF=0, SPEED=5, ATTACKSPEED=1)
                    self.itemStart = pygame.time.get_ticks()
                elif (item.GetImage() == ATTACKSPEED):
                    self.itemType = ATTACKSPEED
                    self.ResetCondition()
                    self.ChangeStat(MAXHP=0, HP=0, ATK=0, DEF=0, SPEED=0, ATTACKSPEED=1.5)
                    self.itemStart = pygame.time.get_ticks()
                    
    def ItemReset(self):
        '''
        아이템 효과가 다할 시에 관련 변수들을 리셋시켜주는 메서드
        복잡하길래 그냥 하나로 묶어버림
        '''
        self.itemType = None
        self.ResetCondition()
        self.isChangeStat = False
        self.getitem = False
        if (self.itemType == ICE):
            self.projectileimage = BASIC
            self.ammunition = 30
        else:
            self.itemElapsed = 0
            self.itemStart = 0

    def drawStat(self):
        '''
        플레이어의 스텟을 그려주는 메서드
        '''
        Length = 200
        convertConficient = self.MAXHP / 200
        pygame.draw.rect(Screen, VIRGINRED, (10, 10, Length, 30), 2)
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (10, 10, self.HP / convertConficient , 30))
            
        if (self.itemType == ICE):
            Screen.blit(ICEICON, (Length + 20, 15))
            write(SmallFont, ' X ' + str(self.ammunition), BLACK, Length + 40, 15)
        elif (self.itemType == ARMOR):
            Screen.blit(ARMORICON, (Length + 20, 15))
            write(SmallFont, ' : ' + str(self.duration - self.itemElapsed) + ' sec ', BLACK, Length + 40, 15)
        elif (self.itemType == HASTE):
            Screen.blit(HASTEICON, (Length + 20, 15))
            write(SmallFont, ' : ' + str(self.duration - self.itemElapsed) + ' sec ', BLACK, Length + 40, 15)
        elif (self.itemType == ATTACKSPEED):
            Screen.blit(ATTACKSPEEDICON, (Length + 20, 15))
            write(SmallFont, ' : ' + str(self.duration - self.itemElapsed) + ' sec ', BLACK, Length + 40, 15)
            
    def updateCondition(self):
        '''
        플레어어의 컨디션을 업데이트 시켜주는 함수
        불값을 기반으로 업데이트 시켜줌
        
        아이템 관련 및 피격까지 관리함
        '''
        super().updateCondition()
        for enemy in Enemylist:
            if (self.isHitbox is True):
                if (self.checkcollision(enemy) is True and enemy.GetCondition(ATKHITBOX) is True):
                    self.getattack(enemy)
                    
        if (self.getitem is True and self.isChangeStat is True):
            if (self.itemType == ICE):
                if (self.ammunition == 0):
                    self.ItemReset()
            elif (self.itemType == ARMOR):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > 20):
                    self.ItemReset()
            elif (self.itemType == HASTE):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > 20):
                    self.ItemReset()
            elif (self.itemType == ATTACKSPEED):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > 20):
                    self.ItemReset()

class EnemyObject(LifeObject):
    def __init__(self, x_pos, y_pos=None):
        '''
        적의 기본적인 정보를 저장하는 생성자
        '''
        super().__init__(x_pos, y_pos)
        
        self.direction = RIGHT
        self.isDrop = False # 아이템 드랍 관련 불값
        self.isDetect = False # 플레이어 발견 관련 불값
        self.attackRange = 75 # 공격 범위
        self.atkcool = 1
        
        static = [pygame.image.load('enemy_sprite/enemy_static.png')]
        dead = [pygame.image.load('enemy_sprite/enemy_dead.png')]
        walk = [pygame.image.load('enemy_sprite/enemy_walk_' + str(i) + '.png') for i in range(1, 3)]
        attack = [pygame.image.load('enemy_sprite/enemy_attack_' + str(i) + '.png') for i in range(1, 3)]
        getattack = [pygame.image.load('enemy_sprite/enemy_get_attack.png')]

        self.spritelist = [static, walk, attack, getattack, dead]
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
        self.animation_time = round(100 / len(self.spritelist[self.cur] * 100), 2)
        
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
        trueDrop = random.choices(range(1, 6), weights = [1, 1, 1, 1, 1])
        if (trueDrop.pop() >= 4):
            image = random.choice(ItemTypes)
            Itemlist.append(Item(self.x_pos, self.y_pos, image))
        else:
            pass
    
    def detectPlayer(self):
        '''
        플레이어를 감지하는 함수
        '''
        if (self.isDetect is False):
            self.effectStart = pygame.time.get_ticks()
        self.isDetect = True
        self.effectElapsed = (pygame.time.get_ticks() - self.effectStart) / 1000
        if (self.effectElapsed >= self.effectTime):
            self.effectStart = 0
            self.effectElapsed = 0
            
    def AI(self, player):
        '''
        기본적의 적의 AI
        플레이어에 상태에 따라서 업데이트가 된다
        '''
        distance = self.hitbox.centerx - (player.GetPos(X) + player.GetSize(WIDTH) / 2) #플레이어와 적과의 거리를 계산함
        if (abs(distance) <= 400 or self.isGetattack is True):
            self.detectPlayer()
            
        if (self.isDetect is True):
            if (distance > 0):
                self.leftwalk()
            else:
                self.rightwalk()

        if (abs(distance) <= self.attackRange):
            if (player.GetCondition(HITBOX) is True):
                self.attack()
                if (self.coolElapsed != 0 and self.checkcollision(player) is True):
                    self.static()

        for projectile in player.GetProjectiles():
            if (len(player.GetProjectiles()) != 0):
                if (self.isHitbox is True):
                    if (self.checkcollision(projectile) is True):
                        self.index = 0
                        self.getattack(player)
                        player.GetProjectiles().remove(projectile)
                        
        if (player.GetCondition(DEAD) is True):
            self.static()

        if (self.isDead is True and self.isDrop is False):
            self.dropItem()
            self.isDrop = True
            
        return distance
    
    def drawEffect(self):
        if (self.isDetect is True):
            if (self.effectElapsed != 0):
                Screen.blit(DETECTICON, (self.x_pos - 30, self.hitbox.top - 30))

    def drawStat(self):
        Length = 125
        convertConficient = self.MAXHP / Length
        pygame.draw.rect(Screen, VIRGINRED, (self.hitbox.centerx - Length / 2,
                                             self.hitbox.bottom + 18, Length, 12), 3)
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (self.hitbox.centerx - Length / 2,
                                           self.hitbox.bottom + 19, self.HP / convertConficient, 9))
            
    def updateSprite(self, dt):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        '''
        적의 스프라이트를 업데이트 시켜주는 함수
        스프라이트 업데이트 지연까지 추가함
        '''
        super().updateSprite(dt)
        if (self.direction == LEFT):
            self.hitbox = self.cursprite.get_rect(bottomright=(self.x_pos + 70, self.y_pos)) #방향전환시 좌표오류를 잡아줌
        else:
            self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
            
    def update(self, dt, player):
        '''
        적의 업데이트 메서드
        첫번째 변수는 스프라이트 업데이트 주기 설정, 두번째 변수는 AI가 작동될 목표
        '''
        self.AI(player)
        self.updateCondition()
        self.updatePos()
        self.updateSprite(dt)

class BossObject(EnemyObject):
    def __init__(self, x_pos, y_pos=None):
        super().__init__(x_pos, y_pos)
        self.attackRange = 70
        
        static = [pygame.image.load('enemy_sprite/enemy_static.png')]
        dead = [pygame.image.load('enemy_sprite/enemy_dead.png')]
        walk = [pygame.image.load('enemy_sprite/enemy_walk_' + str(i) + '.png') for i in range(1, 3)]
        attack = [pygame.image.load('enemy_sprite/enemy_attack_' + str(i) + '.png') for i in range(1, 3)]
        getattack = [pygame.image.load('enemy_sprite/enemy_get_attack.png')]

        self.spritelist = [static, walk, attack, getattack, dead]
        self.cursprite = self.spritelist[self.cur][self.index]
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


def rungame(stage):
    pygame.init()
    
    Stage = stage
    Stage.SetStage()

    while True:
        dt = Clock.tick(60) / 1000 # 스프라이트 업데이트 주기 함수
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    Stage.player.leftwalk()
                elif (event.key == pygame.K_RIGHT):
                    Stage.player.rightwalk()
                elif (event.key == pygame.K_UP):
                    Stage.player.jump()
                elif (event.key == pygame.K_x):
                    Stage.player.attack()
                elif (event.key == pygame.K_z): #아이템 획득 키
                    Stage.player.getItem()
                elif (event.key == pygame.K_g):
                    pass
                elif (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            elif (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT or
                    event.key == pygame.K_RIGHT or
                    event.key == pygame.K_x):
                    if (Stage.player.GetCondition(DEAD) is False):
                        Stage.player.static()
                    else:
                        Stage.player.dead()

        Stage.DrawStage()
        Stage.player.draw()
        Stage.player.update(1)
        if (len(Stage.player.GetProjectiles()) != 0):
            for projectile in Stage.player.GetProjectiles():
                projectile.move()
                projectile.draw()
                
            for projectile in Stage.player.GetProjectiles():
                if (projectile.GetPos(X) <= MAP_LIMIT_LEFT or
                    projectile.GetPos(X) + projectile.GetSize(WIDTH) >= MAP_LIMIT_RIGHT):
                    Stage.player.GetProjectiles().remove(projectile)
            
        for enemy in Enemylist:
            if (len(Enemylist) != 0):
                enemy.draw()
                enemy.update(dt * 15, Stage.player)
                
        for item in Itemlist:
            if (len(Itemlist) != 0):
                item.draw()
        
        if (Stage.player.GetCondition(DEAD) is True):
            return False

        write(SmallFont, str(Enemylist[0].effectStart) + '   ' + str(len(Enemylist)), BLACK, 400, 20)
        pygame.display.update()
        Clock.tick(FPS)
    
def main():
    global Clock, Screen, BigFont, SmallFont
    pygame.init()
    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((x_size, y_size))
    BigFont = pygame.font.SysFont('notosanscjkkrblack', 70)
    SmallFont = pygame.font.SysFont('notosanscjkkrblack', 40)
    
    pygame.display.set_caption("Adventure")
    
    stage = GameStage(1)
    
    stage.OpeningScreen()
    stage.GameGuide()
    while True:
        rungame(stage)
        stage.GameoverScreen()
    
if (__name__ == '__main__'):
    main()