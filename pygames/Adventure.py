import pygame
import sys
import random

pygame.init() # pygame 초기화

'''
맵 관련 변수
'''
MAP_GROUND = 465
MAP_HEIGHT = 0
MAP_LIMIT_LEFT = 0
MAP_LIMIT_RIGHT = 800
XMARGIN = 200
YMARGIN = 0

CAMERAXMARGIN = 250
CAMERAYMARGIN = 200

JUMPDISTANCE = 80
AIRSPACE = -10
GRAVITY = 10
DURATION = 20
AMMUNITION = 30

'''
오브젝트 관련 변수
'''
PLAYERATKCOOL = 1
ENEMYATKCOOL = 1

SEALATTACKRANGE = 75
SNOWMANATTACKDISTANCE = 200
SNOWBALLRANGE = 300
PLYAERRANGE = 300
POLARBEARATTACKRANGE = 0

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
HPRECOVERY = 'items/hprecovery.png'
MAXHPUP = 'items/hpmaxup.png'
COIN = 'items/coin.png'

BASIC = 'char_sprite/bubble.png'
REINFORCE = 'char_sprite/ice.png'

SNOWBALL = 'enemy_sprite/SnowMan_sprite/snowball.png'

ICEICON = pygame.image.load(ICE)
ARMORICON = pygame.image.load(ARMOR)
HASTEICON = pygame.image.load(HASTE)
ATTACKSPEEDICON = pygame.image.load(ATTACKSPEED)
HPRECOVERYICON = pygame.image.load(HPRECOVERY)
MAXHPUPICON = pygame.image.load(MAXHPUP)
COINICON = pygame.image.load(COIN)

DETECTICON = pygame.image.load('effect_icon/detectIcon.png')

'''
오브젝트 관련 리스트 및 변수 -> 이 리스트들을 GameStage 클래스 내부에 조만간 편입시켜야 할듯.
'''
Enemylist = [] # 화면에 그릴 적 리스트
ItemTypes = [ICE, ARMOR, HASTE, ATTACKSPEED, HPRECOVERY, MAXHPUP] # 아이템 타입, 주로 스프라이트 파일로 통해 아이템 획득을 구분할 예정
Itemlist = [] # 아이템을 담는 리스트
ProjectileList = []

'''
기본적인 스텟 함수
'''
PlayerStat = [750, 750, 1000, 0, 10]
EnemyStatdic = {'Seal': [2500, 2500, 80, 20, 4.5],
                'SnowMan': [2000, 2000, 120, 0, 3],
                'PolarBear': [4500, 4500, 180, 60, 3]}

'''
적 타입 및 이름을 나타내는 변수
'''
NORMAL = 'Normal'
BOSS = 'Boss'

SEAL = 'Seal'
SNOWMAN = 'SnowMan'
POLARBEAR = 'PolarBear'

'''
아이템 획득 시 스텟 변환 리스트
'''
ICEStat = [0, 0, 100, 0, 0, 1]
ARMORStat = [0, 0, 0, 20, 0, 1]
HASTEStat = [0, 0, 0, 0, 5, 1]
ATTACKSPEEDStat = [0, 0, 0, 0, 0, 1.5]
MAXHPUPStat = [250, 0, 0, 0, 0, 1]

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

map_x_size = 2400
map_y_size = 1000

# make enemylist!!!
stage_1_map = pygame.image.load('map_images/stage_1_map.png')
stage_2_map = pygame.image.load('map_images/stage_2_map.png')
stage_1_scale = pygame.transform.scale(stage_1_map, (map_x_size, map_y_size))
stage_2_scale = pygame.transform.scale(stage_2_map, (map_x_size, map_y_size))

