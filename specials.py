import os
import pygame 
from pygame.locals import *
from random import randint


def load_sliced_sprites(w, h, filename):
    images= []
    master_image = pygame.image.load(filename).convert_alpha()
    master_width,master_height = master_image.get_size()
    for i in xrange(int(master_width/w)):                  
        images.append(master_image.subsurface((i*w,0,w,h)))
    
    return images

class FlamethrowerShot(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = load_sliced_sprites(350,100,"flamethrowerFire.png")
        self.image = self.images[0]
        #self.image = pygame.transform.scale(self.image,(20,50))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.mask = pygame.mask.from_surface(self.image)
        self.speed=0

        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.act_frame = 0
        self.shot = False
        self.type = 1
        
    
    def update(self,time_passed):
        self.time += time_passed
        #if self.shot:
            
        if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.images)
                self.image = self.images[self.act_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.time = 0
                

        self.rect.left += self.speed

class Shot(pygame.sprite.Sprite):
    def __init__(self,initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ShotgunSchuss.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image,(20,50))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.mask = pygame.mask.from_surface(self.image)
        self.speed= 20
        self.type = 0


    
    def update(self,time_passed):
        
        self.rect.left += self.speed

class Stone(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.image = pygame.image.load("Stone.png").convert_alpha()
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.speedx = 6
        self.speedy = 0.5 * randint(1,6)
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.counter = 0
        
    def update(self,time_passed):
        self.time += time_passed

 
        self.rect.left -= self.speedx
        self.rect.top += self.speedy 


class Spit(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.imagesCreate = load_sliced_sprites(50,50,"PoisonSpitCreate.png")
        self.imagesSpit = load_sliced_sprites(50,50,"PoisonSpit.png")
        self.image = self.imagesCreate[0]
        #self.image = pygame.transform.scale(self.image,(20,50))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.speed= 0
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.counter = len(self.imagesCreate)
        
    def update(self,time_passed):
        self.time += time_passed
        
        if self.counter == 0:
            self.speed = 5
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesSpit)
                self.image = self.imagesSpit[self.act_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.time = 0
                
        else:   
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesCreate)
                self.image = self.imagesCreate[self.act_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.time = 0
                self.counter -=1
                    
        self.rect.left -= self.speed




class Cafe(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.images = load_sliced_sprites(50,60,"Cafe.png")
        self.image = self.images[0]
        #self.image = pygame.transform.scale(self.image,(20,50))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.speed= 2
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.type = 0
        
    def update(self,time_passed):
        self.time += time_passed
        
        if self.time >= self.change_time:
            self.act_frame = (self.act_frame + 1) % len(self.images)
            self.image = self.images[self.act_frame]
            self.mask = pygame.mask.from_surface(self.image)
            self.time = 0
        
                    
        self.rect.left -= self.speed


class Crate(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps,cratetype,speed):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.cratetype = cratetype
        
        if self.cratetype == 1: #Heart
            self.images = load_sliced_sprites(50,50,"CrateHeart.png")
        
        if self.cratetype == 2: #Shotgun
            self.images = load_sliced_sprites(50,50,"CrateShotgun.png")
        if self.cratetype == 3: #Flamethrower
            self.images = load_sliced_sprites(50,50,"CrateFlamethrower.png")
        if self.cratetype == 4: # Chainsaw
            self.images = load_sliced_sprites(50,50,"CrateChainsaw.png")
        if self.cratetype == 5: #Jump
            self.images = load_sliced_sprites(50,50,"CrateJump.png")            
        if self.cratetype == 6: #WaffeWeg
            self.images = load_sliced_sprites(50,50,"CrateWaffeWeg.png")
        if self.cratetype == 7: #Zombieplus
            self.images = load_sliced_sprites(50,50,"CrateZombiePlus.png")
        if self.cratetype == 8: #Airstrike
            self.images = load_sliced_sprites(50,50,"CrateBomb.png")
            
        self.image = self.images[0]
        #self.image = pygame.transform.scale(self.image,(20,50))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.speed= speed
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.hit = False
        self.type = 1


    def update(self,time_passed):
        self.time += time_passed
        if self.hit and self.act_frame < 9:
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.images)
                self.image = self.images[self.act_frame]
                    
                self.mask = pygame.mask.from_surface(self.image)
                self.time = 0
        
        elif self.act_frame ==9:
            self.image = self.images[9]
            
        else:
            self.image = self.images[0]
                    
        self.rect.left -= self.speed



class HealthTank(pygame.sprite.Sprite):
    def __init__(self,initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.images = load_sliced_sprites(300,40,"HealthTank.png")
        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image,(250,20))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position


        
    def update(self,tank):

        if tank.health == 7.0:
            self.image = self.images[0]
        if tank.health <= 6.5:
            self.image = self.images[1]
        if tank.health <= 6.0:
            self.image = self.images[2]
        if tank.health <= 5.5:
            self.image = self.images[3]
        if tank.health == 5.0:
            self.image = self.images[4]
        if tank.health <= 4.5:
            self.image = self.images[5]
        if tank.health <= 4.0:
            self.image = self.images[6]
        if tank.health <= 3.5:
            self.image = self.images[7]
        if tank.health <= 3.0:
            self.image = self.images[8]
        if tank.health <= 2.5:
            self.image = self.images[9]
        if tank.health <= 2.0:
            self.image = self.images[10]
        if tank.health <= 1.5:
            self.image = self.images[11]
        if tank.health <= 1.0:
            self.image = self.images[12]
        if tank.health <= 0.5:
            self.image = self.images[13]

        
        
        
class Powerbar(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.images = load_sliced_sprites(300,40,"Power.png")
        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image,(250,20))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.counter = 20
        self.empty = False
        
    def update(self,time_passed):
        self.time += time_passed
        
        if self.counter > 0:
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.images)
                self.image = self.images[self.act_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.image = pygame.transform.scale(self.image,(250,20))
                self.time = 0
                self.counter -=1
        else:
            self.image = self.images[19]
            self.empty = True   
            
class Heart(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.images = load_sliced_sprites(50,50,"Herz.png")
        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps

        
    def update(self,time_passed):
        self.time += time_passed
        

        if self.time >= self.change_time:
            self.act_frame = (self.act_frame + 1) % len(self.images)
            self.image = self.images[self.act_frame]
            self.mask = pygame.mask.from_surface(self.image)
            self.image = pygame.transform.scale(self.image,(40,40))
            self.time = 0



class Bloodsplat(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.images = load_sliced_sprites(200,200,"Bloodsplat.png")
        self.image = self.images[0]
        #self.image = pygame.transform.scale(self.image,(40,40))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.counter = 4
        
    def update(self,time_passed):
        self.time += time_passed
        
        if self.counter >0:
            
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.images)
                self.image = self.images[self.act_frame]
                self.mask = pygame.mask.from_surface(self.image)
                #self.image = pygame.transform.scale(self.image,(40,40))
                self.time = 0
                self.counter -=1
                
                
                
class Airstrike(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps,imagesExplosion):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        
        self.imagesBomb = pygame.image.load("Bomb.png").convert_alpha()
        self.imagesExplosion = imagesExplosion
        self.image = self.imagesBomb
        #self.image = pygame.transform.scale(self.image,(20,50))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.speed= 2
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps

        self.counter = len(self.imagesExplosion) -1
        self.drop = 8
        self.type = 2
        self.change = False
        
    def update(self,time_passed):
        self.time += time_passed
        
        
        
        if self.rect.top >= 300 or self.drop ==0:
            if self.drop > 0:
                self.rect.left -= 250
            self.rect.top = 140
            self.drop = 0
            if self.counter == 0:
                self.image = self.imagesExplosion[21]
        
        
            elif self.time >= self.change_time:
                
                self.act_frame = (self.act_frame + 1) % len(self.imagesExplosion)
                self.image = self.imagesExplosion[self.act_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.image = pygame.transform.scale(self.image,(704,400))
                self.time = 0
                self.counter -= 1
            
        
                    
        self.rect.left -= self.speed
        self.rect.top += self.drop
            
