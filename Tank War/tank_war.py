import pygame,sys,os,random
from pygame import *


winWidth  = 1000               #屏幕宽
winHeight = 600                #屏幕高
TankModel1= 1                  #坦克型号1
TankModel2= 2                  #坦克型号2
clockTick = 60                 #帧数
White =    (255,255,255)       #白色
Black =    (  0,  0,  0)       #黑色
Gold  =    (205,127, 32)       #金色
Red   =    (255,  0,  0)       #红色
Green =    (199,237,204)       #绿色
Blue  =    (  0, 78,152)       #蓝色 
path1 = "pictures\\bullet.png " #子弹型号1
path2 = "pictures\\bullet2.png" #子弹型号2

class Tankbuild :
    '''坦克类创建'''
    def __init__(self,chose,key=[],image="",power=10,blood=100) :

        self.chose=chose    #选择车型与操作系统
        
        self.tankxchose  =[200,winWidth/2+200]
        self.tankx       =self.tankxchose[chose-1]
        self.tanky       =200
        self.tankspeed   =5
        self.key         =key                               #操作按钮
        self.imageall    =pygame.image.load(image)          #装载图片
        self.tankright   =self.imageall
        self.tankleft    =pygame.transform.flip(self.tankright,True,False)
        self.tankimage   =[self.tankleft,self.tankright]

        self.tankstatus  =0
        
        self.moveleft  =False
        self.moveright =False
        self.moveup    =False
        self.movedown  =False

        self.fire      =[]
        self.firemax   =4
        self.attackable=True
        self.blood     =blood               #血量
        self.fullblood =blood
        self.power     =power                #力量
        self.death     =False

    def updatetank(self) :
        '''坦克update'''
        #坦克的移动
        if self.moveleft :
            self.tankx-=self.tankspeed
            self.moveleft =False
        elif self.moveright :
            self.tankx+=self.tankspeed
            self.moveright=False
        elif self.moveup :
            self.tanky-=self.tankspeed
            self.moveup   =False
        elif self.movedown :
            self.tanky+=self.tankspeed
            self.movedown =False

        #坦克的操作，通过wsad按键操作坦克1，ikjl操作坦克2
        get_press = pygame.key.get_pressed()
        #上下左右
        if get_press[self.key[0]]:
            self.moveup = True
        elif get_press[self.key[1]]:
            self.movedown = True
        elif get_press[self.key[2]]:
            self.moveleft = True
        elif get_press[self.key[3]]:
            self.moveright = True
        # if self.chose==1 :
        #     get_press=pygame.key.get_pressed()
        #     if get_press[K_w] :
        #         self.moveup   =True
        #     elif get_press[K_s] :
        #         self.movedown =True
        #     elif get_press[K_a] :
        #         self.moveleft =True
        #     elif get_press[K_d] :
        #         self.moveright=True
        #
        # elif self.chose==2 :
        #     get_press=pygame.key.get_pressed()
        #     if get_press[K_i] :
        #         self.moveup   =True
        #     elif get_press[K_k] :
        #         self.movedown =True
        #     elif get_press[K_j] :
        #         self.moveleft =True
        #     elif get_press[K_l] :
        #         self.moveright=True

        #坦克的左右反转
        if self.moveleft :
            self.tankstatus=0
        elif self.moveright :
            self.tankstatus=1


class bullet :
    '''创建子弹'''
    def __init__(self,bulx,buly,direction,path) :
        
        self.bulx     =bulx
        self.buly     =buly
        self.speed    =8
        self.direction=direction

        self.image=pygame.image.load(path)
        self.bulRect=pygame.Rect(self.bulx,self.buly,
                      self.image.get_width(),
                      self.image.get_height())

    def updatebullet(self) :
        '''子弹的移动与更新'''
        if   self.direction==0 :
            self.bulx-=self.speed
        elif self.direction==1 :
            self.bulx+=self.speed


