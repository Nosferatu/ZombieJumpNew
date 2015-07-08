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



class GameOverScreen(pygame.sprite.Sprite):
    def __init__(self,initial_position,fps):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = load_sliced_sprites(400,300,"GameOverScreen3.png")
        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image,(800,600))
        self.rect= self.image.get_rect()
        self.rect.topleft=initial_position

        self.time = 0.0
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.act_frame = 0
        self.change = False
        self.counter = len(self.images)-1

    
    def update(self,time_passed):
        self.time += time_passed

        if self.counter == 0:
            self.image = self.images[38]
            self.image = pygame.transform.scale(self.image,(800,600))
        else:
            if self.time >= self.change_time:
                self.act_frame = (self.act_frame + 1) % len(self.images)
                self.image = self.images[self.act_frame]
                self.image = pygame.transform.scale(self.image,(800,600))
                self.time = 0
                self.counter -=1
            
            
            
            