class GameStage(object):
    '''
    해당 클래스는 게임 스테이지를 구현시켜주는 클래스로, 여기에서 스테이지 진행, 게임오버 화면, 클리어 화면, 오프닝, 카메라 뷰 등을 모두 다룸
    '''
    def __init__(self, stage, score):
        '''
        스테이지의 기본적인 시스템
        '''
        self.stage = stage # 스테이지 설정
        self.totalScore = score
        self.curScore = 0
        self.mapImages = [stage_1_scale, stage_2_scale] # 스테이지 맵 이미지
        
        self.PLAYER = None # 스테이지 내에 그려질 플레이어
        self.ClearStage = False # 스테이지가 클리어 됬는지 아닌지 판별하는 불값
        self.GameOver = False
        self.XCameraMoveable = True # 카메라가 이동가능한 상태인지 설정시켜주는 불값
        self.isXCameraMove = False # 지금 카메라가 작동하고 있는지 판별시켜주는 불값
        self.forceXMove = False # 모든 적이 죽었르 경우 발동되는 불값
        self.isYCameraMove = False
        self.CameraDirection = LEFT # 카메라 방향
        self.Deadboollist = [] # 적 전체의 사망 판정을 관리하는 리스트
        self.Deadbooldic = {NORMAL: list(),
                            BOSS: list()} #점수 차등 부여를 위한 딕셔너리 타입, 추후에 활용할 예정
        self.curDeadbool = [] # 현재 카메라가 비추는 영역에서의 적의 사망 판정으 관리하는 리스트
        self.CameraPos = [0, 0] # 카메라 위치
        self.CameraSlack = pygame.Rect(CAMERAXMARGIN, CAMERAYMARGIN, x_size - CAMERAXMARGIN * 2, MAP_GROUND - CAMERAYMARGIN)
        
        self.clearCounts = 0
    def GetPlayer(self):
        '''
        플레이어를 리턴시켜주는 메서드
        주로 플레이어의 정보를 필요로 하는 루프나 클래스에서 쓰임
        '''
        return self.PLAYER
    
    def GetCameraView(self, pos):
        '''
        카메라뷰 위치를 리턴시켜주는 메서드
        '''
        try:
            if (pos == 'x'):
                return self.CameraPos[0]
            elif (pos == 'y'):
                return self.CameraPos[1]
            else:
                raise ValueError
        except ValueError:
            print('Not Pos!!!')
            
    def OpeningScreen(self):
        '''
        게임 오프닝을 보여주는 메서드
        '''
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
        '''
        게임 가이드를 보여주는 메서드
        '''
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
            Screen.blit(HPRECOVERYICON, (XMARGIN, 360))
            write(SmallFont, ': RECOVERY HP', BLACK, XMARGIN + 35, 360)
            Screen.blit(MAXHPUPICON, (XMARGIN, 390))
            write(SmallFont, ': IMPROVE MAXHP AND RECOVERY HP', BLACK, XMARGIN + 35, 390)
            
            write(SmallFont, 'PRESS S!', BLACK, XMARGIN, 500)
            pygame.draw.rect(Screen, BLACK, (0, 0, x_size, y_size), 5)
            pygame.display.update()
        
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_s):
                        return False
    
    def ClearScreen(self):
        '''
        스테이지 클리어시 나오는 화면
        '''
        self.clearCounts += 1
        write(BigFont, 'Stage Clear!!!', BLACK, XMARGIN, 200)
        if (len(self.mapImages) == self.clearCounts):
            write(BigFont, 'Total Sclre: ' + str(self.totalScore + self.curScore), BLACK, XMARGIN, 270)
        pygame.display.update()
        pygame.time.wait(1000)
            
    def GameoverScreen(self):
        '''
        플레이어의 HP가 전부 소진되고 적이 전원 사망하지 않을 시 나오는 화면
        '''
        write(BigFont, 'GameOver!!!', BLUE, XMARGIN, 200)
        write(BigFont, 'Try Again?', BLUE, XMARGIN, 280)
        write(BigFont, 'Y / N', BLUE, XMARGIN, 360)
        pygame.display.update()
        pygame.time.wait(2000)
    
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_y):
                    self.ResetStage()
                    self.SetStage()
                elif (event.key == pygame.K_n):
                    pygame.quit()
                    sys.exit()
                elif (event.key is None):
                    pygame.quit()
                    sys.exit()
                    
    def SetEnemy(self, EnemyList):
        for enemy in EnemyList:
            if (enemy.GetName() == SEAL):
                enemy.SetStat(*EnemyStatdic[SEAL])
            elif (enemy.GetName() == SNOWMAN):
                enemy.SetStat(*EnemyStatdic[SNOWMAN])
            self.Deadboollist.append(enemy.GetCondition(DEAD))
              
    def SetStage(self):
        '''
        스테이지를 설정시켜주는 메서드
        주로 main()함수에서 쓰임
        '''
        if (self.stage == 1):
            self.PLAYER = PlayerObject(100)
            self.PLAYER.SetStat(*PlayerStat)
            
            Itemlist.append(ItemObject(100, MAP_GROUND, COIN))
            Enemylist.append(EnemyObject(SNOWMAN, NORMAL, 800))
            Enemylist.append(EnemyObject(SEAL, NORMAL, 500))
            Enemylist.append(EnemyObject(SEAL, NORMAL, 1500))
            Enemylist.append(EnemyObject(SNOWMAN, NORMAL, 1800))
            self.SetEnemy(Enemylist)
                
        elif (self.stage == 2):
            self.PLAYER = PlayerObject(100)
            self.PLAYER.SetStat(*PlayerStat)
            
            Enemylist.append(EnemyObject(SEAL, NORMAL, 800))
            self.SetEnemy(Enemylist)
                
    def ResetStage(self):
        '''
        스테이지 재시도시 또는 스테이지 클리어 시 호출되는 메서드
        '''
        Enemylist.clear()
        Itemlist.clear()
        self.Deadboollist.clear()
        self.PLAYER.GetProjectiles().clear()
        ProjectileList.clear()
        for enemy in Enemylist:
            self.Deadboollist.append(enemy.GetCondition(DEAD))
        self.ClearStage = False
        self.GameOver = False
    
    def DrawStage(self):
        '''
        스테이지를 그려주는 메서드
        '''
        Screen.blit(self.mapImages[self.stage - 1], (0, y_size - map_y_size), (self.CameraPos[0], self.CameraPos[1], map_x_size, map_y_size))
        write(SmallFont, 'Scroe: ' + str(self.totalScore + self.curScore), BLACK, 650, 25)
        
    def UpdateEnemy(self):
        '''
        적들이
        '''
        self.Deadboollist.clear()
        self.curDeadbool.clear()
        for enemy in Enemylist:
            self.Deadboollist.append(enemy.GetCondition(DEAD))
            if (enemy.GetPos(X) >= 0 and enemy.GetPos(X) + enemy.GetSize(WIDTH) <= x_size):
                self.curDeadbool.append(enemy.GetCondition(DEAD))
                
        if (all(self.Deadboollist)):
            self.ClearStage = True
            
    def UpdateScore(self):
        '''
        스코어를 업데이트시켜주는 메서드
        스코어는 스테이지가 클리어 될수록 누적이 됨
        '''
        coinCoefficient = 50
        itemCoefficient = 100
        killCoefficient = 400
        bosskillCoefficient = 800
        stageclearCofficient = 1500
        
        coinscore = self.PLAYER.coincounts * coinCoefficient
        itemscore = self.PLAYER.itemcounts * itemCoefficient
        killscore = self.Deadboollist.count(True) * killCoefficient
        stageclearscore = self.clearCounts * stageclearCofficient
        
        self.curScore = coinscore + itemscore + killscore + stageclearscore
        
    def GetScore(self):
        return self.curScore
        
    def CameraXMovement(self, dx=0):
        '''
        카메라 이동을 관리하는 메서드
        '''
        self.CameraPos[0] += dx

    def CameraYMovement(self, dy=0):
        self.CameraPos[1] += dy
                
    def UpdateCamera(self):
        '''
        카메라의 위치를 업데이트시켜주는 메서드
        '''
        PlayerCenterX = self.PLAYER.GetPos(X) + self.PLAYER.GetSize(WIDTH) / 2
        PlayerCenterY = self.PLAYER.GetPos(Y) + self.PLAYER.GetSize(HEIGHT) / 2
        self.CameraDirection = self.PLAYER.GetCondition(DIRECTION)
            
        if (self.CameraPos[0] + x_size >= map_x_size):
            self.CameraPos[0] = map_x_size - x_size
            self.XCameraMoveable = False
        elif (PlayerCenterX <= CAMERAXMARGIN and self.CameraPos[0] <= 0):
            self.CameraPos[0] = 0
            self.XCameraMoveable = False
            
        for enemy in Enemylist:
            if (enemy.GetPos(X) <= x_size - enemy.GetSize(WIDTH) and enemy.GetPos(X) >= 0):
                if (not all(self.curDeadbool)):
                    self.isXCameraMove = False
                    self.XCameraMoveable = False
                elif (all(self.curDeadbool) and (self.CameraPos[0] > 0 and self.CameraPos[0] < map_x_size - x_size)):
                    self.XCameraMoveable = True
                if (PlayerCenterX > CAMERAXMARGIN and self.CameraDirection == RIGHT and self.XCameraMoveable):
                    self.forceXMove = True
                else:
                    self.forceXMove = False
        if (self.PLAYER.GetCondition(WALK)):
            self.isXCameraMove = True
        else:
            self.isXCameraMove = False
        
        if (not self.XCameraMoveable):
            if (self.CameraPos[0] >= map_x_size - x_size):
                if (PlayerCenterX < CAMERAXMARGIN):
                    self.XCameraMoveable = True
            elif (self.CameraPos[0] <= 0):
                if (PlayerCenterX > CAMERAXMARGIN):
                    self.XCameraMoveable = True
                    
        if (self.PLAYER.GetCondition(ONGROUND)):
            self.CameraPos[1] = 0
            
    def removeProjectile(self):
        '''
        투사체가 맵 밖으로 나갈 때 지우는 메서드
        '''
        PlayerProjectile = self.PLAYER.GetProjectiles()
        
        for projectile in PlayerProjectile:
            if (projectile.GetPos(X) <= MAP_LIMIT_LEFT or projectile.GetPos(X) + projectile.GetSize(WIDTH) >= MAP_LIMIT_RIGHT):
                PlayerProjectile.remove(projectile)
                
        for projectile in ProjectileList:
            if ((projectile.GetPos(X) <= MAP_LIMIT_LEFT or projectile.GetPos(X) + projectile.GetSize(WIDTH) >= MAP_LIMIT_RIGHT) or
                abs(projectile.GetPos(X) - projectile.GetInitPos(X)) > SNOWBALLRANGE):
                ProjectileList.remove(projectile)
                    
    def UpdateStage(self):
        '''
        통합 업데이트 메서드
        '''
        self.UpdateCamera()
        self.UpdateEnemy()
        self.removeProjectile()
        self.UpdateScore()
        
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
        self.init_x_pos = x_pos
        self.init_y_pos = y_pos
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
                return self.x_pos
            elif (pos == 'y'):
                return self.y_pos
            else:
                raise ValueError
        except ValueError:
            print('Not Pos!!!!')
            
    def GetInitPos(self, pos):
        try:
            if (pos == 'x'):
                return self.init_x_pos
            elif (pos == 'y'):
                return self.init_y_pos
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
        Screen.blit(self.image, (self.x_pos, self.y_pos))

    def checkcollision(self, enemy):
        '''
        충돌 판정
        '''
        if (pygame.Rect.colliderect(self.hitbox, enemy.hitbox)):
            return True
        else:
            return False
        
    def updatePos(self, Stage):
        '''
        투사체가 자동으로 움직이도록 하는 메서드
        업데이트까지 겸함
        '''
        PlayerOnGround = Stage.GetPlayer().GetCondition(ONGROUND)
        AirSpace = Stage.GetPlayer().airSpace
        Gravity = Stage.GetPlayer().gravity
        
        if (self.direction == LEFT):
            self.x_pos += -self.SPEED
        else:
            self.x_pos += self.SPEED
            
        if (not PlayerOnGround):
            if (AirSpace != 0):
                self.y_pos -= AirSpace
            else:
                self.y_pos -= Gravity
                
        self.hitbox.x = self.x_pos
        self.hitbox.y = self.y_pos

