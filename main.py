import pygame
import os
import sys
from pygame.locals import *
from random import randint
from player import *
from zombies import *
from specials import *
from objectGenerator import *
from _subprocess import INFINITE
from startAndEnd import *
from Button import *



def collision(obj1,obj2):
    offset_x, offset_y = (obj2.rect.left - obj1.rect.left), (obj2.rect.top - obj1.rect.top)
    if (obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None):
        return True
    else:
        return False

def checkEvents(player,shot):
    for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
                
              
            if event.type == KEYDOWN:
                
                if event.key == K_m:                    
                    if buttonSoundOnOff.change:
                        buttonSoundOnOff.change = False
                        pygame.mixer.music.pause()
                        buttonSoundOnOff.clicked = True

    
                    else:
                        buttonSoundOnOff.change = True
                        pygame.mixer.music.unpause()
                        buttonSoundOnOff.clicked = False
            
                if event.key == K_SPACE:
                    player.jump()
            
    
                if event.key == K_s:
                    player.schuss = True
                    if player.reloadCD <= 0 and player.shotgunAmmo > 0 and player.invincible == False and player.isjump == False:
                        player.shotgun = True
                        player.flamethrower = False
                        shotgun_sound.play()
                        schuss=Shot((player.rect.centerx,player.rect.centery-90))
                        
                        shot.add(schuss)
                        player.reloadCD = 1000
                        player.shotgunAmmo -= 1 
                       
                    else:
                        pass
                
                if event.key == K_a:
                        
                    if player.gasAmmo > 0 and player.invincible == False and player.isjump == False:  
                        flamethrower_sound.play()
                        player.flamethrower = True
                        player.shotgun = False
                        flameShot = FlamethrowerShot((player.rect.centerx+40,player.rect.centery-130),0.01)
                        flameShot.shot = True
                        shot.add(flameShot)
                        player.throwFlames = True 
                        
                if event.key == K_d:
                    if player.bombAmmo >= 1:
                        bombExplosion_sound.play()
                        bomb = Airstrike((750,-150),0.01,imagesExplosion)
                        shot.add(bomb)
                        player.bombAmmo -= 1
              
                  
            if event.type == KEYUP:
    
                    
                if event.key == K_s:                
                    player.schuss = False
                
                if event.key == K_a:  
                    flamethrower_sound.stop()
                    player.throwFlames = False
                    for shot1 in shot:
                        if shot1.type == 1:
                            shot.remove(shot1)

               
               
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                
                if buttonSoundOnOff.pressed(mouse) and buttonSoundOnOff.change:
                    buttonSoundOnOff.change = False
                    pygame.mixer.music.pause()
                    buttonSoundOnOff.clicked = True

                else:
                    buttonSoundOnOff.change = True
                    pygame.mixer.music.unpause()
                    buttonSoundOnOff.clicked = False
          
