import pygame 
import os
from pygame.locals import *

def load_sliced_sprites(w, h, filename):
    images= []
    master_image = pygame.image.load(filename).convert_alpha()
    master_width,master_height = master_image.get_size()
    for i in xrange(int(master_width/w)):                  
        images.append(master_image.subsurface((i*w,0,w,h)))
    
    return images


class Player(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):

        
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        self.imagesPlayer = load_sliced_sprites(200,224,"CharacterWalk5.png")
        self.imagesShotgun = load_sliced_sprites(200,224,"CharacterWalkShotgun.png")
        self.imagesSchuss = load_sliced_sprites(200,224,"CharacterWalkShotgunSchuss.png")
        self.imagesJump = load_sliced_sprites(200,224,"CharacterJump2.png")
        self.imagesChainsaw = load_sliced_sprites(240,224,"CharacterWalkChainsaw.png")
        self.imagesFlamethrower = load_sliced_sprites(240,224,"CharacterWalkFlamethrower.png")
        self.imagesDie = load_sliced_sprites(300,224,"CharacterDie2.png")
        self.imagesStand = self.imagesPlayer[0]
        self.imagesStandShotgun = self.imagesShotgun[0]
        self.imagesStandFlamethrower = self.imagesFlamethrower[0]
        self.image = self.imagesPlayer[0]
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position
        self.fps = fps
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image,(120,144))
        self.lifes = 1
        self.invincible = False
        
        self.tank = False
        #player attribute
        self.shotgunAmmo = 0
        self.reloadCD = 0
        self.gasAmmo = 0
        self.bombAmmo = 0
        self.kills = 0
        self.distance = 0
        
        self.shotgun = False
        self.flamethrower = False
        
        
        self.time = 0.0
        self.change_time = 1.0/self.fps
        self.jumpHeight = 41
        self.isjump = False
        self.v = self.jumpHeight
        self.m = 0.02
        self.schuss = False
        self.throwFlames = False
        self.doublejump = False
        self.doublejumpDuration = 0.0
        self.chainsawCounter = 0.0
        self.dead = False
        self.dieCounter = 3
        
    def jump(self):
        self.isjump = True
        
        if self.doublejump and self.rect.top<360:
            self.v = self.jumpHeight
            self.doublejump = False
    
    def update(self,time_passed):
        self.time += time_passed
        
        if self.invincible and self.isjump == False:
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesChainsaw)
                self.image = self.imagesChainsaw[self.act_frame]
                self.image = pygame.transform.scale(self.image,(160,144))
                self.mask = pygame.mask.from_surface(self.image)
                self.time = 0

        if self.flamethrower:
            if self.tank and self.isjump == False:
                self.image = self.imagesStandFlamethrower
                self.image = pygame.transform.scale(self.image,(160,144))
                self.mask = pygame.mask.from_surface(self.image)
            elif self.isjump:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesJump)
                    self.image = self.imagesJump[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(120,144))
                    self.mask = pygame.mask.from_surface(self.image)
                    self.time = 0
            else:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesFlamethrower)
                    self.image = self.imagesFlamethrower[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(160,144))
                    self.mask = pygame.mask.from_surface(self.image)
                    self.time = 0
        
        
        
        elif self.shotgun:
            if self.tank and self.isjump == False:
                    self.image = self.imagesStandShotgun
                    self.image = pygame.transform.scale(self.image,(120,144))
                    self.mask = pygame.mask.from_surface(self.image)
            
            elif self.schuss:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesSchuss)
                    self.image = self.imagesSchuss[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(120,144))
                    self.mask = pygame.mask.from_surface(self.image)
                    self.time = 0
                    
            elif self.isjump:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesJump)
                    self.image = self.imagesJump[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(120,144))
                    self.mask = pygame.mask.from_surface(self.image)
                    self.time = 0
                    
            else:
                if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesShotgun)
                    self.image = self.imagesShotgun[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(120,144))
                    self.mask = pygame.mask.from_surface(self.image)
                    self.time = 0
                    self.schuss = False
                    
        elif self.tank and self.isjump == False:
            
            self.image = self.imagesStand
            self.image = pygame.transform.scale(self.image,(120,144))
            self.mask = pygame.mask.from_surface(self.image)
            
        if self.isjump:
            if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesJump)
                    self.image = self.imagesJump[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(120,144))
                    self.mask = pygame.mask.from_surface(self.image)
                    self.time = 0
                    
        if self.dead:
            self.shotgun = False
            self.flamethrower = False
            self.invincible = False
            self.doublejump = False
            self.throwFlames = False
            self.rect.left -=2
            if self.dieCounter <= 0:
                self.image = self.imagesDie[3]
                self.image = pygame.transform.scale(self.image,(220,144))

            elif self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.imagesDie)

                self.image = self.imagesDie[3-self.dieCounter]
                self.image = pygame.transform.scale(self.image,(220,144))
                self.mask = pygame.mask.from_surface(self.image)
                self.time = 0
                self.dieCounter -=1
         
        
            
        elif self.tank == False:
            if self.time >= self.change_time:
                    self.act_frame = (self.act_frame + 1) % len(self.imagesPlayer)
                    self.image = self.imagesPlayer[self.act_frame]
                    self.image = pygame.transform.scale(self.image,(120,144))
                    self.mask = pygame.mask.from_surface(self.image)
                    self.time = 0
                    self.shotgun = False
                    
    
                    
        if self.doublejumpDuration > 0.0:
            self.doublejumpDuration -= 10.0
        else: 
            self.doublejump = False                

        if self.chainsawCounter > 0.0:
            self.chainsawCounter -=10.0
        else:
            self.invincible = False
    

                    
        if self.isjump:
            
            
            
            
            
            if self.v > 0:
                F = ( 0.5 * self.m * (self.v*self.v) )
            else:
                F = -( 0.5 * self.m * (self.v*self.v) )
    
            # Change position
            self.rect.top =  self.rect.top - F
 
            # Change velocity
            self.v = self.v - 1
 
            # If ground is reached, reset variables.
            if  self.rect.top >= 365:
                self.rect.top = 365
                self.isjump = 0
                self.v = self.jumpHeight
                if self.doublejumpDuration > 0.0:
                    self.doublejump = True  