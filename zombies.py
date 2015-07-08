import pygame 
import os
from pygame.locals import *
from random import randint
from specials import *


def load_sliced_sprites(w, h, filename):
    images= []
    master_image = pygame.image.load(filename).convert_alpha()
    master_width,master_height = master_image.get_size()
    for i in xrange(int(master_width/w)):                  
        images.append(master_image.subsurface((i*w,0,w,h)))
    
    return images

class NormalZombie(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        self.imagesWalk = load_sliced_sprites(100,100,"NormalZombieWalk.png")
        self.imagesDead = load_sliced_sprites(100,100,"NormalZombieDie.png")
        self.imagesDeadFlame = load_sliced_sprites(100,100,"NormalZombieBurn.png")
        
        self.image = self.imagesWalk[0]
        self.image = pygame.transform.scale(self.image,(140,140))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.fps = fps
        self.speed= 3
        self.show = True #Braucht man, damit man die Zombies in for-Schleife durchlaufen kann
        self.change_time = 1.0/self.fps
        self.time = 0
        self.change = True #Braucht man, damit man die Zombies in for-Schleife durchlaufen kann
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.lengthDead = 7
        self.counter = 0
        self.type = 0
        self.flameDie = False
    
    def update(self,time_passed,spawn):
        self.time += time_passed
            
                
        if self.dead:
            self.speed = 2
            if self.lengthDead <= 0 and self.flameDie == False:
                    
                self.image = self.imagesDead[7]
                self.image = pygame.transform.scale(self.image,(140,140))
            
            elif self.lengthDead <= 0 and self.flameDie:     
                self.image = self.imagesDeadFlame[7]
                self.image = pygame.transform.scale(self.image,(140,140))
                
            elif self.flameDie:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesDeadFlame)
                    self.image = self.imagesDeadFlame[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(140,140))
                    self.time = 0
                    self.lengthDead -= 1
            
            
            else:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesDead)
                    self.image = self.imagesDead[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(140,140))
                    self.time = 0
                    self.lengthDead -= 1
                    
                    
                    #self.dead = False
        else:
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesWalk)
                self.image = self.imagesWalk[self.act_frame]
                self.image = pygame.transform.scale(self.image,(140,140))
                self.time = 0
                self.mask = pygame.mask.from_surface(self.image)
                      
        self.rect.left -= self.speed
class Spitter(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        self.imagesBackwards = load_sliced_sprites(100,100,"PoisonZombieBackwards.png")
        self.imagesStand = load_sliced_sprites(100,100,"PoisonZombieStanding.png")
        self.imagesSpit = load_sliced_sprites(100,100,"PoisonZombieSpit.png")
        self.imagesDead = load_sliced_sprites(100,100,"PoisonZombieDie.png")
        self.imagesDeadFlame = load_sliced_sprites(100,100,"PoisonZombieBurn.png")
        
        self.image = self.imagesStand[0]
        self.image = pygame.transform.scale(self.image,(150,150))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.fps = fps
        self.speed= 2
        self.show = False
        self.change_time = 1.0/self.fps
        self.time = 0
        self.change = True
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.lengthDead = 7
        self.counter = 700
        self.stopTime = randint(520,580)
        self.shoot = False
        self.spitCounter = 200
        self.type = 1
        self.spitEnd = False
        self.flameDie = False
        
    
    def update(self,time_passed,spawn):
        self.time += time_passed
           
            
        if self.shoot:
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesSpit)
                self.image = self.imagesSpit[self.act_frame]
                self.image = pygame.transform.scale(self.image,(150,150))
                self.time = 0
                self.mask = pygame.mask.from_surface(self.image)      
                

        
  
        
        
        if self.counter <= 0 and self.dead == False:
            self.speed = 2
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesStand)
                self.image = self.imagesStand[self.act_frame]
                self.image = pygame.transform.scale(self.image,(150,150))
                self.time = 0
                self.mask = pygame.mask.from_surface(self.image)
        
        elif self.counter <= self.stopTime and self.dead == False:
            self.speed = 0
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesBackwards)
                self.image = self.imagesBackwards[self.act_frame]
                self.image = pygame.transform.scale(self.image,(150,150))
                self.time = 0
                self.mask = pygame.mask.from_surface(self.image)
                
        
        if self.dead:
            
            self.speed = 2
            if self.lengthDead <= 0 and self.flameDie == False:
                    
                self.image = self.imagesDead[7]
                self.image = pygame.transform.scale(self.image,(150,150))
            
            elif self.lengthDead <= 0 and self.flameDie:     
                self.image = self.imagesDeadFlame[7]
                self.image = pygame.transform.scale(self.image,(150,150))
                
            elif self.flameDie:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesDeadFlame)
                    self.image = self.imagesDeadFlame[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(150,150))
                    self.time = 0
                    self.lengthDead -= 1
            
            
            
            else:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesDead)
                    self.image = self.imagesDead[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(150,150))
                    self.time = 0
                    self.lengthDead -= 1
                    
                    
               
        self.counter -= 1        
        self.spitCounter -= 1        
        self.rect.left -= self.speed
        
        
