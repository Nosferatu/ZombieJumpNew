import os
import pygame
from pygame.locals import *

def load_sliced_sprites(w, h, filename):
    images = []
    master_image = pygame.image.load(filename).convert_alpha()

    #master_image.set_colorkey((255,0,255))
    
    master_width, master_height = master_image.get_size()
    for i in xrange(int(master_width/w)):
        images.append(master_image.subsurface((i*w,0,w,h)))

        return images

class BombWithAnimation(pygame.sprite.Sprite):
    def __init__(self, initial_position, fps):
        pygame.sprite.Sprite.__init__(self)
        self.act_frame = 0
        self.frames = load_sliced_sprites(20,20,"explosed-sprite.png")# create the images for the animation
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.fps = fps
        self.change_time = 1.0/self.fps
        self.time = 0


    def update(self, time_passed):
        self.time += time_passed
        if self.time >= self.change_time:
            self.act_frame = (self.act_frame + 1) % len(self.frames)
            self.image = self.frames[self.act_frame]
            self.time = 0

