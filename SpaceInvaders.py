##Space Invaders##

import pygame
import sys
from random import shuffle
from pygame.locals import *

#CONSTANTS

# COLORS
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
YELLOW    = (255, 255,   0)
ORANGE    = (255, 128,   0)
CYAN      = (  0, 255, 255)
BLACK     = (  0,   0,   0)
GREY      = ( 50,  50,  48)
COMBLUE   = (233, 232, 255)
WHITE     = (255, 255, 255)

## Player Constants ##

PLAYERWIDTH = 40
PLAYERHEIGHT = 20
PLAYERSPEED = 5


## Display Constants ##

GAMETITLE = 'Space Invaders!'
DISPLAYWIDTH = 640
DISPLAYHEIGHT = 480
BGCOLOR = GREY
XMARGIN = 50
YMARGIN = 50

## Bullet Constants ##

BULLETWIDTH = 10
BULLETHEIGHT = 10
BULLETOFFSET = 1500

## Enemy Constants ##

ENEMYWIDTH = 30
ENEMYHEIGHT = 30
ENEMYGAP = 20
ARRAYWIDTH = 10
ARRAYHEIGHT = 3
MOVETIME = 500
MOVEX = 10
MOVEY = ENEMYHEIGHT
TIMEOFFSET = 300
DIRECT_DICT = {pygame.K_LEFT  : (-1),
               pygame.K_RIGHT : (1)}





class Player(pygame.sprite.Sprite):
   
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYERWIDTH
        self.height = PLAYERHEIGHT
        self.image = self.getImage()
        self.rect = self.image.get_rect()

        self.speed = PLAYERSPEED
    
    def update(self, keys, *args):
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key] * self.speed
            self.checkForSide()
    def moveLeft(self):
        self.rect .x -= -1 * self.speed            
        self.checkForSide()

    def moveRight(self):
        self.rect.x += 1 * self.speed    
        self.checkForSide()

    def checkForSide(self):
        if self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH
            
        elif self.rect.left < 0:
            self.rect.left = 0
    def getImage(self):
        image = pygame.image.load('spaceship.png') 
        image.convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))

        return image
       



class Blocker(pygame.sprite.Sprite):
       
    def __init__(self, side, color, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = side
        self.height = side
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
    
        self.row = row
        self.column = column



class Bullet(pygame.sprite.Sprite):
        
    def __init__(self, rect, color, vectory, speed):
        pygame.sprite.Sprite.__init__(self)
        self.width = BULLETWIDTH
        self.height = BULLETHEIGHT
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = rect.centerx
        self.rect.top = rect.bottom
        self.vectory = vectory
        self.speed = speed
    

    def update(self, *args):
        self.oldLocation = (self.rect.x, self.rect.y)
        self.rect.y += self.vectory * self.speed

        if self.rect.bottom < 0 or self.rect.bottom > 500:
            self.kill()

        

class Enemy(pygame.sprite.Sprite):
       
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = ENEMYWIDTH
        self.height = ENEMYHEIGHT
        self.row = row
        self.column = column
        self.image = self.getImage()
        self.rect = self.image.get_rect()
      
        self.vectorx = 1
        self.moveNumber = 0
        self.moveTime = MOVETIME
        self.timeOffset = row * TIMEOFFSET
        self.timer = pygame.time.get_ticks() - self.timeOffset


    def update(self, keys, currentTime):
        if currentTime - self.timer > self.moveTime:
            if self.moveNumber <= 5:
                self.rect.x += MOVEX * self.vectorx
                self.moveNumber = self.moveNumber + 1
            if self.moveNumber > 5:
                self.moveNumber = 0
                self.rect.y += MOVEY
                self.vectorx = self.vectorx * -1
                if self.moveTime >= 80:
                    self.moveTime -= 70
            self.timer = currentTime


    def getImage(self):
        image = pygame.image.load('alien1.png')
        for i in range(3):
           if self.row == i:
                image= pygame.image.load('alien'+str(i+1)+".png")
        image.convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))

        return image