def checkAllCollisions(player,allzombies,powerups,ui,shot,projectiles,a,b,back1,back2,screenWidth):
    for zombie in allzombies:
        if collision(player,zombie) and zombie.dead == False and player.invincible == False:
            
            #time_passed = clock.tick(50) #Bullet Time wenn man stirbt
            player.lifes -= 1
            heartCounter = player.lifes
            for heart in hearts:
                if heartCounter>0:
                    heartCounter -=1
                else:
                    hearts.remove(heart)
            if player.lifes == 0:
                player.dead = True
                player.act_frame = 0
                gameOver(True,player,x,back1,back2,screenWidth) # Game Over
            zombie.act_frame = 0
            zombie.dead = True
            player.kills +=1  
        
        elif collision(player,zombie) and zombie.dead == False and player.invincible:
            randChainsawSound = randint(1,4)
            if randChainsawSound == 1:
                chainsawFlesh1_sound.play()
                chainsaw_sound.stop()
            elif randChainsawSound == 2:
                chainsawFlesh2_sound.play()
                chainsaw_sound.stop()
            elif randChainsawSound == 3:
                chainsawFlesh3_sound.play()
                chainsaw_sound.stop()
            else:
                chainsawFlesh4_sound.play()
                chainsaw_sound.stop()
            zombie.act_frame = 0
            zombie.dead = True
            player.kills +=1  
            
        
        if zombie.rect.left < -150:
            allzombies.remove(zombie)
            
        if zombie.type == 1:
            if zombie.spitCounter == 25 and zombie.counter > 0 and zombie.dead == False:
                spit = Spit((zombie.rect.centerx-40,zombie.rect.centery-70),0.01)
                zombie.shoot = True
                projectiles.add(spit)
            
            elif zombie.spitCounter == 0:
                zombie.shoot = False
                zombie.spitCounter = 300
            
    for shot1 in shot:
        
        for zombie in allzombies:
            
            if collision(shot1,zombie) and zombie.dead == False:  # Kollision zwischen shot1 und Zombie testen
                zombie.act_frame = 0
                zombie.dead = True
                player.kills +=1
                if shot1.type == 0:
                    shot.remove(shot1)     # remove Shot
                if shot1.type >= 1:
                    zombie.flameDie = True    
                       
        
        if shot1.rect.left > 800:
            shot.remove(shot1)
    
    
    for zombie in allzombies:
        for zombieCharge in allzombies:
            if zombieCharge.type == 3 and zombie.type != 3:
                
                if collision(zombieCharge,zombie) and zombie.dead == False:  # Kollision zwischen zwei Zombies testen
                    zombie.act_frame = 0
                    zombie.dead = True
    
    
    for crate in powerups:
        if collision (player,crate) and crate.type == 1 and crate.hit == False:
            crate.hit = True
            
            if crate.cratetype == 1:
                ExtraLifeSpeech_sound.play()
                player.lifes += 1
                heart = spawnNewHeart(player.lifes)
                hearts.add(heart)
            elif crate.cratetype == 2:
                player.shotgun = True # Shotgun Model wenn Shotgun aufgesammelt
                player.shotgunAmmo += 3
                player.flamethrower = False
                shotgunSpeech_sound.play()
            elif crate.cratetype == 3:
                player.flamethrower = True
                player.gasAmmo += 200
                player.shotgun = False
                flamethrowerSpeech_sound.play()
            elif crate.cratetype == 4:
                player.invincible = True
                chainsaw_sound.play()
                chainsawSpeech_sound.play()
    
                player.chainsawCounter = 7000
                
            elif crate.cratetype == 5:
                player.doublejump = True
                player.doublejumpDuration = 10000
                doubleJumpSpeech_sound.play()
            elif crate.cratetype == 6:
                player.shotgun = False
                player.flamethrower = False
                player.gasAmmo = 0
                player.shotgunAmmo = 0
                player.invincible = False
                player.bombAmmo = 0
                player.chainsawCounter = 0
                weaponLossSpeech_sound.play()
    
            elif crate.cratetype == 7:
                ersterZombieX = 900
                i = player.distance / 100
                zombieAttackSpeech_sound.play()
                while i > 0:
                    zombie = spawnRandomZombie(ersterZombieX)
                    allzombies.add(zombie)
                    i -= 1
                    abstandZombie = randint(300,450)
                    ersterZombieX += abstandZombie
                    
            elif crate.cratetype == 8:
                
                player.bombAmmo += 1
                airstrikeSpeech_sound.play()

            
            if screenWidth == 6000:
                crateMax = 8
            else:
                crateMax = 7        
                
            if player.lifes >= 3: # Keine Herzen mehr spawnen
                crateType = randint(2,crateMax)
            else: 
                crateType = randint(1,crateMax)
            crate = spawnNewCrate(crateType)
            
            powerups.add(crate)
        elif crate.rect.left < -100 and crate.type == 1:
            powerups.remove(crate)
            if screenWidth == 6000:
                crateMax = 8
            else:
                crateMax = 7 
            if crate.hit == False: #nur neue Kiste spawnen, wenn sie nicht eingesammelt wurde.
                if player.lifes == 3: # Keine Herzen mehr spawnen
                    crateType = randint(2,crateMax)
                else: 
                    crateType = randint(1,crateMax)
                crate = spawnNewCrate(crateType)
            
                powerups.add(crate)        

        
        if collision (player,crate) and crate.type == 0:        
        
            powerups.remove(crate)
            for powerbar in ui:
                ui.remove(powerbar)
            power = Powerbar((250,20),0.0005)
            ui.add(power)
            cafe = spawnNewCafe()
        
            powerups.add(cafe)
        elif crate.rect.left < -100 and crate.type == 0:
            powerups.remove(crate)
            cafe = spawnNewCafe()
            powerups.add(cafe)  
    
    
    for projectile in projectiles:
        
        if collision (player,projectile):
            projectiles.remove(projectile)
            time_passed = clock.tick(50) #Bullet Time wenn man stirbt
            player.lifes -= 1
            heartCounter = player.lifes
            for heart in hearts:
                if heartCounter>0:
                    heartCounter -=1
                else:
                    hearts.remove(heart)
            if player.lifes == 0:
                player.dead = True
                player.tank = False
                player.act_frame = 0
                gameOver(True,player,x,back1,back2,screenWidth) # Game Over
      
        elif projectile.rect.left < -100:
            projectiles.remove(projectile)
            
                

