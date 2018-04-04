import pygame


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