class Text(object):
    def __init__(self, font, size, message, color, rect, surface):
        self.message = message
        self.font = pygame.font.Font(font, size)
        self.surface = self.font.render(self.message, 1, color)
        self.rect = self.surface.get_rect()
        self.rect.centery = rect.centery - 10
        self.rect.centerx = rect.centerx

    def draw(self, surface):
        surface.blit(self.surface, self.rect)



class App(object):
    
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.start = 1
        self.gameOver = 0
        self.beginGame = 0
        

    def resetGame(self):
        self.start = 1
        self.needToMakeEnemies = 1
        
        self.introMessage1 = Text('orena.ttf', 35,
                                 'Space Invaders!',
                                 WHITE, self.displayRect,
                                 self.displaySurf)
        self.introMessage2 = Text('orena.ttf', 20,
                                  'Press Any Key to Continue',
                                  GREEN, self.displayRect,
                                  self.displaySurf)
        self.introMessage2.rect.top = self.introMessage1.rect.bottom + 5

        self.gameOverMessage = Text('orena.ttf', 30,
                                    'GAME OVER', GREEN,
                                    self.displayRect, self.displaySurf)
        
        self.player = self.makePlayer()
        self.bullets = pygame.sprite.Group()
        self.blockerGroup3 = self.makeBlockers(2)
        self.greenBullets = pygame.sprite.Group()
        self.blockerGroup4 = self.makeBlockers(3)
        self.blockerGroup1 = self.makeBlockers(0)
        self.blockerGroup2 = self.makeBlockers(1)
        self.allBlockers = pygame.sprite.Group(self.blockerGroup1, self.blockerGroup2,
                                               self.blockerGroup3, self.blockerGroup4)
        self.allSprites = pygame.sprite.Group(self.player, self.allBlockers)
        self.keys = pygame.key.get_pressed()
        self.gameOverTime = pygame.time.get_ticks()
        self.fps = 60
        self.enemyMoves = 0
        self.clock = pygame.time.Clock()
        self.enemyBulletTimer = pygame.time.get_ticks()
        self.gameOver = 0
        



    def makeBlockers(self, number=1):
        blockerGroup = pygame.sprite.Group()
        
        for row in range(0,5,1):
            for column in range(0,7,1):
                blocker = Blocker(10, GREEN, row, column)
                blocker.rect.y = 375 + (row * blocker.height)
                blocker.rect.x = 50 + (150 * number) + (column * blocker.width)
                blockerGroup.add(blocker)

        for blocker in blockerGroup:
            if (blocker.column == 0 and blocker.row == 0 or blocker.column == 6 and blocker.row == 0):
                blocker.kill()

        return blockerGroup



    def checkForEnemyBullets(self):
        redBulletsGroup = pygame.sprite.Group()

        for bullet in self.bullets:
            if bullet.color == RED:
                redBulletsGroup.add(bullet)

        for bullet in redBulletsGroup:
            if pygame.sprite.collide_rect(bullet, self.player):
                self.gameOver = 1
                self.gameOverTime = pygame.time.get_ticks()
                bullet.kill()



    def shootEnemyBullet(self, rect):
        if (pygame.time.get_ticks() - self.enemyBulletTimer) > BULLETOFFSET:
            self.bullets.add(Bullet(rect, RED, 1, 5))
            self.allSprites.add(self.bullets)
            self.enemyBulletTimer = pygame.time.get_ticks()



    def findEnemyShooter(self):
        columnList = []
        for enemy in self.enemies:
            columnList.append(enemy.column)
        #get rid of duplicate columns
        columnList = list(columnSet)
        columnSet = set(columnList)
        shuffle(columnList)

        rowList = []
        column = columnList[0]
        enemyList = []
        for enemy in self.enemies:
            if enemy.column == column:
                rowList.append(enemy.row)

        row = max(rowList)

        for enemy in self.enemies:
            if enemy.column == column and enemy.row == row:
                self.shooter = enemy 

        
        
        
        
    

    def makeScreen(self):
        pygame.display.set_caption(GAMETITLE)
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        displayRect = displaySurf.get_rect()
        displaySurf.fill(BGCOLOR)
        displaySurf.convert()

        return displaySurf, displayRect



    def makePlayer(self):
        player = Player()
        ##Place the player centerx and five pixels from the bottom
        player.rect.centerx = self.displayRect.centerx
        player.rect.bottom = self.displayRect.bottom - 5

        return player



    def makeEnemies(self):
        enemies = pygame.sprite.Group()
        
        for row in range(ARRAYHEIGHT):
            for column in range(ARRAYWIDTH):
                enemy = Enemy(row, column)
                enemy.rect.x = XMARGIN + (column * (ENEMYWIDTH + ENEMYGAP))
                enemy.rect.y = YMARGIN + (row * (ENEMYHEIGHT + ENEMYGAP))
                enemies.add(enemy)

        return enemies



    def checkInput(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()  
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and len(self.greenBullets) < 1:
                    bullet = Bullet(self.player.rect, GREEN, -1, 20)
                    self.greenBullets.add(bullet)
                    self.bullets.add(self.greenBullets)
                    self.allSprites.add(self.bullets)
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()


    def startInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                self.gameOver = 0
                self.start = 0
                self.beginGame = 1


    def gameOverInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYUP:
                self.start = 1
                self.beginGame = 0
                self.gameOver = 0
    

        


    def checkCollisions(self):
        self.checkForEnemyBullets()
        pygame.sprite.groupcollide(self.bullets, self.enemies, 1, 1)
        pygame.sprite.groupcollide(self.enemies, self.allBlockers, 0, 1)
        self.collide_green_blockers()
        self.collide_red_blockers()
        

        
    def collide_green_blockers(self):
        for bullet in self.greenBullets:
            casting = Bullet(self.player.rect, GREEN, -2, 5)
            casting.rect = bullet.rect.copy()
            for pixel in range(bullet.speed):
                hit = pygame.sprite.spritecollideany(casting,self.allBlockers)
                if hit:
                    hit.kill()
                    bullet.kill()
                    break
                casting.rect.y -= 2


    def collide_red_blockers(self):
        reds = (shot for shot in self.bullets if shot.color == RED)
        red_bullets = pygame.sprite.Group(reds)
        pygame.sprite.groupcollide(red_bullets, self.allBlockers, 1, 1)

    



    def checkGameOver(self):
        if len(self.enemies) == 0:
            self.gameOver = 1
            self.start = 0
            self.beginGame = 0
            self.gameOverTime = pygame.time.get_ticks()

        else:
            for enemy in self.enemies:
                if enemy.rect.bottom > DISPLAYHEIGHT:
                    self.gameOver = 1
                    self.start = 0
                    self.beginGame = 0
                    self.gameOverTime = pygame.time.get_ticks()
       
        
                

    def terminate(self):
        pygame.quit()
        sys.exit()


    def mainLoop(self):
        while 1:
            
            if self.gameOver:
                self.playIntroSound = 1
                self.displaySurf.fill(BGCOLOR)
                self.gameOverMessage.draw(self.displaySurf)
                #prevent users from exiting the GAME OVER screen
                #too quickly
                if (pygame.time.get_ticks() - self.gameOverTime) > 2000:
                    self.gameOverInput()
                pygame.display.update()
            
            if self.start:
                self.resetGame()
                self.gameOver = 0
                self.displaySurf.fill(BGCOLOR)
                self.introMessage1.draw(self.displaySurf)
                self.introMessage2.draw(self.displaySurf)
                self.startInput()
                pygame.display.update()

            
            elif self.beginGame:
                if self.needToMakeEnemies:
                    
                    self.enemies = self.makeEnemies()
                    self.allSprites.add(self.enemies)
                    self.needToMakeEnemies = 0
                    pygame.event.clear()
                    
                    
                        
                else:    
                    currentTime = pygame.time.get_ticks()
                    self.displaySurf.fill(BGCOLOR)
                    self.checkInput()
                    self.allSprites.update(self.keys, currentTime)
                    if len(self.enemies) > 0:
                        self.findEnemyShooter()
                        self.shootEnemyBullet(self.shooter.rect)
                    self.checkCollisions()
                    self.allSprites.draw(self.displaySurf)
                    self.blockerGroup1.draw(self.displaySurf)
                    pygame.display.update()
                    self.checkGameOver()
                    self.clock.tick(self.fps)
                    
            
            
    


if __name__ == '__main__':
    app = App()
    app.mainLoop()