#Starte neues Spiel
def gameStart(background,screenWidth):
    back1 = pygame.image.load(background).convert_alpha()
    back2 = pygame.image.load(background).convert_alpha()
    
    player = Player((100,365),0.015) 
       
    a = 350
    b = 800
    
    allzombies = pygame.sprite.RenderUpdates()    
    if screenWidth == 6000:
        continueGame(player,0,allzombies,a,b,False,back1,back2,screenWidth)
    else:
        continueGame(player,0,allzombies,a,b,True,back1,back2,screenWidth)
  
#Setze gestartetes Spiel endlos fort  
def continueGame(player,x,allzombies,a,b,spawnBoss,back1,back2,screenWidth):
    
    power = Powerbar((250,20),0.0005)
    
    ui = pygame.sprite.RenderUpdates()
    ui.add(power)
  
    bossSpawn = randint(400,1000)
    
    nextZombie = randint(a,b) #Abstand Zombie und naechster Zombie
    
    projectiles = pygame.sprite.RenderUpdates()
    
    cafe = spawnNewCafe()
    crateType = randint(1,7)
    crate = spawnNewCrate(crateType)    
    
    powerups = pygame.sprite.RenderUpdates()
    powerups.add(crate,cafe)
    
    i = 0
    while i<player.lifes:
        i += 1
        heart = spawnNewHeart(i)
        hearts.add(heart)
    
    zombieCounter = 0
    zombieAttack = False
  
    while True:
        checkEvents(player,shot)          
 
                
        screen.blit(back1, (x,0))
        screen.blit(back2,(x+screenWidth,0))
        x = x - 2
        if x <= -screenWidth:
            x = 0
        ui.draw(screen)
        screen.blit(player.image,player.rect)
        screen.blit(buttonSoundOnOff.image,buttonSoundOnOff.rect)
        projectiles.draw(screen)    
        allzombies.draw(screen)
        hearts.draw(screen)
        powerups.draw(screen)
        shot.draw(screen)

        if player.shotgunAmmo > 0:
            screen.blit(shotgun,(10,20))
            label = font.render("Ammo: "+str(player.shotgunAmmo),True,(255,255,255))
            screen.blit(label,(60,25))
        
        if player.doublejumpDuration > 0.0:
            screen.blit(doubleJump,(10,180))
            labelJump = font.render("Jump Time: "+str(player.doublejumpDuration*0.001),True,(255,255,255))
            screen.blit(labelJump,(60,180))
            
        if player.chainsawCounter > 0.0:
            screen.blit(chainsaw,(10,60))
            labelChainsaw = font.render("Invincible: "+str(player.chainsawCounter*0.001),True,(255,255,255))
            screen.blit(labelChainsaw,(60,60))    
            
            
        if player.gasAmmo> 0:
            screen.blit(flamethrower,(5,80))
            labelFlamethrower= font.render("Flamethrower: "+str(player.gasAmmo),True,(255,255,255))
            screen.blit(labelFlamethrower,(60,100))  
        
        if player.bombAmmo >0:
            screen.blit(airstrike,(10,140))
            labelAirstrike= font.render("Airstrike: "+str(player.bombAmmo),True,(255,255,255))
            screen.blit(labelAirstrike,(60,140)) 
    
    

    
        time_passed = clock.tick(100)
        player.reloadCD -= 30
    
        player.distance +=0.06
    
        labelKill = font.render("Kills: "+str(player.kills),True,(255,255,255))
        screen.blit(labelKill,(250,40))
        
        labelDistance = font.render("Distance: "+str(player.distance),True,(255,255,255))
        screen.blit(labelDistance,(390,40))
        

        if player.distance >= bossSpawn and spawnBoss:
            bossfight(x,allzombies,player,a,b,back1,back2,screenWidth)
    
        if power.empty:
            player.dead = True
            player.act_frame = 0
            gameOver(True,player,x,back1,back2,screenWidth) # Game Over

    
        if player.throwFlames:
            if player.gasAmmo>0:
                player.gasAmmo -=1
        
            elif player.gasAmmo <= 0:
                player.throwFlames = False
                for shot1 in shot:
                    if shot1.type == 1:
                        shot.remove(shot1)
                player.flamethrower = False  
                flamethrower_sound.stop()  
    
        if player.shotgunAmmo == 0: #Munition leer = Normales Laufmodel
            player.shotgun = False
            
        if zombieCounter<=0 and zombieAttack:
            zombieAttack = False
            
        elif zombieAttack:
            zombieCounter -= 10
    
        if nextZombie>0:
            nextZombie -= 2
        else: 
            fZombie = spawnRandomZombie(800)
            nextZombie = randint(a,b) #Abstand Zombie und naechster Zombie
            if a > 250:
                a -= 5
            if b > 350:
                b -= 10
                
            allzombies.add(fZombie)
        
        checkAllCollisions(player,allzombies,powerups,ui,shot,projectiles,a,b,back1,back2,screenWidth)
        
        
        #Soundabfragen:
        if player.invincible == False:
            chainsaw_sound.stop()

        
        buttonSoundOnOff.update()
        
        
        player.update(time_passed)
        ui.update(time_passed)
        hearts.update(time_passed)
        allzombies.update(time_passed)
        powerups.update(time_passed)
        projectiles.update(time_passed)
        shot.update(time_passed)
       
        
        pygame.display.update()
        
        