class ItemObject(object):
    def __init__(self, x_pos, y_pos, image):
        '''
        아이템의 전체적인 정보를 저장하는 생성자
        '''
        self.x_pos = x_pos # 지속적으로 업데이트 되는 위치를 저장하는 변수
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
        Screen.blit(self.icon, (self.x_pos, self.hitbox.y))

    def checkcollision(self, Player):
        '''
        충돌판정 함수
        '''
        if (pygame.Rect.colliderect(self.hitbox, Player.hitbox)):
            return True
        else:
            return False
        
    def updatePos(self, Stage):
        PlayerCenterX = Stage.GetPlayer().GetPos(X) + Stage.GetPlayer().GetSize(WIDTH) / 2
        PlayerDirection = Stage.GetPlayer().GetCondition(DIRECTION)
        
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos
        
        if ((Stage.XCameraMoveable and Stage.isXCameraMove) or Stage.forceXMove):
            if (PlayerCenterX <= CAMERAXMARGIN and PlayerDirection == LEFT):
                self.x_pos += Stage.GetPlayer().GetStat(SPEED)
            elif (PlayerCenterX >= CAMERAXMARGIN and PlayerDirection == RIGHT):
                self.x_pos += -Stage.GetPlayer().GetStat(SPEED)
                
        if (not Stage.GetPlayer().GetCondition(ONGROUND)):
            if (Stage.GetPlayer().airSpace != 0):
                self.y_pos -= Stage.GetPlayer().airSpace
            else:
                self.y_pos -= Stage.GetPlayer().gravity
        else:
            self.y_pos = MAP_GROUND
    
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
        self.projectilelist = []
        
        self.gravity = 0 # 중력 계수
        self.airSpace = AIRSPACE # 점프 계수
        
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
        
    def GetProjectiles(self):
        return self.projectilelist
    
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
        self.drawPos()
        self.drawStat()
        self.drawEffect()

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
        if (self.HP <= 0):
            self.dead()
            
        if (self.isWalk):
            self.Condition = WALK
        elif (self.isAttack):
            self.Condition = ATTACK
        elif (self.isGetattack):
            self.Condition = GETATTACK
        elif (self.isDead):
            self.Condition = DEAD
        elif (self.isWalk is False and self.isAttack is False and
              self.isGetattack is False and self.isDead is False):
            self.Condition = STATIC
            
        if (self.Condition != ATTACK):
            self.updateCooldown()
        
    def updatePos(self, Stage):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        '''
        pass
    
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
        if (self.Condition == DEAD):
            self.cur = 4
            self.isChangeCondition = False
        
        if (self.current_time >= self.animation_time or self.isChangeCondition):
            self.current_time = 0
            
            self.index += 1
            if (self.index >= len(self.spritelist[self.cur]) or self.isChangeCondition):
                self.index = 0
        
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
    def update(self, dt, Stage):
        '''
        통합 update 메서드
        가독성을 위해
        '''
        self.updateCondition()
        self.updatePos(Stage)
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
        self.itemcounts = 0 #누적으로 획득한 아이템 개수
        self.coincounts = 0 #코인 개수
        self.itemType = None
        self.projectileimage = BASIC
        self.ammunition = 30 # 강화 공격 제한 개수
        self.duration = 20 # 아이템 지속 시간
        self.itemStart = 0 # 아이템 시작 시간
        self.itemElapsed = 0 # 아이템 획득 후 경과시간
        self.atkcool = PLAYERATKCOOL
        
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
        self.MAXHP = PlayerStat[0]
        self.ATK = PlayerStat[2]
        self.DEF = PlayerStat[3]
        self.SPEED = PlayerStat[4]
        self.projectileimage = BASIC
        
        self.duration = DURATION
        self.itemStart = 0
        self.itemElapsed = 0
        self.atkcool = PLAYERATKCOOL
        self.ammunition = AMMUNITION
        
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
                
    def attack(self):
        '''
        플레이어의 공격 상태를 설정하는 메서드
        플레이어는 원거리 공격을 주로 하므로 공격판정마다 projectilelist 내에 방향을 추가
        (overriding)
        '''
        super().attack()
        if (self.itemType == ICE and self.coolElapsed == 0):
            self.ammunition -= 1
        if (self.isDead is False and self.isGetattack is False and self.coolElapsed == 0):
            if (self.direction == LEFT):
                self.projectilelist.append(Projectile(self.projectileimage, self.hitbox.left, self.hitbox.y, self.ATK, LEFT))
            else:
                self.projectilelist.append(Projectile(self.projectileimage, self.hitbox.right, self.hitbox.y, self.ATK, RIGHT))
                 
    def getItem(self):
        '''
        아이템을 얻게 해주는 메서드 아이템 종류에 따라 효과가 다르게 발동되도록 변경
        '''
        for item in Itemlist:
            if (self.checkcollision(item)):
                Itemlist.remove(item)
                self.getitem = True
                if (item.GetImage() != COIN):
                    self.isChangeStat = True
                    self.itemcounts += 1
                    if (item.GetImage() == ICE):
                        self.itemType = ICE
                        self.ResetCondition()
                        self.ChangeStat(*ICEStat)
                        self.projectileimage = REINFORCE
                        self.getitem = False
                    elif (item.GetImage() == ARMOR):
                        self.itemType = ARMOR
                        self.ResetCondition()
                        self.ChangeStat(*ARMORStat)
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == HASTE):
                        self.itemType = HASTE
                        self.ResetCondition()
                        self.ChangeStat(*HASTEStat)
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == ATTACKSPEED):
                        self.itemType = ATTACKSPEED
                        self.ResetCondition()
                        self.ChangeStat(*ATTACKSPEEDStat)
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == MAXHPUP):
                        self.itemType = MAXHPUP
                        self.ResetCondition()
                        self.ChangeStat(*MAXHPUPStat)
                        self.HP = self.MAXHP
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == HPRECOVERY):
                        self.HP = self.MAXHP
                        self.getitem = False
                else:
                    self.coincounts += 1
                    self.getitem = False
                
    def ItemReset(self):
        '''
        아이템 효과가 다할 시에 관련 변수들을 리셋시켜주는 메서드
        복잡하길래 그냥 하나로 묶어버림
        '''
        self.itemType = None
        self.ResetCondition()
        self.isChangeStat = False
        if (self.itemType == ICE):
            self.projectileimage = BASIC
            self.ammunition = AMMUNITION
        else:
            self.itemElapsed = 0
            self.itemStart = 0

    def drawStat(self):
        '''
        플레이어의 스텟을 그려주는 메서드
        '''
        Length = 200
        convertCoefficient = Length / self.MAXHP
        pygame.draw.rect(Screen, VIRGINRED, (10, 10, Length, 30), 2)
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (10, 10, self.HP * convertCoefficient , 30))
            
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
            if (self.isHitbox):
                if (self.checkcollision(enemy) and enemy.GetCondition(ATKHITBOX)):
                    self.getattack(enemy)
                    
        for projectile in ProjectileList:
            if (len(ProjectileList) != 0):
                if (self.isHitbox):
                    if (self.checkcollision(projectile)):
                        self.getattack(enemy)
                        ProjectileList.remove(projectile)
                    
        if (self.isChangeStat):
            if (self.itemType == ICE):
                if (self.ammunition == 0):
                    self.ItemReset()
            elif (self.itemType == ARMOR):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == HASTE):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == ATTACKSPEED):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == MAXHP):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
                    if (self.HP > self.MAXHP):
                        self.HP = self.MAXHP
                        
    def updatePos(self, Stage):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        플레이어는 카메라의 위치에 따라 위치가 보정되도록 변경됨
        '''
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos

        if (Stage.GetCameraView(X) <= map_x_size - x_size or Stage.GetCameraView(X) >= 0):
            if (self.hitbox.centerx > CAMERAXMARGIN and self.direction == RIGHT):
                if (Stage.XCameraMoveable):
                    Stage.CameraXMovement(self.SPEED)
                    self.x_pos -= self.SPEED
            elif (self.hitbox.centerx <= CAMERAXMARGIN and Stage.GetCameraView(X) > 0 and self.direction == LEFT):
                if (Stage.XCameraMoveable):
                    Stage.CameraXMovement(-self.SPEED)
                    self.x_pos += self.SPEED
                
        if (Stage.XCameraMoveable is False):
            if (self.hitbox.left <= MAP_LIMIT_LEFT):
                self.x_pos = MAP_LIMIT_LEFT
            if (self.hitbox.right >= MAP_LIMIT_RIGHT):
                self.x_pos = MAP_LIMIT_RIGHT - self.hitbox.width
                
        if (self.isOnGround is False):
            self.y_pos += self.airSpace
            Stage.CameraYMovement(self.airSpace)
            if (self.y_pos <= MAP_GROUND - JUMPDISTANCE):
                self.airSpace = 0
                self.gravity = GRAVITY
            self.y_pos += self.gravity
            Stage.CameraYMovement(self.gravity)
        if (self.y_pos >= MAP_GROUND):
            self.y_pos = MAP_GROUND
            self.isOnGround = True
            self.gravity = 0
            self.airSpace = AIRSPACE
                
        if (self.isWalk and self.isAttack is False):
            if (self.direction == LEFT):
                self.x_pos += -self.SPEED
            elif (self.direction == RIGHT):
                self.x_pos += self.SPEED
        