class DenfendBuf(pygame.sprite.Sprite) :
    '''防护罩buff'''
    def __init__(self) :
        super().__init__()
        self.def_pic=pygame.image.load("pictures/defendbuf.png")
        self.def_spc=pygame.image.load("pictures/defend.png   ")

    def add_buff(self,target,pos,time_left) :
        if time_left>0 :
            bloodgroove(pos,Blue,time_left,target.fullblood)
            Screen.blit(self.def_spc,(target.tankx-9,target.tanky-12))
            target.attackable=False
            if target.blood<=100 :
                target.blood+=0.035
        if time_left==0 :
            target.attackable=True
            BuffList.remove(self)
            

class Add_Fire(pygame.sprite.Sprite) :
    '''加子弹'''
    def __init__(self) :
        super().__init__()
        self.def_pic=pygame.image.load("pictures/add_fire.png")

    def add_buff(self,target,pos,n) :
        global time_left
        if time_left>0 :
            target.firemax+=1
            time_left=0
        if time_left==0 :
            BuffList.remove(self)

class Add_Speed(pygame.sprite.Sprite) :
    '''加速'''
    def __init__(self) :
        super().__init__()
        self.def_pic=pygame.image.load("pictures/add_speed.png")
        
    def add_buff(self,target,pos,n) :
        global time_left
        if time_left>0 :
            target.tankspeed+=1
            time_left=0
        if time_left==0 :
            BuffList.remove(self)

class Bullet_lot(pygame.sprite.Sprite) :
    '''无限子弹'''
    def __init__(self) :
        super().__init__()
        self.def_pic=pygame.image.load("pictures/bullet_lot.png")

    def add_buff(self,target,pos,n) :
        global time_left
        before=target.firemax
        if time_left>0 :
            target.firemax=100
            
        if time_left==0 :
            target.firemax=before
            BuffList.remove(self)
            
def bul_restrict(num1,num2) :
    '''限制子弹数量'''
    if len(Tank .fire)>num1 :
        del Tank .fire[-1]
    if len(Tank2.fire)>num2 :
        del Tank2.fire[-1]


def bloodgroove(pos,color,num,full) :
    '''绘制血条'''
    pygame.draw.rect(Screen,Black,[pos[0],pos[1],22,full+2],1)
    pygame.draw.rect(Screen,color,[pos[0]+1,pos[1]+1,20,num],0)


def terminate() :
    '''退出游戏'''
    pygame.quit()
    sys.exit()

    
def createmap() :
    '''创建地图'''
    global scoregreen,scorered,time_left,buffx,buffy,buffchoseone
    
    #显示坦克方块
    tank1Rect=pygame.Rect(Tank.tankx,Tank.tanky,
                          Tank.tankright.get_width(),
                          Tank.tankright.get_height())
    tank2Rect=pygame.Rect(Tank2.tankx,Tank2.tanky,
                          Tank2.tankright.get_width(),
                          Tank2.tankright.get_height())
    
    '''显示buff，并通过撞击确定获得buff的目标，并给予时间限制，一定时间后，buff
    效果消失'''
    time_left-=0.5
    for buff in BuffList :
        Screen.blit(buff.def_pic,(buffx,buffy))
        buffRect=pygame.Rect(buffx,buffy,
                             buff.def_pic.get_width (),
                             buff.def_pic.get_height())
        if   tank1Rect.colliderect(buffRect) :
            time_left=100
            buffx=-1000
            buffchoseone=0
        elif tank2Rect.colliderect(buffRect) :
            time_left=100
            buffx=-1000
            buffchoseone=1

        buff.add_buff([Tank,Tank2,Tankbuild(1,[K_w,K_s,K_a,K_d],"pictures/tank1.png")][buffchoseone],(40,200),time_left)
        
    #显示分数
    scoreFont=pygame.font.Font('freesansbold.ttf',80)
    sGreen   =scoreFont.render(str(scoregreen),True,Green)
    sRed     =scoreFont.render(str(scorered),  True,Red  )
    Screen.blit(sGreen,(winWidth/2-100,40))
    Screen.blit(sRed  ,(winWidth/2+50,40))
    
    #显示坦克与坦克状态更新
    Tank.updatetank()
    Tank2.updatetank()  
    Screen.blit(Tank .tankimage[Tank .tankstatus],(Tank .tankx,Tank .tanky))
    Screen.blit(Tank2.tankimage[Tank2.tankstatus],(Tank2.tankx,Tank2.tanky))
    
    '''循环遍历update子弹的状态，若子弹飞出屏幕，则从弹夹中删去子弹
    如果子弹击中敌方目标，子弹消失，敌方扣血'''
    bul_restrict(Tank.firemax,Tank2.firemax)
    for item in Tank.fire :
        Screen.blit(item.image,(item.bulx,item.buly))
        item.updatebullet()
        bulRect=pygame.Rect(item.bulx,item.buly,
                            item.image.get_width(),
                            item.image.get_height())
        if not (item.bulx>-50 and item.bulx<winWidth) :         
            Tank.fire.remove(item)
        if bulRect.colliderect(tank2Rect) :
            Tank.fire.remove(item)
            if Tank2.attackable==True :
                Tank2.blood-=random.randint(0.8*Tank.power,1.2*Tank.power)

    for item in Tank2.fire : 
        Screen.blit(item.image,(item.bulx,item.buly))
        item.updatebullet()
        bulRect2=pygame.Rect(item.bulx,item.buly,
                            item.image.get_width(),
                            item.image.get_height())
        if not (item.bulx>-50 and item.bulx<winWidth) :
            Tank2.fire.remove(item)
        if bulRect2.colliderect(tank1Rect) :
            Tank2.fire.remove(item)
            if Tank.attackable==True :
                Tank.blood-=random.randint(0.8*Tank2.power,1.2*Tank2.power)


    '''绘制血条'''
    bloodgroove([         40,40],Green,Tank.blood ,Tank.fullblood)
    bloodgroove([winWidth-60,40],Red  ,Tank2.blood,Tank2.fullblood)

  