def bossfight(x,allzombies,player,a,b,back1,back2,screenWidth):
    for zombie in allzombies:
        zombie.tank = True
        zombie.speed -= 2
        zombie.dead = True
        zombie.act_frame = 0
    tankBoss = Tank((700,0),0.01)
    
    player.tank = True
    
    powerups = pygame.sprite.RenderUpdates()
    
    projectiles = pygame.sprite.RenderUpdates()
    
    bloodsplat = Bloodsplat((tankBoss.rect.centerx-40,tankBoss.rect.centery-100),0.01)
    
    ui = pygame.sprite.RenderUpdates()
    
    health = HealthTank((250,20))
    
    
    while tankBoss.dead == False and tankBoss.flameDead == False:
        
        checkEvents(player,shot)
        
        screen.blit(back1, (x,0))
        
        labelKill = font.render("Kills: "+str(player.kills),True,(255,255,255))
        screen.blit(labelKill,(250,40))
        
        labelDistance = font.render("Distance: "+str(player.distance),True,(255,255,255))
        screen.blit(labelDistance,(390,40))
        
        time_passed = clock.tick(100)
        player.reloadCD -= 30
        
        checkAllCollisions(player, allzombies, powerups, ui, shot, projectiles,a,b,back1,back2,screenWidth)
        
        if tankBoss.throwcounter == 0 and tankBoss.lengthThrow == 3:          
            if len(projectiles.sprites()) == 0 and len(powerups.sprites()) == 0:
                throwThing = randint(0,1)
                if throwThing == 0:
                    stone = Stone((tankBoss.rect.centerx-40,tankBoss.rect.centery-70),0.01)
                    projectiles.add(stone)
                else:
                    if player.lifes >= 3:
                        cratetypeBoss = randint(2,3)
                    else:
                        cratetypeBoss = randint(1,3)
                    crate = Crate(((tankBoss.rect.centerx-40,tankBoss.rect.centery-70)),0.05,cratetypeBoss,5)
                    powerups.add(crate)
        
        for crate in powerups:
            if crate.rect.left > tankBoss.rect.centerx-40:
                powerups.remove(crate)
        
        
        screen.blit(health.image, health.rect)
        screen.blit(player.image,player.rect)
        screen.blit(tankBoss.image,tankBoss.rect)
        screen.blit(bloodsplat.image,bloodsplat.rect)
        allzombies.draw(screen)
        hearts.draw(screen)
        projectiles.draw(screen)
        powerups.draw(screen)
        shot.draw(screen)

        if player.shotgunAmmo > 0:
            screen.blit(shotgun,(10,20))
            label = font.render("Ammo: "+str(player.shotgunAmmo),True,(255,255,255))
            screen.blit(label,(60,25))
        
        if player.doublejumpDuration > 0.0:
            screen.blit(doubleJump,(10,180))
            labelJump = font.render("Jump Time: "+str(player.doublejumpDuration*0.001),True,(255,255,255))
            screen.blit(labelJump,(60,180))
            
        if player.chainsawCounter > 0.0:
            screen.blit(chainsaw,(10,60))
            labelChainsaw = font.render("Invincible: "+str(player.chainsawCounter*0.001),True,(255,255,255))
            screen.blit(labelChainsaw,(60,60))    
            
            
        if player.gasAmmo> 0:
            screen.blit(flamethrower,(5,80))
            labelFlamethrower= font.render("Flamethrower: "+str(player.gasAmmo),True,(255,255,255))
            screen.blit(labelFlamethrower,(60,100))  
        
        if player.bombAmmo >0:
            screen.blit(airstrike,(10,140))
            labelAirstrike= font.render("Airstrike: "+str(player.bombAmmo),True,(255,255,255))
            screen.blit(labelAirstrike,(60,140)) 
    
        

            
        if player.throwFlames:
            if player.gasAmmo>0:
                player.gasAmmo -=1
        
            elif player.gasAmmo <= 0:
                player.throwFlames = False
                for shot1 in shot:
                    if shot1.type == 1:
                        shot.remove(shot1)
                player.flamethrower = False  
                flamethrower_sound.stop()     

        if collision(player,tankBoss) and tankBoss.health > 0:
            player.dead = True
            player.tank = False
            player.act_frame = 0
            gameOver(True, player, x,back1, back2,screenWidth)         
            
        for shot1 in shot:
            if collision (shot1,tankBoss):
                if shot1.type == 0:
                    tankBoss.health -= 1
                    bloodsplat = Bloodsplat((tankBoss.rect.centerx-40,tankBoss.rect.centery-100),0.01)
                    
                    shot.remove(shot1)
                elif shot1.type == 1:
                    tankBoss.health -= 0.02
                    tankBoss.burn = True
        
        bloodsplat.update(time_passed)
        health.update(tankBoss)
        shot.update(time_passed)
        powerups.update(time_passed)
        projectiles.update(time_passed)
        hearts.update(time_passed)
        allzombies.update(time_passed)
        tankBoss.update(time_passed)
        player.update(time_passed)
        
        pygame.display.update()
    
    allzombies.add(tankBoss)
    for zombie in allzombies:
        zombie.speed += 2
        zombie.tank = False
        
    player.kills += 10
    player.tank = False    
    continueGame(player,x,allzombies,a,b,False,back1,back2,screenWidth)
        
        
        
        