class FatZombie(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        self.imagesShow = load_sliced_sprites(100,100,"FetterZombie3.png")
        self.imagesWalk = load_sliced_sprites(100,100,"FetterZombieWalk2.png")
        self.imagesDead = load_sliced_sprites(150,100,"FetterZombieDie.png")
        self.imagesDeadFlame = load_sliced_sprites(150,100,"FetterZombieDieFlame.png")        
        self.image = self.imagesShow[0]
        self.image = pygame.transform.scale(self.image,(120,120))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.fps = fps
        self.speed= 2
        self.show = False
        self.change_time = 1.0/self.fps
        self.time = 0
        self.change = True
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.lengthDead = 7
        self.counter = 0
        self.type = 2
        self.flameDie = False
    
    def update(self,time_passed,spawn):
        self.time += time_passed
        if self.show:
            self.speed = 3
            if self.change and self.counter < 4:
                        
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesShow)
                    self.image = self.imagesShow[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(120,120))
                    self.time = 0
                    self.counter +=1
                    self.mask = pygame.mask.from_surface(self.image)
                
                    
            if self.dead:
                self.speed =2
                #print self.lengthDead
                if self.lengthDead <= 0 and self.flameDie == False:
                    
                    self.image = self.imagesDead[7]
                    self.image = pygame.transform.scale(self.image,(170,120))
                
                elif self.lengthDead <= 0 and self.flameDie:     
                    self.image = self.imagesDeadFlame[7]
                    self.image = pygame.transform.scale(self.image,(170,120))
                elif self.flameDie:
                    if self.time >= self.change_time:
                        self.act_frame = (self.act_frame + 1) % len(self.imagesDeadFlame)
                        self.image = self.imagesDeadFlame[self.act_frame]
                        self.image = pygame.transform.scale(self.image,(170,120))
                        self.time = 0
                        self.lengthDead -= 1
                  
                    
                    
                else:
                    if self.time >= self.change_time:
                        self.act_frame = (self.act_frame + 1) % len(self.imagesDead)
                        self.image = self.imagesDead[self.act_frame]
                        self.image = pygame.transform.scale(self.image,(170,120))
                        self.time = 0
                        self.lengthDead -= 1
                        
                        
                        #self.dead = False
            else:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesWalk)
                    self.image = self.imagesWalk[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(120,120))
                    self.time = 0
                    self.mask = pygame.mask.from_surface(self.image)
                     
        else: 
            if self.rect.left <= spawn:
                self.show = True        
        self.rect.left -= self.speed
        
        
        
        
