import pygame 
import os
from pygame.locals import *
from random import randint
from player import *
from zombies import *
from specials import *
from objectGenerator import *
from _subprocess import INFINITE
from startAndEnd import *
from __builtin__ import True




class ButtonSound(pygame.sprite.Sprite):

    def __init__(self,initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.imageOn = pygame.image.load("SoundOn.png").convert_alpha()
        
        self.imageOff = pygame.image.load("SoundOff.png").convert_alpha()
        self.image = self.imageOn
        self.imageOn = pygame.transform.scale(self.imageOn,(30,30))
        self.imageOff = pygame.transform.scale(self.imageOff,(30,30))
        self.rect = self.image.get_rect()
        self.rect.topleft=initial_position
        self.clicked = False
        self.change = True
        
        
    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


    def update(self):

        if self.change:
            self.image = self.imageOn
            self.clicked = True
        else:
            self.image = self.imageOff
            self.clicked = False