def start(startThisShit):

    startScreen = pygame.image.load("StartScreen.png").convert_alpha()
    while startThisShit:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:

                if event.key == K_m:
                    
                    if buttonSoundOnOff.change:
                        buttonSoundOnOff.change = False
                        pygame.mixer.music.pause()
                        buttonSoundOnOff.clicked = True
    
                    else:
                        buttonSoundOnOff.change = True
                        pygame.mixer.music.unpause()
                        buttonSoundOnOff.clicked = False
                        
                if event.key == K_1:
                    b = "Background_02.png"
                    startThisShit = False
                    gameStart(b,6000)
                if event.key == K_2:
                    b = "forest.png"
                    startThisShit = False
                    gameStart(b,3200)
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                
                if buttonSoundOnOff.pressed(mouse) and buttonSoundOnOff.change:
                    buttonSoundOnOff.change = False
                    pygame.mixer.music.pause()
                    buttonSoundOnOff.clicked = True

                else:
                    buttonSoundOnOff.change = True
                    pygame.mixer.music.unpause()
                    buttonSoundOnOff.clicked = False
                


                    

         
        
        screen.blit(startScreen,(0,0))
        screen.blit(buttonSoundOnOff.image,buttonSoundOnOff.rect)
        
        
        buttonSoundOnOff.update()

        pygame.display.update()
        
        
