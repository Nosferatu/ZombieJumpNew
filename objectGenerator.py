import pygame 
import os
from pygame.locals import *
from random import randint
from player import *
from zombies import *
from specials import *

    
    
def spawnRandomZombie(x):
    type = randint (0,100)
    if type <= 50: #60%-Chance, dass normaler Zombie spawned
        zombie = NormalZombie((x,370),0.01)
    elif type <= 80: #40% Chance, dass fetter Zombie spawned
        zombie = FatZombie((x,390),0.01)
    elif type <= 93: # Chance, dass fetter Zombie spawned
        zombie = Charger((x,380),0.01)
    elif type <= 100:
        zombie = Spitter((x,370),0.01)
    return zombie
    
def spawnNewCrate(cratetype):
    sgy = randint(250,400)
    sgx = randint(800,3000)
    crate = Crate((sgx,sgy),0.02,cratetype)
    return crate

def spawnNewCafe():
    sgy = randint(250,400)
    sgx = randint(1000,3000)
    cafe = Cafe((sgx,sgy),0.002)
    return cafe

def spawnNewHeart(lifes):
    sgx = 750 - 50*lifes
    heart = Heart((sgx,20),0.005)
    return heart