def showOver(color) :
    '''绘制游戏结束画面'''
    gameOverFont=pygame.font.Font('freesansbold.ttf',150)
    gameSurf=gameOverFont.render('Game',True,color)
    overSurf=gameOverFont.render('Over',True,color)
    gameRect=gameSurf.get_rect()
    overRect=overSurf.get_rect()
    gameRect.midtop=(winWidth/2,10)
    overRect.midtop=(winHeight/2,gameRect.height+10+25)

    Screen.blit(gameSurf,gameRect)
    Screen.blit(overSurf,overRect)

    pygame.display.update()
    pygame.time.wait(1000)



def CreateBuff() :
    '''添加buff'''
    BuffList.append(random.choice([Bullet_lot(),Add_Speed(),DenfendBuf()]))
    


if __name__=='__main__' :
    '''正文'''
    #参数配置
    scoregreen=0
    scorered  =0
    #运行与窗口
    pygame.init()
    Screen=pygame.display.set_mode((winWidth,winHeight))
    displaySpeed=pygame.time.Clock()
    pygame.display.set_caption('Tank War')


    while True :

        #参数初始化
        #攻击高
        Tank =Tankbuild(1,[K_w,K_s,K_a,K_d],"pictures/tank1.png",power=15)
        #血厚
        Tank2=Tankbuild(2,[K_UP,K_DOWN,K_LEFT,K_RIGHT],"pictures/tank2.png",blood=150)
        Buff_Time=USEREVENT
        pygame.time.set_timer(Buff_Time,15*1000)
        time_left=0
        BuffList=[]
        buffx=0
        buffy=0
        buffchoseone=2
        
        while True :
            '''游戏循环'''
            Screen.fill(White)       
            displaySpeed.tick(clockTick)
            
            #事件处理
            for event in pygame.event.get() :
                if   event.type==QUIT :
                    terminate()
                elif event.type==KEYDOWN :
                    if event.key==K_r :
                        Tank.fire.append(bullet(Tank.tankx,Tank.tanky,Tank.tankstatus,path1))  
                    if event.key==K_o :
                        Tank2.fire.append(bullet(Tank2.tankx,Tank2.tanky,Tank2.tankstatus,path2))         
                elif event.type==Buff_Time :
                    CreateBuff()
                    buffx=random.randint(200,800)
                    buffy=random.randint(100,550)

            #图像显示
            createmap()
            if Tank.blood<=0 :
                showOver(Red)
                scorered+=1
                break
            elif Tank2.blood<=0 :
                showOver(Green)
                scoregreen+=1
                break
            pygame.display.update()


    pygame.quit()

    