def gameOver(over,player,x,back1,back2,screenWidth):

    clock=pygame.time.Clock()
    
    over = GameOverScreen((0,0),0.013,gameOverScreen)
    
    screen.blit(over.image,over.rect)

    font = pygame.font.SysFont("Arial", 40, True, True)
    font2 = pygame.font.SysFont("Arial", 60, True, True)
    
    gameOverSpeech_sound.play()
    
    while over:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    over = False
                    start(True)
                if event.key == K_m:
                    
                    if buttonSoundOnOff.change:
                        buttonSoundOnOff.change = False
                        pygame.mixer.music.pause()
                        buttonSoundOnOff.clicked = True
    
                    else:
                        buttonSoundOnOff.change = True
                        pygame.mixer.music.unpause()
                        buttonSoundOnOff.clicked = False
                        
                        
                if event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    
                    if buttonSoundOnOff.pressed(mouse) and buttonSoundOnOff.change:
                        buttonSoundOnOff.change = False
                        pygame.mixer.music.pause()
                        buttonSoundOnOff.clicked = True
    
                    else:
                        buttonSoundOnOff.change = True
                        pygame.mixer.music.unpause()
                        buttonSoundOnOff.clicked = False
                    
                    
        time_passed = clock.tick(50)
        screen.blit(back1, (x,0))
        screen.blit(back2,(x+screenWidth,0))
        x = x - 2
        if x <= -screenWidth:
            x = 0
        
        screen.blit(player.image,player.rect)        
        screen.blit(over.image,over.rect)
        
        if over.counter == 0:
            
            labelKill = font.render("Kills: "+str(player.kills),True,(204,0,0))
            screen.blit(labelKill,(100,500))
            
            labelDistance = font.render("Distance: "+str(player.distance),True,(204,0,0))
            screen.blit(labelDistance,(500,500))
            
            labelPoints = font2.render("Total Points: "+str(player.kills*10+player.distance),True,(204,0,0))
            screen.blit(labelPoints,(200,50))
        
        
        screen.blit(buttonSoundOnOff.image,buttonSoundOnOff.rect)
        
        
        buttonSoundOnOff.update()
       
        
        over.update(time_passed)
        player.update(time_passed)
        
        pygame.display.update()



pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

screen = pygame.display.set_mode((800,600), 0, 32)
pygame.display.set_caption("Zombie Jump")


pygame.mixer.music.load("MadMavBlackSheepOgg.ogg")

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)


buttonSoundOnOff = ButtonSound((5,565))



x = 0

hearts = pygame.sprite.OrderedUpdates()
 
shotgun = pygame.image.load("shotgun.png").convert_alpha()
doubleJump = pygame.image.load("doublejumpSmall.png").convert_alpha()
doubleJump = pygame.transform.scale(doubleJump,(30,30))

chainsaw = pygame.image.load("ChainsawBild.png").convert_alpha()

flamethrower = pygame.image.load("Flamethrower.png").convert_alpha()

airstrike = pygame.image.load("BombSymbol.png").convert_alpha()
airstrike = pygame.transform.scale(airstrike,(30,30))
    
 


shotgun_sound = pygame.mixer.Sound("shotgunSound2.wav")
shotgun_sound.set_volume(0.5)

shotgunSpeech_sound = pygame.mixer.Sound("shotgunSpeech_01.wav")

airstrikeSpeech_sound = pygame.mixer.Sound("Airstrike.wav")

chainsawSpeech_sound = pygame.mixer.Sound("Chainsaw.wav")

flamethrowerSpeech_sound = pygame.mixer.Sound("Flamethrower.wav")

ExtraLifeSpeech_sound = pygame.mixer.Sound("ExtraLife.wav")

doubleJumpSpeech_sound = pygame.mixer.Sound("DoubleJump.wav")

weaponLossSpeech_sound = pygame.mixer.Sound("WeaponLost.wav")

zombieAttackSpeech_sound = pygame.mixer.Sound("ZombieAttack.wav")

gameOverSpeech_sound = pygame.mixer.Sound("GameOver.wav")

chainsawFlesh1_sound = pygame.mixer.Sound("chainsawFleshSound1.wav")
chainsawFlesh1_sound.set_volume(0.5)

chainsawFlesh2_sound = pygame.mixer.Sound("chainsawFleshSound2.wav")
chainsawFlesh2_sound.set_volume(0.5)

chainsawFlesh3_sound = pygame.mixer.Sound("chainsawFleshSound3.wav")
chainsawFlesh3_sound.set_volume(0.5)

chainsawFlesh4_sound = pygame.mixer.Sound("chainsawFleshSound4.wav")
chainsawFlesh4_sound.set_volume(0.5)

chainsaw_sound = pygame.mixer.Sound("chainsawSound.wav")
chainsaw_sound.set_volume(0.5)

bombExplosion_sound = pygame.mixer.Sound("bombExplosionSound.wav")
bombExplosion_sound.set_volume(0.5)

flamethrower_sound = pygame.mixer.Sound("FlamethrowerSound.wav")
flamethrower_sound.set_volume(0.5)

imagesExplosion = load_sliced_sprites(533,300,"LuftschlagExplosion.png")

gameOverScreen = load_sliced_sprites(400,300,"GameOverScreen3.png")

clock=pygame.time.Clock()
shot = pygame.sprite.RenderUpdates()
font = pygame.font.SysFont("Arial", 20, True, False)

time_passed = clock.tick(100)

#Starte unseres Spiel
start(True)





    