class EnemyObject(LifeObject):
    def __init__(self, Name, Type, x_pos, y_pos=None):
        '''
        적의 기본적인 정보를 저장하는 생성자
        '''
        super().__init__(x_pos, y_pos)
        
        self.direction = RIGHT
        self.Name = Name
        self.Type = Type
        self.isDrop = False # 아이템 드랍 관련 불값
        self.isDetect = False # 플레이어 발견 관련 불값
        self.atkcool = ENEMYATKCOOL
        
        if (self.Name == SEAL):
            self.attackRange = 75 # 공격 범위
            static = [pygame.image.load('enemy_sprite/Seal_sprite/seal_static.png')]
            dead = [pygame.image.load('enemy_sprite/Seal_sprite/seal_dead.png')]
            walk = [pygame.image.load('enemy_sprite/Seal_sprite/seal_walk_' + str(i) + '.png') for i in range(1, 3)]
            attack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_attack_' + str(i) + '.png') for i in range(1, 3)]
            getattack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_get_attack.png')]
            
        elif (self.Name == SNOWMAN):
            self.projectileimage = SNOWBALL
            self.attackDistance = 200
            static = [pygame.image.load('enemy_sprite/SnowMan_sprite/snowman_static.png')]
            dead = [pygame.image.load('enemy_sprite/SnowMan_sprite/snowman_dead.png')]
            walk = [pygame.image.load('enemy_sprite/SnowMan_sprite/snowman_walk_' + str(i) + '.png') for i in range(1, 3)]
            attack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_attack_' + str(i) + '.png') for i in range(1, 3)]
            getattack = [pygame.image.load('enemy_sprite/SnowMan_sprite/snowman_get_attack.png')]
            
        elif (self.Name == POLARBEAR):
            static = [pygame.image.load('enemy_sprite/Seal_sprite/snowman_static.png')]
            dead = [pygame.image.load('enemy_sprite/Seal_sprite/seal_dead.png')]
            walk = [pygame.image.load('enemy_sprite/Seal_sprite/seal_walk_' + str(i) + '.png') for i in range(1, 3)]
            attack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_attack_' + str(i) + '.png') for i in range(1, 3)]
            getattack = [pygame.image.load('enemy_sprite/Seal_sprite0/seal_get_attack.png')]

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
            
    def GetName(self):
        return self.Name
    
    def GetType(self):
        return self.Type
            
    def attack(self):
        super().attack()
        if (self.Name == SNOWMAN):
            if (self.isDead is False and self.isGetattack is False and self.coolElapsed == 0):
                if (self.direction == LEFT):
                    ProjectileList.append(Projectile(self.projectileimage, self.hitbox.left, MAP_GROUND - 50, self.ATK, LEFT))
                else:
                    ProjectileList.append(Projectile(self.projectileimage, self.hitbox.right, MAP_GROUND - 50, self.ATK, RIGHT))
            

    def dropItem(self):
        '''
        아이템을 드롭시키는 함수, 나중에 확률에 따라 드랍시킬 생각
        '''
        trueDrop = random.choices(range(1, len(ItemTypes)), weights = [1, 1, 1, 1, 1])
        if (trueDrop.pop() >= 4):
            image = random.choice(ItemTypes)
            Itemlist.append(ItemObject(self.x_pos, self.y_pos, image))
        
        if (self.Type == NORMAL):
            coindrops = random.randrange(1,3)
            for i in range(-coindrops, coindrops):
                Itemlist.append(ItemObject(self.x_pos + i * 20, self.y_pos, COIN))
        elif (self.Type == BOSS):
            coindrops = random.randrange(3,9)
            for i in range(-coindrops, coindrops):
                Itemlist.append(ItemObject(self.x_pos + i * 12, self.y_pos, COIN))
    
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
        if (abs(distance) <= 400 or self.HP != self.MAXHP):
            self.detectPlayer()
            
        if (self.isDetect):
            if (distance > 0):
                self.leftwalk()
            else:
                self.rightwalk()
                
        if (abs(distance) <= self.attackRange):
            if (player.GetCondition(HITBOX)):
                if (self.coolElapsed != 0 and self.checkcollision(player)):
                    self.static()
                self.attack()

        for projectile in player.GetProjectiles():
            if (len(player.GetProjectiles()) != 0):
                if (self.isHitbox):
                    if (self.checkcollision(projectile)):
                        self.index = 0
                        self.getattack(player)
                        player.GetProjectiles().remove(projectile)
                        
        if (player.GetCondition(DEAD)):
            self.static()

        if (self.isDead and self.isDrop is False):
            self.dropItem()
            self.isDrop = True
    
    def AI_2(self, player):
        distance = self.hitbox.centerx - (player.GetPos(X) + player.GetSize(WIDTH) / 2) #플레이어와 적과의 거리를 계산함
        if (abs(distance) <= 400 or self.HP != self.MAXHP):
            self.detectPlayer()
            
        if (self.isDetect):
            if (distance > 0):
                self.leftwalk()
            else:
                self.rightwalk()
                
        if (abs(distance) <= self.attackDistance):
            if (player.GetCondition(HITBOX)):
                if (self.coolElapsed != 0):
                    self.static()
                self.attack()

        for projectile in player.GetProjectiles():
            if (len(player.GetProjectiles()) != 0):
                if (self.isHitbox):
                    if (self.checkcollision(projectile)):
                        self.index = 0
                        self.getattack(player)
                        player.GetProjectiles().remove(projectile)
                        
        if (player.GetCondition(DEAD)):
            self.static()

        if (self.isDead and self.isDrop is False):
            self.dropItem()
            self.isDrop = True
            
        return distance
    
    def drawEffect(self):
        if (self.isDetect):
            if (self.effectElapsed != 0):
                Screen.blit(DETECTICON, (self.x_pos - 30, self.hitbox.top - 30))

    def drawStat(self):
        if (self.Type == NORMAL):
            Length = 125
            convertCoefficient = Length / self.MAXHP
            pygame.draw.rect(Screen, VIRGINRED, (self.hitbox.centerx - Length / 2,
                                             self.hitbox.bottom + 18, Length, 12), 3)
            if (self.HP >= 0):
                pygame.draw.rect(Screen, RED, (self.hitbox.centerx - Length / 2,
                                               self.hitbox.bottom + 19, self.HP * convertCoefficient, 9))
        elif (self.Type == BOSS):
            Length = 300
            convertCoefficient = Length / self.MAXHP
            
    def updatePos(self, Stage):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        '''
        PlayerDirection = Stage.GetPlayer().GetCondition(DIRECTION)
        PlayerSpeed = Stage.GetPlayer().GetStat(SPEED)
        
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos

        if (self.isWalk and self.isAttack is False):
            if (self.direction == LEFT):
                self.x_pos += -self.SPEED
            elif (self.direction == RIGHT):
                self.x_pos += self.SPEED
        
        if (Stage.XCameraMoveable and (Stage.isXCameraMove or Stage.forceXMove)):
            if (PlayerDirection == LEFT):
                self.x_pos += PlayerSpeed
            elif (PlayerDirection == RIGHT):
                self.x_pos -= PlayerSpeed
        
        elif (not Stage.isXCameraMove and (self.x_pos <= x_size and self.x_pos >= 0)):
            if (self.hitbox.left <= MAP_LIMIT_LEFT):
                self.x_pos = MAP_LIMIT_LEFT #좌표 보정인데.... 오류라서
            if (self.hitbox.right >= MAP_LIMIT_RIGHT):
                self.x_pos = MAP_LIMIT_RIGHT - self.hitbox.width
                    
        if (not Stage.GetPlayer().GetCondition(ONGROUND)):
            if (Stage.GetPlayer().airSpace != 0):
                self.y_pos -= Stage.GetPlayer().airSpace
            else:
                self.y_pos -= Stage.GetPlayer().gravity
        else:
            self.y_pos = MAP_GROUND
            
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
            
    def update(self, dt, Stage):
        '''
        적의 업데이트 메서드
        첫번째 변수는 스프라이트 업데이트 주기 설정, 두번째 변수는 AI가 작동될 목표
        '''
        if (self.Name == SEAL):
            self.AI(Stage.GetPlayer())
        elif (self.Name == SNOWMAN):
            self.AI_2(Stage.GetPlayer())
        super().update(dt, Stage)

def rungame(Stage):
    while True:
        dt = Clock.tick(60) / 1000 # 스프라이트 업데이트 주기 함수
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    Stage.GetPlayer().leftwalk()
                elif (event.key == pygame.K_RIGHT):
                    Stage.GetPlayer().rightwalk()
                elif (event.key == pygame.K_UP):
                    Stage.GetPlayer().jump()
                elif (event.key == pygame.K_x):
                    Stage.GetPlayer().attack()
                elif (event.key == pygame.K_z): #아이템 획득 키
                    Stage.GetPlayer().getItem()
                elif (event.key == pygame.K_g):
                    pass
                elif (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            elif (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT or
                    event.key == pygame.K_RIGHT or
                    event.key == pygame.K_x):
                    if (Stage.GetPlayer().GetCondition(DEAD) is False):
                        Stage.GetPlayer().static()
                    else:
                        Stage.GetPlayer().dead()
        
        Stage.UpdateStage()
        Stage.DrawStage() #?
        Stage.GetPlayer().update(1, Stage) #?
        Stage.GetPlayer().draw() #? #?
        if (len(Stage.GetPlayer().GetProjectiles()) != 0):
            for projectile in Stage.GetPlayer().GetProjectiles():
                projectile.updatePos(Stage)
                projectile.draw()
                
            for projectile in Stage.GetPlayer().GetProjectiles():
                if (projectile.GetPos(X) <= MAP_LIMIT_LEFT or
                    projectile.GetPos(X) + projectile.GetSize(WIDTH) >= MAP_LIMIT_RIGHT):
                    Stage.GetPlayer().GetProjectiles().remove(projectile)
            
        for enemy in Enemylist:
            if (len(Enemylist) != 0):
                if (len(ProjectileList) != 0):
                    for projectile in ProjectileList:
                        projectile.updatePos(Stage)
                        projectile.draw()
                enemy.update(dt * 15, Stage)
                enemy.draw()
                
        for item in Itemlist:
            if (len(Itemlist) != 0):
                item.updatePos(Stage)
                item.draw()
        
        if (Stage.GetPlayer().GetCondition(DEAD)):
            Stage.GameOver = True
            return False
        
        if (Stage.ClearStage):
            Stage.ClearScreen()
            return False

        write(SmallFont, str(Enemylist[0].delayElapsed) + '   ' + str(Enemylist[0].coolElapsed), BLACK, 350, 20)
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
    
    level = 1
    score = 0
    while True:
        Stage = GameStage(level, score)
        Stage.SetStage()
        if (level == 1):
            Stage.OpeningScreen()
            Stage.GameGuide()
        while True:
            rungame(Stage)
            if (Stage.ClearStage):
                level += 1
                score += Stage.GetScore()
                Stage.ResetStage()
                break
            elif (Stage.GameOver):
                Stage.GameoverScreen()
    
if (__name__ == '__main__'):
    main()