class Charger(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        self.imagesStomp = load_sliced_sprites(150,150,"ChargerPose.png")
        self.imagesWalk = load_sliced_sprites(150,150,"ChargerWalkIn.png")
        self.imagesCharge = load_sliced_sprites(150,150,"ChargerCharge.png")
        self.imagesDie = load_sliced_sprites(200,180,"ChargerDie.png")
        self.imagesDeadFlame = load_sliced_sprites(200,180,"ChargerDieFlame.png")
        self.image = self.imagesWalk[0]
        self.image = pygame.transform.scale(self.image,(130,130))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.fps = fps
        self.speed= 2
        self.show = False
        self.change_time = 1.0/self.fps
        self.time = 0
        self.change = True
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.lengthDead = 5
        self.lengthDead2 = 6
        self.counter = len(self.imagesStomp)
        self.type = 3
        self.flameDie = False
    
    def update(self,time_passed,spawn):
        self.time += time_passed
        if self.change and self.dead == False:
            if self.counter == 0:
                if self.time >= self.change_time:
                    self.speed += 1.1
                    self.act_frame = (self.act_frame + 1) % len(self.imagesCharge)
                    self.image = self.imagesCharge[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(130,130))
                    self.time = 0
                    self.mask = pygame.mask.from_surface(self.image)
                
            else:                
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesStomp)
                    self.image = self.imagesStomp[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(130,130))
                    self.time = 0
                    self.mask = pygame.mask.from_surface(self.image)
                    self.counter -= 1
            
                
        if self.dead:
            self.speed =2
                #print self.lengthDead
            if self.lengthDead <= 0:
                    
                self.image = self.imagesDie[5]
                self.image = pygame.transform.scale(self.image,(180,160))
             
            
            elif self.lengthDead2 <= 0 and self.flameDie:     
                    self.image = self.imagesDeadFlame[6]
                    self.image = pygame.transform.scale(self.image,(180,160))
                    
            elif self.flameDie:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesDeadFlame)
                    self.image = self.imagesDeadFlame[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(180,160))
                    self.time = 0
                    self.lengthDead2 -= 1           
                
                
                    
            else:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesDie)
                    self.image = self.imagesDie[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(180,160))
                    self.time = 0
                    self.lengthDead -= 1
        else:
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesWalk)
                self.image = self.imagesWalk[self.act_frame]
                self.image = pygame.transform.scale(self.image,(130,130))
                self.time = 0
                self.mask = pygame.mask.from_surface(self.image)
                 
                
        self.rect.left -= self.speed
        
class Tank(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        self.imagesJumpIn = load_sliced_sprites(200,200,"TankJumpIn.png")
        self.imagesStand = load_sliced_sprites(200,200,"Tank.png")
        self.imagesThrow = load_sliced_sprites(300,300,"TankThrow.png")
        self.imagesDead = load_sliced_sprites(150,100,"FetterZombieDie.png") #ToDo
        self.imagesDeadFlame = load_sliced_sprites(150,100,"FetterZombieDieFlame.png") #ToDo        
        self.image = self.imagesJumpIn[0]
        #self.image = pygame.transform.scale(self.image,(120,120))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.fps = fps
        self.speedx = 3.5
        self.speedy = 2
        self.show = False
        self.change_time = 1.0/self.fps
        self.time = 0
        self.change = True
        self.health = 7
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.lengthDead = 7
        self.lengthThrow = len(self.imagesThrow)
        self.lengthJI = len(self.imagesJumpIn)
        self.throwcounter = 300
        self.throwFinished = False
        self.type = 4
        self.flameDead = False
    
    def update(self,time_passed):
        self.time += time_passed
        

        
        if self.lengthJI > 0:
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesJumpIn)
                self.image = self.imagesJumpIn[self.act_frame]
                #self.image = pygame.transform.scale(self.image,(130,130))
                self.time = 0
                self.mask = pygame.mask.from_surface(self.image)
                self.speedy +=1
                self.lengthJI -= 1
                
            if self.rect.top > 300:
                self.speedy = 0
                self.speedx = 0
                self.rect.top = 300
            
        
        elif self.throwcounter > 0:
            self.rect.top = 300
            self.rect.left = 468
            self.throwcounter -= 1
            self.image = self.imagesStand[0]
            self.mask = pygame.mask.from_surface(self.image)
                
               
        if self.throwcounter == 0:
            self.rect.top = 200
            self.rect.left = 418
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesThrow)
                self.image = self.imagesThrow[self.act_frame]
                #self.image = pygame.transform.scale(self.image,(130,130))
                self.time = 0
                self.mask = pygame.mask.from_surface(self.image)
                self.lengthThrow -= 1
                
                
            if self.throwFinished:
                self.throwFinished = False
                self.throwcounter = 80
                self.lengthThrow = len(self.imagesThrow)
                self.rect.left += 50
            elif self.lengthThrow == 0:
                self.throwFinished = True
               
        self.rect.left -= self.speedx
        self.rect.top += self.speedy        
        