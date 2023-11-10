import os, pygame,sys,random
from pygame.locals import *
 
import math
vect = pygame.Vector2
pos3 = 0
pos4 = 0
saohua=[pygame.image.load("dia1.png"),
        pygame.image.load("dia2.png"),
        pygame.image.load("dia3.png"),
        pygame.image.load("dia4.png")]
 
class Chimp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image = pygame.image.load('dog.png')
        # colorkey = self.image.get_at((0, 1))
        # self.image.set_colorkey(colorkey, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = 200, 100
        self.angle = 0
        self.x_speed = 3
        self.y_speed = 3
        self.speed = 4
        self.rotate = False
 
    def update(self):
        if not self.rotate:
            self.original = self.image
            self.rotate = True
        if self.rotate:
            center = self.rect.center
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, -self.angle )
            self.rect = self.image.get_rect(center=center)
        angle = self.angle * math.pi / 180
        self.x_speed = self.speed * math.cos(angle)
        self.y_speed = self.speed * math.sin(angle)
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
 
    def punched(self, pos1, pos2):
        pos0 = vect(0, 0)
        arch = pos2 - pos1
        angle = pos0.angle_to(arch)
        self.angle = angle
 
class Me(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image = pygame.image.load('me.png')
        # colorkey = self.image.get_at((0, 1))
        # self.image.set_colorkey(colorkey, RLEACCEL)
        self.rect = self.image.get_rect()
 
    def update(self):
        if pos4<0 :
            self.rect.y=0
        elif pos4>470 :
            self.rect.y=470
        if pos3<0 :
            self.rect.x=0
        elif pos3>430 :
            self.rect.x=430
        if pos4>0 and pos4<470 and pos3>0 and pos3<430 :
            self.rect.x = pos3
            self.rect.y = pos4
 
def main():
    global pos3,pos4
    pygame.init()
    screen = pygame.display.set_mode((468, 500))
    pygame.display.set_caption('miserable')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    time=0
    now=0
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("don't let the single dog catch you", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        background.blit(text, textpos)
 
    screen.blit(background, (0, 0))
    clock = pygame.time.Clock()
    chimp = Chimp()
    me = Me()
    allsprites = pygame.sprite.Group()
    allsprites.add(chimp)
    allsprites.add(me)
 
    while True:
        clock.tick(60)
        time+=1
        text = font.render("you have survived for "+str(time//60)+' second', 1, (10, 10, 10))
        textpos = [40,30]
        if time%600==0 :
            chimp.speed+=1    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                cur_pos = pygame.mouse.get_pos()
                pos1 = vect(chimp.rect.centerx, chimp.rect.centery)
                pos2 = vect(cur_pos[0], cur_pos[1])
                pos3,pos4=event.pos
                chimp.punched(pos1, pos2)

            else:
                pass            
        allsprites.update()
        screen.blit(background, (0, 0))
        
        if chimp.rect.colliderect(me.rect) :
            stoptext1= font.render("Thanks God", 1, (255, 0, 0))
            stoptext2 = font.render("You Become the SINGLE DOG", 1, (255, 0, 0))
            stoptext3= font.render("After "+str(time//60)+" seconds,",1,(255,0,0))
            screen.blit(stoptext1,[250,180])
            screen.blit(stoptext2,[50,230])
            screen.blit(stoptext3,[40,180])
            chimp.rect.x=0
            chimp.rect.y=0
            time=0
            chimp.speed=4
            pygame.display.update()
            pygame.time.wait(3000)
            
        if time%200==1 :
            dia=random.choice(saohua) 
        if time%500>150 and time%500<350 :
            screen.blit(dia,(chimp.rect.x+20,chimp.rect.y-55))
            
        screen.blit(text, textpos)
        allsprites.draw(screen)
        pygame.display.flip()
 
if __name__ == '__main__':
    main()
